# BeautySpot: ECM-2434-Group-Software-Engineering-Project

Developers
-----------
Harry Collins- https://github.com/harry-kav  
Toby Forbes- https://github.com/tobyforbes201  
Jason Gurung - https://github.com/jasongrg1  
Artur Kapitanczyk - https://github.com/arturkapitanczyk  
Shalan Sharma- https://github.com/Shalan-Sharma  
Jack Shaw- https://github.com/js1294  

Description
------------

This web-application is a game to take the best photos around the University of Exeter campus.  
Users take photos around campus fulfilling different criteria to complete challenges, which will have a large variety and can be daily, weekly, time-limited, special events etc.  
Points are rewarded for completing challenges and for winning them. Challenge winners can be decided by gamekeepers (admins) or through a user voting system.  
These points can be used to unlock stickers and tags to use on photos, as well as on weekly and all-time leaderboards showing who the most prominent photographers are.  
Photos can be viewed in the photo feed, which shows the latest and highest-rated photos for each live challenge.  

Features currently implemented
-------------------------------

User signup and login  
<img alt="Sign up" src="https://github.com/js1294/ECM-2434-Group-Software-Engineering-Project/blob/photoFeed/docs/images/signup.png">  
<img alt="Sign in" src="https://github.com/js1294/ECM-2434-Group-Software-Engineering-Project/blob/photoFeed/docs/images/signin.png">  
  
Photo uploading to database  
<img alt="Photo uploading" src="https://github.com/js1294/ECM-2434-Group-Software-Engineering-Project/blob/photoFeed/docs/images/uploadphoto.png">
<img alt="Upload success" src="https://github.com/js1294/ECM-2434-Group-Software-Engineering-Project/blob/photoFeed/docs/images/uploadsuccess.png">  
  
Acquiring date and location metadata from photos  
Photo feed with the latest and highest-rated challenge submissions  
<img alt="Photo feed" src="https://github.com/js1294/ECM-2434-Group-Software-Engineering-Project/blob/photoFeed/docs/images/feed1.png">  
CSS styling  
<img alt="CSS" src="https://github.com/js1294/ECM-2434-Group-Software-Engineering-Project/blob/photoFeed/docs/images/feed2.png">  
Photo moderation and removal  
Gamekeeper/admin privileges

Features to be added
---------------------

Photo challenges that require users to traverse the university campus to meet the criteria   
Points for completing and winning challenges  
Leaderboard  
Stickers and tags    
Expansion of challenges e.g. utilising AR  
Expansion of CSS

Requirements
-------------

Python 3.9.0 or later  

django library:  
	pip install django  
exif library:  
	pip install exif  
geopy library:  
	pip install geopy  
	  
If you wish to host a dedicated server to run the web-app off of, you will also need a hosting service e.g. Google Cloud SDK  

Running the Project:
--------------------

Firstly, download the project and the dependencies.  
To run the project locally, open a command line/terminal at the outermost mysite folder of the project directory. Then, run the following command:  
	python manage.py runserver  
A local server will be established.  

To deploy the project onto a Google Cloud server, use the following guide:  
	https://cloud.google.com/python/django/appengine  
	  
Once the project is running, users will be able to navigate to the server URL and access the web-app without needing to install anything.  

License
-------

<img alt="GitHub" src="https://img.shields.io/github/license/js1294/ECM-2434-Group-Software-Engineering-Project">

Other info
----------

Commit Activity:  
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/y/js1294/ECM-2434-Group-Software-Engineering-Project">  
  
Code Size:  
<img alt="GitHub code size" src="https://img.shields.io/github/languages/code-size/js1294/ECM-2434-Group-Software-Engineering-Project">  
  
Pull Requests:  
<img alt="GitHub pull requests" src="https://badgen.net/github/prs/js1294/ECM-2434-Group-Software-Engineering-Project">  
	

