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
    mocked_return_value = jsonfield.JSONField(
        default=json.dumps({"message":
                            "Please enter json as mocked value. please change that setting"}))
    http_method = models.CharField(
        choices=HTTP_Methods, default="GET", max_length=6)
    # custom error message for api for wrong usage
    error_403 = models.CharField(max_length=200, default="wrong used Data!")
    error_400 = models.CharField(max_length=200, default="BAD request for this api")
    # if easily_updatable is set=>MockedApiResult could be easily manipulated
    # via POST .PATCH etc
    easily_updatable = models.BooleanField(default=False)
    # Needed for mock complicated behavior of api
    behavior_after_post = models.CharField(
        max_length=1000, null=True, blank=True)

    @property
    def simpleHTML(self):
        """This is generating simplehtml from json value"""
        try:
            return json2html.convert(json=self.mocked_return_value, safe=False)
        except:
            return "<p>" + str(self.mocked_return_value) + "</p>"

    @classmethod
    def Error404(self):
        return "MockedApi 404"

    def __str__(self):
        return self.url_to_api + self.http_method


class MockedApiResult(models.Model):

    """Defines the URL result. Needed for storing info about api call"""
    original_api = models.ForeignKey(MockedApi)
    mocked_return_value = jsonfield.JSONField(
        default={"message": "This is storing the volatile data for api calls"})
    # needed to differ for different URIS e.g. api/account/123/ vs
    # api/account/124/
    exact_url = models.CharField(max_length=200)
    callback_success = models.BooleanField(default=False)

    def __str__(self):
        return "_".join([self.exact_url,
                         str(self.callback_success),
                         str(self.mocked_return_value)])


class MockedAPiValue(models.Model):

    """Whenever an api is called that match the url. The volatile stored value
    MockedAPiValue is created. it is used then to store the results and
    manipulate the data. This is an instance of proper MockedApiURLs.

    needed for cases like
    http://api/account/123/product_buy/ ,data="price":"10,
    then to decrease http://api/account/123/ user money.
    """
    original_api = models.ForeignKey(MockedApi)
    exact_url = models.CharField(max_length=200)
    mocked_return_value = jsonfield.JSONField(
        default=json.dumps({}))

    @property
    def simpleHTML(self):
        """This is generating simplehtml from json value"""
        try:
            return json2html.convert(json=self.mocked_return_value, safe=False)
        except:
            return "<p>" + str(self.mocked_return_value) + "</p>"

    def set_new_mocked_value(self, value):
        self.mocked_return_value = value

    def __str__(self):
        return "<" + self.exact_url + ":" + str(self.mocked_return_value) + ">"
