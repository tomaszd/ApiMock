import json

from django.db import models
from json2html import json2html
import jsonfield


# Create your models here.
class MockedApi(models.Model):
    """Defines the URL pattern Plus behavior of mocked Api"""
    HTTP_Methods = (
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("HEAD", "HEAD"),
        ("PATCH", "PATCH"),
        ("DELETE", "DELETE")
    )
    url_to_api = models.CharField(max_length=200)
    mocked_return_value = jsonfield.JSONField(default={"message":"Please enter proper json return Value For this Api"})
    http_method = models.CharField(choices=HTTP_Methods, default="GET", max_length=6)

    @property
    def simpleHTML(self):
      return json2html.convert(json=self.mocked_return_value)

    def __str__(self):
      return self.url_to_api + self.http_method


class MockedApiResult(models.Model):
    """Defines the URL result. Needed for storing info about api call"""
    original_api = models.ForeignKey(MockedApi)
    mocked_return_value = jsonfield.JSONField(default={"message":"This is storing the volatile data for api calls"})
    # needed to differ for different URIS e.g. api/account/123/ vs api/account/124/
    exact_url = models.CharField(max_length=200)
    callback_success = models.BooleanField(default=False)

    def __str__(self):
      return self.exact_url + str(self.mocked_return_value)
