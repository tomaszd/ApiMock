from django.http import HttpResponse
from django.shortcuts import render

from .models import MockedApi

# Create your views here.
def home(request):

    return HttpResponse("Welcome in ApiMock")



def mocked(request):
    mocked_apis = MockedApi.objects.all()
    cos = ""
    for i in mocked_apis:
      cos += str(i) + "</br>"
      print "i", i

    return HttpResponse("Here is the URL to test all mocked urls </br> " + str(cos))


def mocked_apis(request):
   """request.path
    u'/apimock/mocked/csdfdsfdsfsdfsdfs'"""
   maly_url = request.path.replace("/apimock/mocked/", '')
   print "request", request
   for mocked_api in  MockedApi.objects.all():
     if maly_url == mocked_api.url_to_api:
       print "co sue dzeje ?"
       return HttpResponse(mocked_api.mocked_return_value)

   return HttpResponse("witaj kolezko! w mocked apis wszedles na adres :v " + str(request.path))
   return HttpResponse("witaj kolezko! ")
