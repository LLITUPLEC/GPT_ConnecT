# from django.contrib import admin
# from .models import * #Bs_depowner, Bs_department, Bs_position
#
#
# admin.site.register(Bs_depowner)
# admin.site.register(Bs_department)
# admin.site.register(Bs_position)
# admin.site.register(Bs_RWStation)

from django.contrib import admin
from django.db.models import Model
from . import models
from django.db.models.base import ModelBase

for e in dir(models):
    if isinstance(getattr(models, e), ModelBase) and issubclass(getattr(models, e), Model):
        admin.site.register(getattr(models, e))