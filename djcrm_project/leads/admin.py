from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Lead)
admin.site.register(Organisation)
