from django.contrib import admin
from app.models import Profiles, Tags, Answers, Questions, Likequestion, Likeanswers

# Register your models here.

admin.site.register(Profiles)
admin.site.register(Tags)
admin.site.register(Answers)
admin.site.register(Questions)
admin.site.register(Likequestion)
admin.site.register(Likeanswers)
