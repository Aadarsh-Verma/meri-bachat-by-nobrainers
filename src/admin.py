from django.contrib import admin

from src.models import Mobile
from import_export.admin import ImportExportModelAdmin


# Register your models here.


@admin.register(Mobile)
class CustomerClass(ImportExportModelAdmin):
    pass


