import logging
import re

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from .models import MockedApi
from .models import MockedApiResult

logger = logging.getLogger(__name__)

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

def mocked_param(request, *args, **kwargs):
    print "request.GET", str(request.GET)
    return HttpResponse("witamy w URL z paramem" + \
                        str(args) + str(kwargs) + str(request.GET.get('format')))



def mocked_apis(request):
   """request.path
    u'/apimock/mocked/csdfdsfdsfsdfsdfs'"""
   _url = request.path.replace("/apimock/mocked/", '')
   for mocked_api in  MockedApi.objects.all():
     if re.match(mocked_api.url_to_api, _url):

       # todo dodac logowanie
       logger.info('Log Info')
       logger.critical("asdasa")
       logger.debug('Usage of API: {} for url {} '.format(mocked_api, _url))
       # if mocked_api.http_method==request.method:
       _callback_success = True
       if request.method != mocked_api.http_method:
         return HttpResponse(mocked_api.Error403, status=403)

       try:
         if request.GET.get('format') == "json":
           return JsonResponse(mocked_api.mocked_return_value)
         return HttpResponse(mocked_api.simpleHTML)
       except:
         # wrong used API
         return HttpResponse(mocked_api.Error403, status=403)
         _callback_success = False
       finally:
         MockedApiResult.objects.create(original_api=mocked_api,
                                        mocked_return_value=mocked_api.mocked_return_value,
                                        exact_url=_url,
                                        callback_success=_callback_success
                                        )
   return HttpResponse(MockedApi.Error404(), status=404)
