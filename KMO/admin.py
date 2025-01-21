from django.contrib import admin
from .models import Kmo, Kmodet, Kmo_members, Kmo_responsible


admin.site.register(Kmo)
admin.site.register(Kmodet)
admin.site.register(Kmo_members)
admin.site.register(Kmo_responsible)
