import ast
import logging
import re
import requests

from django.http import HttpResponse
from django.http import JsonResponse
from django.http import QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.urls import reverse


from .models import MockedAPiValue
from .models import MockedApi
from .models import MockedApiResult


logger = logging.getLogger(__name__)


def home(request):
    return HttpResponse("Welcome in ApiMock.Check the used APIs in {} :"
                        " Use APIs by entering url : {} ".format(reverse('mocked'),
                                                                 reverse('mocked_apis')))


def mocked(request):
    """List of all added apis so far"""
    mocked_apis = MockedApi.objects.all()
    return render(request,
                  'apimock/list.html',
                  {"mocked_apis": mocked_apis}
                  )


def get_cached_updatable_response(request, _url):
    """Get the mocked value for specific URL"""
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
    """Set Mocked Value for easily_updated URLs"""
    if request.method == "POST":
        if MockedAPiValue.objects.filter(exact_url=_url):
            cached = MockedAPiValue.objects.get(exact_url=_url)
            cached.mocked_return_value = request.POST.dict()
            cached.save()
            _response = JsonResponse(
                cached.mocked_return_value, safe=False)
            return _response


def patch_updatable_mocked_response(request, _url):
    """PATCH Mocked Value for easily_updated URLs"""
    if request.method == "PATCH":
        if MockedAPiValue.objects.filter(exact_url=_url):
            cached = MockedAPiValue.objects.get(exact_url=_url)
            # import pdb
            # pdb.set_trace()
            # Note standard QueryDict(request.body).dict() not working in test.py
            # but working  on production
            parsed_patch_dict = ast.literal_eval(request.body)
            if cached.mocked_return_value:
                cached.mocked_return_value.update(parsed_patch_dict)
            else:
                cached.mocked_return_value = parsed_patch_dict
            cached.save()
            _response = JsonResponse(
                cached.mocked_return_value, safe=False)
            return _response


def check_permission(request):
    """basic algorithm who can enter use mocked APIs"""
    if request.user:
        if request.user.is_staff or "API_runners" in request.user.groups.all():
            return True
    return HttpResponse("You are not an admin or member of 'API_runners' group",
                        status=404)


def notify_users(request):
    """Function to notify users that api was called.

    as for now -> users that belong to "API_runners"
    are informed that api was used.

    Could be extended later for some real notification/mails etc
    as for now the basic console output is made.
    Also note more info could be added here e.g. POST params etc """
    for user in User.objects.filter(groups__name='API_runners'):
        msg = "User {} was informed about request {}".format(
            user.username, request)
        print msg
        logger.debug(msg)


@csrf_exempt
def mocked_apis(request):
    """The main and the most important part
    When user is making request to that view the logic of view is selecting 
    which exactly API was called.

    When the request path matches the Api patterns -> there is a special 
    logic for that request

    Note majority of API could be set with easily_updatable=True paramteter 
    to drastically simplify behavior -> e.g. users could get /post data
    to it directly."""
    check_permission(request)
    _url = request.path.replace("/apimock/mocked/", '')
    for mocked_api in MockedApi.objects.all():
        if re.match(mocked_api.url_to_api, _url):
            # Notify about request all the users that are interested in it
            notify_users(request)

            # Get instantly the instances it API urls
            # so for example instances for specific URL like /api/account/12/
            if mocked_api.easily_updatable:
                # service possible POST
                _response = set_updatable_mocked_response(request, _url)
                if _response is not None:
                    return _response
                # service possible PATCH
                _response = patch_updatable_mocked_response(request, _url)
                if _response is not None:
                    return _response

            # service GET
            # check if there is ready value for mocked API
            _response = get_cached_updatable_response(request, _url)
            if _response is not None:
                return _response

            _callback_success = True

            if request.method != mocked_api.http_method:
                return HttpResponse(mocked_api.error_403, status=403)
            # special case for complicated logic of posts
            if mocked_api.behavior_after_post and request.method == "POST":
                pass
                # so for example to remove money from api/account/233
                # after api/account/233/product_buy/ Many posibilites
                # discarder for now as not properly tested -this is a nice
                # field to improve the app
                # Idea is to make python code and actions as described in
                # behavior_after_post field in MockedApi model.
                # magicline =
                # exec(mocked_api.behavior_after_post)

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
                _response = HttpResponse(mocked_api.error_403, status=403)
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
                # storing the results of api calls which could be used
                # later by some logic to repeat calls / . Please note they could
                # be cleaned up later in some Celery /periodic task or by cron
                # jobs.
                MockedApiResult.objects.create(
                    original_api=mocked_api,
                    mocked_return_value=mocked_api.mocked_return_value,
                    exact_url=_url,
                    callback_success=_callback_success
                )
    return HttpResponse(MockedApi.Error404(), status=404)
