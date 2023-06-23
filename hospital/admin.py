from django.contrib import admin
from .models import Hospital, Major, School, Doctor


admin.site.register(Hospital)
admin.site.register(Major)
admin.site.register(Doctor)
admin.site.register(School)
