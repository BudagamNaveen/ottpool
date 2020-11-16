from django.contrib import admin
from .models import Ott_titles,Ott_screens,pooled_members

# Register your models here.
admin.site.register(Ott_titles)
admin.site.register(Ott_screens)
admin.site.register(pooled_members)