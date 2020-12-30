from django.contrib import admin
from .models import *


# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question']}),
                 ('User', {'fields': ['author']}),
                 (None, {'fields': ['voted_users']}),
                 (None,{'fields':['value']}),
                 ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}), ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment)
admin.site.register(Likee)
