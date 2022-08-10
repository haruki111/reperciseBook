from django.contrib import admin
from .models import Tag, Book, Section, Problem
# Register your models here.
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(Section)
admin.site.register(Problem)
