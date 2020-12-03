from django.contrib import admin

# Register your models here.
from .models import FCI_regional_office
from .models import godowns

admin.site.register(FCI_regional_office)
admin.site.register(godowns)