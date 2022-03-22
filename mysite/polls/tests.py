"""Django tests to ensure that the app is working correctly are written and run here."""
import tempfile
import datetime

from django.db.models.fields.files import ImageFieldFile
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test.client import Client
from .models import Profile, Image, Challenge
from . import validate, image_metadata

class TestAdminPanel(TestCase):
	"""test admin functionality"""
	def create_user(self):
		"""create a test admin"""
		self.username = "test_admin"
		self.password = User.objects.make_random_password()
		user, created = User.objects.get_or_create(username=self.username)
		user.set_password(self.password)
		user.is_staff = True
		user.is_superuser = True
		user.is_active = True
		user.save()
		self.user = user

	def test_spider_admin(self):
		"""test that admin can login and access admin pages"""
		self.create_user()
		client = Client()
		client.login(username=self.username, password=self.password)
		admin_pages = [
			"/admin/",
		]
		for page in admin_pages:
			resp = client.get(page)
			self.assertEqual(resp.status_code, 200)
			assert b"<!DOCTYPE html" in resp.content
		self.user.delete()

class TestUserPanel(TestCase):
	"""test user functionality"""
	def create_user(self):
		"""create a test user"""
		self.username = "testuser"
		self.password = "Cheesytoenails@123"
		user, created = User.objects.get_or_create(username=self.username)
		user.set_password(self.password)
		user.is_staff = False
		user.is_superuser = False
		user.is_active = True
		user.save()
		self.user = user

	def test_user_credentials(self):
		"""test that the user has the correct username, password"""
		self.create_user()
		client = Client()
		client.login(username=self.username, password=self.password)

		self.assertEqual("testuser",self.username)
		self.assertEqual("Cheesytoenails@123",self.password)

		self.user.delete()

	def test_user_profile(self):
		"""test that user profile is created when user is created"""
		self.create_user()
		if len(Profile.objects.filter(user=self.user)) !=1:
			self.fail("Profile not created correctly")
		self.user.delete()
	def test_spider_user(self):
		"""test that user can login and access user pages"""
		self.create_user()
		client = Client()
		client.login(username=self.username, password=self.password)
		user_pages = [
			"/polls/",
			"/polls/feed",
			"/polls/uploadimage",
			"/polls/leaderboards",
			"/polls/profile",
			"/polls/viewprofile/"+str(self.user.username)
		]
		for page in user_pages:
			resp = client.get(page)
			self.assertEqual(resp.status_code, 200)
			assert b"<!DOCTYPE html" in resp.content

		# should be redirected away from admin page
		admin_page = "/admin/"
		resp = client.get(admin_page)
		self.assertEqual(resp.status_code, 302)

		self.user.delete()

class TestValidate(TestCase):
	"""tests for validate.py"""
	def create_user(self,username,password):
		"""create a test admin"""
		self.username = username
		self.password = password
		user, created = User.objects.get_or_create(username=self.username)
		user.set_password(self.password)
		user.is_staff = False
		user.is_superuser = False
		user.is_active = True
		user.save()
		self.user = user

	def setUp(self):
		"""create a user and paths to test images"""
		self.create_user("testuser","Cheesytoenails@123")
		self.large_image_path = './media/feed/picture/6mb_image.jpg'
		self.good_image_path = './media/feed/picture/Brennan_On_the_Side_of_the_Angels_2.jpg'
		self.bad_image_path = './media/feed/picture/university-of-exeter-forum.jpg'

	def tearDown(self):
		"""delete the test user"""
		User.objects.get(username="testuser").delete()

	def test_check_user_unique(self):
		"""should raise error if username already exists"""
		self.assertRaises(ValidationError, validate.check_user_unique, "testuser")

		try:
			validate.check_user_unique("unique_user")
		except ValidationError:
			self.fail("validate.check_user_unique() raised ValidationError unexpectedly!")

	def test_validate_number(self):
		"""test that password number validation works correctly"""

		# test with input expected to raise error
		self.assertRaises(ValidationError,validate.validate_number,"hello")

		# test with more extreme input
		self.assertRaises(ValidationError,validate.validate_number,"onzgoiaegnimnMAMS")

		# test with valid input
		try:
			validate.validate_number("hdbg1247562mdm")
		except ValidationError:
			self.fail("validate.validate_number() raised ValidationError unexpectedly!")

	def test_validate_special(self):
		"""test that password special character validation works correctly"""

		# test with input expected to raise error
		self.assertRaises(ValidationError,validate.validate_number,"hello")

		# test with more extreme input
		self.assertRaises(ValidationError,validate.validate_number,"onzgoiaegnimnMAMS")

		# test with valid input
		try:
			validate.validate_number("@124hsvjv£%*(*&^%£")
		except ValidationError:
			self.fail("validate.check_image_type() raised ValidationError unexpectedly!")

	def test_validate_upper_lower(self):
		"""test that upper and lower case validation for passwords works"""

		# test with input that should raise error
		self.assertRaises(ValidationError, validate.validate_upper_lower, "hello")

		# more extreme input
		self.assertRaises(ValidationError, validate.validate_upper_lower, "kjaelnal31259$$*&")

		# input that should be valid
		try:
			validate.validate_upper_lower("HEllO")
		except ValidationError:
			self.fail("validate.validate_upper_lower() raised ValidationError unexpectedly!")

	def test_validate_check_image_type(self):
		"""test that image type is validated correctly"""

		# any image that is not .jpg should raise an error
		image = tempfile.NamedTemporaryFile(suffix=".png")
		self.assertRaises(ValidationError, validate.check_image_type, image)


		# test that it works with jpg
		image = tempfile.NamedTemporaryFile(suffix=".jpg")
		try:
			validate.check_image_type(image)
		except ValidationError:
			self.fail("validate.check_image_type() raised ValidationError unexpectedly!")

	def test_validate_image_size(self):
		"""test that image size is validated correctly"""
		image = tempfile.NamedTemporaryFile(suffix='.jpg')

		#a small tempfile should be valid
		self.assertEqual('valid',validate.validate_image_size(image.name))

		#a large image should be invalid
		self.assertEqual('invalid',validate.validate_image_size(self.large_image_path))

	def test_validate_metadata(self):
		"""test that metadata is validated"""

		# image with correct metadata should be valid
		self.assertEqual("valid",validate.validate_metadata(self.good_image_path))

		# image without metadata should be invalid
		self.assertEqual("missing metadata",validate.validate_metadata(self.bad_image_path))


class TestImage(TestCase):
	"""test the Image model"""
	def create_user(self):
		"""create a test user"""
		self.username = "test_user"
		self.password = User.objects.make_random_password()
		user, created = User.objects.get_or_create(username=self.username)
		user.set_password(self.password)
		user.is_staff = False
		user.is_superuser = False
		user.is_active = True
		user.save()
		self.user = user

	def setUp(self):
		"""create a test user and a temporary test image to be stored in an Image model object"""
		self.create_user()
		self.img_obj = Image.objects.create(user=self.user
							,title="testimg",
							description="desc",
							img=SimpleUploadedFile(name='test_image.jpg',
							content='',
							content_type='image/jpeg'),
							gps_coordinates=(50.7366, -3.5350),
							taken_date=datetime.datetime.now(),score=0)

	def tearDown(self):
		"""delete the user and their test image objects"""
		images = Image.objects.filter(user=self.user)
		for image in images:
			image.img.delete()
			image.delete()
		self.user.delete()

	def test_image(self):
		"""test that Image objects are created and stored correctly"""
		self.assertEqual("testimg",self.img_obj.title)
		self.assertEqual("desc",self.img_obj.description)
		if isinstance(self.img_obj.img,ImageFieldFile) == False:
			self.fail("img in Image model not stored correctly")
		self.assertEqual((50.7366,-3.5350),self.img_obj.gps_coordinates)
		self.assertEqual(0,self.img_obj.score)

class TestChallenge(TestCase):
	"""test the Challenge model"""
	def setUp(self):
		"""set up a test challenge object"""
		self.challenge_obj = Challenge.objects.create(name='test_challenge',
												description='desc',
												location=(50.7366,-3.5350),
												locationRadius=1,
												subject='building',
												startDate=datetime.datetime.now(),
												endDate=datetime.datetime.now()
												)
		self.challenge_obj.save()
	def tearDown(self):
		"""delete the challenge object"""
		self.challenge_obj.delete()

	def test_challenge(self):
		"""test that challnge objects are being saved and stored correctly"""
		self.assertEqual(self.challenge_obj.name,'test_challenge')
		self.assertEqual(self.challenge_obj.description,'desc')
		self.assertEqual(self.challenge_obj.location,(50.7366,-3.5350))
		self.assertEqual(self.challenge_obj.subject,'building')

class TestImageMetadata(TestCase):
	"""test methods from image_metadata"""
	def create_user(self):
		"""create a test user"""
		self.username = "test_user"
		self.password = User.objects.make_random_password()
		user, created = User.objects.get_or_create(username=self.username)
		user.set_password(self.password)
		user.is_staff = False
		user.is_superuser = False
		user.is_active = True
		user.save()
		self.user = user

	def setUp(self):
		"""set up a good image with metadata, bad image without"""
		self.good_image_path = './media/feed/picture/Brennan_On_the_Side_of_the_Angels_2.jpg'
		self.bad_image_path = './media/feed/picture/university-of-exeter-forum.jpg'

	def tearDown(self):
		"""nothing to tear down"""
		pass

	def test_get_gps(self):
		"""test that gps data is gathered correctly"""

		# image without metadata should throw exception
		with self.assertRaises(Exception) as context:
			image_metadata.get_gps(self.bad_image_path)
		self.assertTrue('exif not found' in str(context.exception))

		# image with metadata should return a tuple with location data
		try:
			ret_val = image_metadata.get_gps(self.good_image_path)
			if isinstance(ret_val,tuple) == False:
				self.fail("image_metadata.get_gps() does not return a tuple")
			else:
				pass
		except Exception:
			self.fail("image_metadata.get_gps() threw an unexpected exception")

	def test_get_lat(self):
		"""test that latitudes are either positive or negative depending on north vs south"""
		assert image_metadata.get_lat("N",[1,0,2]) >0
		assert image_metadata.get_lat("S",[1,0,2]) <0
		# ignore unexpected data
		assert image_metadata.get_lat("asfadfac",[1,0,2]) <0

	def test_get_long(self):
		"""test that longitudes are either positive or negative depending on east vs west"""
		assert image_metadata.get_long("E",[1,0,2]) >0
		assert image_metadata.get_lat("W",[1,0,2]) <0
		# unexpected data should be ignored
		assert image_metadata.get_lat("asfadfac",[1,0,2]) <0

	def test_get_distance(self):
		"""test that distance between two points is correct"""

		# this sum shows whether the distance calculation is working
		self.assertEqual(0,image_metadata.get_distance((50.7366, -3.5350),(50.7366, -3.5350)))

	def test_get_time(self):
		"""test that time data is gathered from an image"""
		try:
			ret_val = image_metadata.get_time(self.good_image_path)
			try:
				time = datetime.datetime.strptime(ret_val, '%Y:%m:%d %H:%M:%S')
			except:
				self.fail("image_metadata.get_time() does not return a datetime")
		except:
			self.fail("image_metadata.get_time() fails to find a time")

	def test_get_time_dif(self):
		"""test the image_metadata get_time_dif by recreating the logic"""
		time = datetime.datetime.now()
		difference = time - time
		datetime.timedelta(0, 8, 562000)
		seconds_in_day = 24 * 60 * 60
		ret_val = (difference.days * seconds_in_day + difference.seconds) / 60

    	#difference between equal dates should be 0 to prove that the sum is calculated correctly
		self.assertEqual(0,ret_val)
