from django.http import HttpResponse
import datetime
from .forms import ImagefieldForm
from .models import Image
from django.shortcuts import render, redirect

#placeholder function to return location and date taken from metadata
def get_img_metadata(img):
	return '1.001 1.002', datetime.datetime.now()

def not_authenticated(request): 
    return HttpResponse('you must be logged in to upload an image')

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def upload_image(request): 
    context = {}
    #once the request has been made, process it
    if not request.user.is_authenticated:
    	return redirect('not_authenticated')
    if request.method == "POST": 
        form = ImagefieldForm(request.POST, request.FILES) 
        if form.is_valid():
        	#santize inputs
            name = form.cleaned_data.get("name")
            desc = form.cleaned_data.get("description") 
            img = form.cleaned_data.get("image")
            gps, date_taken = get_img_metadata(img)
            #create the table object
            obj = Image.objects.create( 
                                 title = name, 
                                 description = desc, 
                                 img = img, 
                                 gps_coordinates = gps, 
                                 taken_date = date_taken 
                                 ) 
            obj.save() 
            print(obj)
            return redirect('successful_upload')  
    #display the image upload form
    else: 
        form = ImagefieldForm()
        context['form'] = form
        return render( request, "uploadfile.html", context) 

def successful_upload(request): 
    return HttpResponse('image successfully uploaded')
