from django.contrib import admin

from .models import Restaurent, User, Item
# Register your models here.
admin.site.register(User)
admin.site.register(Restaurent)
admin.site.register(Item)


