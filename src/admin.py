from django.contrib import admin

from src.models import Mobile, Laptop, TV
from import_export.admin import ImportExportModelAdmin


# Register your models here.


@admin.register(Mobile)
class CustomerClass(ImportExportModelAdmin):
    pass


@admin.register(Laptop)
class LaptopClass(ImportExportModelAdmin):
    pass


@admin.register(TV)
class TVClass(ImportExportModelAdmin):
    pass
