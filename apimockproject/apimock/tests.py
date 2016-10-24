import json

from django.test import TestCase
from apimock.models import MockedApi
from django.test.client import Client


class MockedApiGETTestCase(TestCase):

    def setUp(self):
        MockedApi.objects.create(url_to_api="^mocked_get$",
                                 mocked_return_value={"value": "testValue"})

    def test_mocked_get_list_template(self):
        """check if simple mocked apis template could be returned"""
        c = Client()
        response = c.get("/apimock/mocked/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Here is the list of all possible apis:",
                      response.content)
        self.assertIn("^mocked_get$", response.content)

    def test_mocked_get_simpleHtml(self):
        """check if simple mocked get could be returned"""
        c = Client()
        response = c.get("/apimock/mocked/mocked_get")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<table border="1"><tr><th>value</th><td>testValue</td></tr></table>', response.content)

    def test_mocked_get_json_format(self):
        """check if simple mocked json get could be returned"""
        c = Client()
        response = c.get("/apimock/mocked/mocked_get?format=json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"value": "testValue"}', response.content)

    def test_custom_404(self):
        """check if proper 404 is returned"""
        c = Client()
        response = c.get("/apimock/mocked/non_exsitng-url")
        self.assertEqual(response.status_code, 404)
        self.assertEqual('MockedApi 404', response.content)
