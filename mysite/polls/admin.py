from django.contrib import admin

from .models import Question, Image

admin.site.register(Question)
admin.site.register(Image)
