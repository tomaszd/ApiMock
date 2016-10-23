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
        ("PATCH", "PATCH"),
        ("DELETE", "DELETE")
    )
    url_to_api = models.CharField(max_length=200)
    mocked_return_value = jsonfield.JSONField()
    http_method = models.CharField(choices=HTTP_Methods, default="GET", max_length=6)

    def create_response(self, *args, **kwargs):
      """Function To create a logic for mocking return value"""
      print "Response! kwargs", kwargs
      final_return_value = {}
      for kw in kwargs:
        print kw

    def __str__(self):

      return self.url_to_api + self.http_method
