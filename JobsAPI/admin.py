from django.contrib import admin
from .models import  WorkExperience, Education, Language, Certification, Application,Job

admin.site.register(Job)
admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(Language)
admin.site.register(Certification)
admin.site.register(Application)
