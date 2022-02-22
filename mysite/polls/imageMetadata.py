from exif import Image

def get_GPS(fname):
    with open(fname, 'rb') as image_file:
        my_image = Image(image_file)

    if my_image.has_exif:
        return [my_image.gps_latitude,my_image.gps_longitude]
    else:
        print("error")

def get_time(fname):
    with open(fname, 'rb') as image_file:
        my_image = Image(image_file)

    if my_image.has_exif:
        return my_image.datetime
    else:
        print("error")

print(get_GPS('test.jpg'))
