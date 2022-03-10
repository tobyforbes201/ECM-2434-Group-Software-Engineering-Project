"""This is used to extract metadata from the image like the location and time taken."""
import datetime
from exif import Image
import geopy.distance


def get_gps(fname):
    """Function which returns GPS coordinated in form tuple (latitude, longitude) in decimal."""
    with open(fname, 'rb') as image_file:
        my_image = Image(image_file)

    if my_image.has_exif:
        return (get_lat(my_image.gps_latitude_ref, my_image.gps_latitude)
                , get_long(my_image.gps_longitude_ref, my_image.gps_longitude))
    raise Exception


def get_lat(ref, lat):
    """A Helper function for get_GPS to convert from degrees to decimal."""
    if ref == "N":
        return lat[0] + (lat[1] / 60) + (lat[2] / 3600)
    return -(lat[0] + (lat[1] / 60) + (lat[2] / 3600))


def get_long(ref, long):
    """A helper function for get_GPS to convert from degrees to decimal."""
    if ref == "E":
        return long[0] + (long[1] / 60) + (long[2] / 3600)
    return -(long[0] + (long[1] / 60) + (long[2] / 3600))


def get_distance(starting_point, fname):
    """A function that gets the distance in km between the location of
     a photo and a GPS location in form (latitude, longitude) in decimal"""
    return geopy.distance.distance(starting_point, get_gps(fname)).km


def get_time(fname):
    """A function that gets the time information from image
     as a string in format YYYY:MM:DD HH:MM:SS."""
    with open(fname, 'rb') as image_file:
        my_image = Image(image_file)

    if my_image.has_exif:
        return my_image.datetime
    raise Exception


def get_time_dif(starting_time, fname):
    """A function that gets the time difference between when a photo
     was taken and a time of choice in format datetime."""
    difference = starting_time - datetime.datetime.strptime(get_time(fname),
                                                            "%Y:%m:%d %H:%M:%S")
    # converts the string into a datetime object
    datetime.timedelta(0, 8, 562000)
    seconds_in_day = 24 * 60 * 60
    return (difference.days * seconds_in_day + difference.seconds) / 60
