from django.contrib import admin
from blog.models import *
# Register your models here.

admin.site.register(Task)
admin.site.register(History)
admin.site.register(Old)
admin.site.register(Notes)
admin.site.register(IpInfo)