import logging
import re
import requests

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import MockedAPiValue
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


def get_cached_updatable_response(request, _url):
    if request.method == "GET":

        if MockedAPiValue.objects.filter(exact_url=_url):
            cached = MockedAPiValue.objects.get(exact_url=_url)
            if request.GET.get('format') == "json":
                _response = JsonResponse(
                    cached.mocked_return_value, safe=False)
            else:
                _response = HttpResponse(cached.simpleHTML)
            return _response


def set_updatable_mocked_response(request, _url):
    if request.method == "POST":
        if MockedAPiValue.objects.filter(exact_url=_url):
            cached = MockedAPiValue.objects.get(exact_url=_url)
            cached.mocked_return_value = request.POST.dict()
            cached.save()
            _response = JsonResponse(
                cached.mocked_return_value, safe=False)
            return _response


@csrf_exempt
def mocked_apis(request):
    """request.path
     u'/apimock/mocked/csdfdsfdsfsdfsdfs'"""
    _request = request
    _url = request.path.replace("/apimock/mocked/", '')
    for mocked_api in MockedApi.objects.all():
        if re.match(mocked_api.url_to_api, _url):
            # if mocked_api.http_method==request.method:
            # Get instanlty the cached version that is volatiole and could be
            # changed:

            if mocked_api.easily_updatable:
                _response = set_updatable_mocked_response(request, _url)
                if _response:
                    return _response

            # check if there is ready value cached for specific url
            _response = get_cached_updatable_response(request, _url)
            if _response:
                return _response

            _callback_success = True

            if request.method != mocked_api.http_method:
                return HttpResponse(mocked_api.Error_403, status=403)
            # special case for complicated logic of posts
            if mocked_api.behavior_after_post and request.method == "POST":
                exec(mocked_api.behavior_after_post)

            _response = ""
            try:
                if request.GET.get('format') == "json":
                    _response = JsonResponse(
                        mocked_api.mocked_return_value, safe=False)
                else:
                    _response = HttpResponse(mocked_api.simpleHTML)
                return _response
            except:
                # wrong used API
                _callback_success = False
                _response = HttpResponse(mocked_api.Error_403, status=403)
                return _response
            finally:
                if _callback_success:
                    MockedAPiValue.objects.create(original_api=mocked_api,
                                                  mocked_return_value=mocked_api.mocked_return_value,
                                                  exact_url=_url)

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
