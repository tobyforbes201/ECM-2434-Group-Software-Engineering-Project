from exif import Image
import geopy.distance
import datetime

#funtion which returns GPS coordinated in form tuple (latitude, longitude) in decimal
def get_GPS(fname):
    with open(fname, 'rb') as image_file:
        my_image = Image(image_file)

    if my_image.has_exif:
        return (get_lat(my_image.gps_latitude_ref, my_image.gps_latitude)
                , get_long(my_image.gps_longitude_ref, my_image.gps_longitude))
    else:
        print("error")

#helper function for get_GPS to convert from degrees to decimal
def get_lat(ref, lat):
    if ref == "N":
        return lat[0] + (lat[1]/60) + (lat[2]/3600)
    else:
        return -(lat[0] + (lat[1]/60) + (lat[2]/3600))

#helper function for get_GPS to convert from degrees to decimal
def get_long(ref, long):
    if ref == "E":
        return long[0] + (long[1]/60) + (long[2]/3600)
    else:
        return -(long[0] + (long[1]/60) + (long[2]/3600))

#gets the distance in km between the location of a photo and a GPS location in form (latitude, longitude) in decimal
def get_distance(startingPoint, fname):
    return geopy.distance.distance(startingPoint, get_GPS(fname)).km

#gets the time information from image as a string in format YYYY:MM:DD HH:MM:SS
def get_time(fname):
    with open(fname, 'rb') as image_file:
        my_image = Image(image_file)

    if my_image.has_exif:
        return my_image.datetime
    else:
        print("error")

#gets the time difference between when a photo was taken and a time of choice in format datetime
def get_time_dif(startingTime, fname):
    difference = startingTime - datetime.datetime.strptime(get_time(fname),"%Y:%m:%d %H:%M:%S") #converts the string into a datetime object
    datetime.timedelta(0, 8, 562000)
    seconds_in_day = 24 * 60 * 60
    return (difference.days * seconds_in_day + difference.seconds)/ 60
    
