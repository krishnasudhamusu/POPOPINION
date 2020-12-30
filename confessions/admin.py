from django.contrib import admin
from .models import Confession,Comment,Like

# Register your models here.
admin.site.register(Confession)
admin.site.register(Comment)
admin.site.register(Like)
