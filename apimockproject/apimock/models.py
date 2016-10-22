from __future__ import unicode_literals


from django.db import models
import jsonfield


# Create your models here.

class MockedApi(models.Model):

    HTTP_Methods = (
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("HEAD", "HEAD"),
    )
    url_to_api = models.CharField(max_length=200)
    mocked_return_value = jsonfield.JSONField()
    http_method = models.CharField(choices=HTTP_Methods, default="GET", max_length=6)
    # Testowe


    def mocked_dynamic_GET(self, **kwargs):
      return kwargs

    def mocked_dynamic_POST(self, **kwargs):
      return kwargs

    def __str__(self):

      return self.url_to_api
