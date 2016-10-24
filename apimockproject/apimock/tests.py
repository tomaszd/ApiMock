import json

from django.test import TestCase
from apimock.models import MockedApi
from django.test.client import Client


class MockedApiGETTestCase(TestCase):

    def setUp(self):
        MockedApi.objects.create(url_to_api="^mocked_get$",
                                 mocked_return_value={"value": "testValue"},
                                 http_method="GET",
                                 Error_403="wrong used test Data")

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
        """Check if proper custom 404 is returned"""
        c = Client()
        response = c.get("/apimock/mocked/non_exsitng-url")
        self.assertEqual(response.status_code, 404)
        self.assertEqual('MockedApi 404', response.content)

    def test_custom_404(self):
        """Check if proper custom 404 is returned"""
        c = Client()
        response = c.get("/apimock/mocked/non_exsitng-url")
        self.assertEqual(response.status_code, 404)
        self.assertEqual('MockedApi 404', response.content)

    def test_custom_403(self):
        """Check if proper 403 is returned when user is using
           e.g. POST for apis that are created for service GET"""
        c = Client()
        response = c.post("/apimock/mocked/mocked_get", data={"post": "data"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual("wrong used test Data", response.content)


class MockedApiGETTestCaseParam(TestCase):

    def setUp(self):
        MockedApi.objects.create(url_to_api="^api/account/(?P<account>\d+)/$",
                                 mocked_return_value={"amount": "10PLN"},
                                 http_method="GET")

    def test_mocked_get_api(self):
        """check if simple mocked apis template could be returned"""
        c = Client()
        response = c.get("/apimock/mocked/api/account/154/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<table border="1"><tr><th>amount</th><td>10PLN</td></tr></table>', response.content)
        response2 = c.get("/apimock/mocked/api/account/187/")
        self.assertEqual(response2.status_code, 200)
        self.assertIn(
            '<table border="1"><tr><th>amount</th><td>10PLN</td></tr></table>', response2.content)
