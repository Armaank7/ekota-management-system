from django.contrib import admin
from .models import Staff, Player

# Register staff and player models so they can be managed in admin
admin.site.register(Staff)
admin.site.register(Player)
