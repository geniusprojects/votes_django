from django.contrib import admin

from .models import Poll, CategoryGroup, Category, Choice, Vote

admin.site.register(Poll)
admin.site.register(CategoryGroup)
admin.site.register(Category)
admin.site.register(Choice)
admin.site.register(Vote)