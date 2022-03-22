"""Classify images and find faces in them"""
from keras.applications.xception import Xception
from keras.preprocessing import image
from keras.applications.xception import preprocess_input, decode_predictions
import numpy as np
import cv2 as cv
# load the model
model = Xception(weights='imagenet', include_top=True)

def ai_classify_image(img_path, subject):
	"""classify a given image, and see if the classification matches a given subject.
	classification is done via the Viola-Jones algorithm"""
	subjects = []
	subjects.append(subject)
	# load the image as size 299,299 for the model to process
	img = image.load_img(img_path, target_size=(299, 299))
	#############################################
	# convert to numpy array
	x = image.img_to_array(img)
	x = np.expand_dims(x, axis=0)
	x = preprocess_input(x)
	# predict the features of the image
	features = model.predict(x)
	# return the top 25 detected objects
	label = decode_predictions(features, top=25)

	# building is a very broad subject so additional subjects are added
	if subject == 'building':
		subjects.append('shop')
		subjects.append('house')
		subjects.append('stage')
		subjects.append('library')
		subjects.append('planetarium')
		subjects.append('church')
		subjects.append('restaurant')
		subjects.append('wall')
		subjects.append('tile')
		subjects.append('bar')
		subjects.append('dome')

	# see if the subject is one of the features that has been classified
	for subject in subjects:
		if subject in str(label):
			print('val found')
			print(label)
			return True
	print(label)
	return False

def ai_face_recognition(image_path):
	"""ai to find and recognise how many faces are in an image"""
	original_image = cv.imread(image_path)
	# Convert color image to grayscale for Viola-Jones
	grayscale_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
	# Load the classifier and create a cascade object for face detection
	face_cascade = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
	# additional cascade object for bodies 
	body_cascade = cv.CascadeClassifier('haarcascade_fullbody.xml')
	# analyse the image in multiple scales to detect faces
	detected_faces = face_cascade.detectMultiScale(
		grayscale_image,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30,30))

	# do the same for bodies- in case faces are covered
	detected_bodies = body_cascade.detectMultiScale(grayscale_image)

	# uncomment the line below to see what faces are detected while developing
	# show_faces(original_image,detected_faces)

	# return the number of detected faces/bodies by returning the highest value for leniency
	return max(len(detected_faces),len(detected_bodies))

def show_faces(image,faces):
	"""draw a rectangle around the faces and display- useful for developers to see results"""
	for (x, y, w, h) in faces:
		cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

	# show image with faces, and close window when a key is pressed
	cv.imshow("Faces found", image)
	cv.waitKey(0)
	cv.destroyAllWindows()
