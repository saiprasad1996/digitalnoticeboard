from django.contrib import admin
from .models import User,Posts,Department
# Register your models here.

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Department)