import logging
import re

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from .models import MockedApi
from .models import MockedApiResult


logger = logging.getLogger(__name__)


def home(request):

    return HttpResponse("Welcome in ApiMock")


def mocked(request):
    """List of all added apis so far"""
    mocked_apis = MockedApi.objects.all()
    return render(request,
                  'apimock/list.html',
                  {"mocked_apis": mocked_apis}
                  )


def mocked_apis(request):
    """request.path
     u'/apimock/mocked/csdfdsfdsfsdfsdfs'"""
    _url = request.path.replace("/apimock/mocked/", '')
    for mocked_api in MockedApi.objects.all():
        if re.match(mocked_api.url_to_api, _url):
            # if mocked_api.http_method==request.method:
            _callback_success = True
            if request.method != mocked_api.http_method:
                return HttpResponse(mocked_api.Error_403, status=403)
            _response = ""
            try:
                if request.GET.get('format') == "json":
                    _response = JsonResponse(
                        mocked_api.mocked_return_value, safe=False)
                    return _response
                else:
                    _response = HttpResponse(mocked_api.simpleHTML)
                    return _response
            except:
                # wrong used API
                _callback_success = False
                _response = HttpResponse(mocked_api.Error_403, status=403)
                return _response
            finally:
                logger.debug(
                    "Usage of API: {} for url {} :Response_was: {},_status={}"
                    " ,response_status= {} ".format(mocked_api,
                                                    _url,
                                                    repr(_response),
                                                    _callback_success,
                                                    _response.status_code))
                MockedApiResult.objects.create(
                    original_api=mocked_api,
                    mocked_return_value=mocked_api.mocked_return_value,
                    exact_url=_url,
                    callback_success=_callback_success
                )
    return HttpResponse(MockedApi.Error404(), status=404)
