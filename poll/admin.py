from django.contrib import admin
from poll.forms import ChoiceForm

from .models import Poll, CategoryGroup, Category, Choice, Vote

@admin.register(Choice)
class Choice(admin.ModelAdmin):
    form = ChoiceForm

admin.site.register(Poll)
admin.site.register(CategoryGroup)
admin.site.register(Category)
#admin.site.register(Choice)
admin.site.register(Vote)