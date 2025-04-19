from django.contrib import admin
from .models import Book, AccessRequest 

# Register your models here.
admin.site.register(Book)
admin.site.register(AccessRequest)
