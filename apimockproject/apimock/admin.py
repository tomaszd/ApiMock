from apimock.models import MockedApi
from apimock.models import MockedApiResult

from django.contrib import admin


# Register your models here.
admin.site.register(MockedApi)
admin.site.register(MockedApiResult)