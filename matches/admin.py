from django.contrib import admin
from .models import Match, MatchAppearance

# Register match models so they can be managed in admin
admin.site.register(Match)
admin.site.register(MatchAppearance)
