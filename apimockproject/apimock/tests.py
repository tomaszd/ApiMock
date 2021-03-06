import json
import unittest

from apimock.models import MockedApi
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


class MockedApiGETTestCase(TestCase):

    def setUp(self):
        MockedApi.objects.create(url_to_api="^mocked_get$",
                                 mocked_return_value={"value": "testValue"},
                                 http_method="GET",
                                 error_403="wrong used test Data")

    def test_mocked_get_list_template(self):
        """check if simple mocked apis template could be returned"""
        c = Client()
        response = c.get(reverse('mocked'))
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


class MockedApiPOSTTestCase(TestCase):

    def setUp(self):
        MockedApi.objects.create(url_to_api="^mocked_post$",
                                 mocked_return_value={
                                     "value": "test_return_value_for_post"},
                                 http_method="POST",
                                 error_403="wrong used test Data,this is api for POST")

    def test_mocked_get_list_template(self):
        """check if simple mocked apis template could be returned"""
        c = Client()
        response = c.get(reverse('mocked'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Here is the list of all possible apis:",
                      response.content)
        self.assertIn("^mocked_post$", response.content)

    def test_mocked_post_simpleHtml(self):
        """check if simple mocked post simplethml  could be returned"""
        c = Client()
        response = c.post("/apimock/mocked/mocked_post", data={"key": "value"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<table border="1"><tr><th>value</th><td>test_return_value_for_post</td></tr></table>', response.content)

    def test_mocked_post_json_format(self):
        """check if simple mocked json format get could be returned for post """
        c = Client()
        response = c.post("/apimock/mocked/mocked_post?format=json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            '{"value": "test_return_value_for_post"}', response.content)

    def test_custom_403(self):
        """check if proper 403 is returned when user use GET for post mocked apis"""
        c = Client()
        response = c.get("/apimock/mocked/mocked_post?format=json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            "wrong used test Data,this is api for POST", response.content)


class EasyUpdateTestCase(TestCase):

    def setUp(self):
        MockedApi.objects.create(url_to_api="^api/account/(?P<account>\d+)/$",
                                 mocked_return_value={
                                     "value": "There is a product bought"},
                                 http_method="GET",
                                 easily_updatable=True,
                                 error_403="Send me Money")

    def test_mocked_api_set_value(self):
        """check if using PostApi is possible"""
        c = Client()
        response = c.get("/apimock/mocked/api/account/45/?format=json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"value": "There is a product bought"}',
                      response.content)
        response = c.post(
            "/apimock/mocked/api/account/45/?format=json", data={"PLN": 100})
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"PLN": "100"}', response.content)
        response = c.get("/apimock/mocked/api/account/45/?format=json")
        self.assertIn('{"PLN": "100"}', response.content)


class EasyUpdatePATCHTestCase(TestCase):
    """Tests for PATCH behavior for easily updated apis"""
    patch_url = "/apimock/mocked/api/account/45/?format=json"

    def setUp(self):
        MockedApi.objects.create(url_to_api="^api/account/(?P<account>\d+)/$",
                                 mocked_return_value={
                                     "account": 157},
                                 http_method="GET",
                                 easily_updatable=True,
                                 error_403="Wrong Case please use PATCH better")

    def test_mocked_api_set_new_value(self):
        """check if using PostApi is possible"""
        c = Client()
        response = c.get(self.patch_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"account": 157}',
                      response.content)
        response = c.patch(
            self.patch_url, data={"PLN": 20, "EURO": 20})
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"PLN": 20, "account": 157, "EURO": 20}',
                      response.content)
        response = c.get(self.patch_url)
        self.assertIn('{"PLN": 20, "account": 157, "EURO": 20}',
                      response.content)

    def test_mocked_api_update_value(self):
        """check if using PostApi is possible"""
        c = Client()
        patch_url = "/apimock/mocked/api/account/45/?format=json"
        response = c.get(self.patch_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"account": 157}',
                      response.content)
        response = c.patch(self.patch_url, data={"account": 456})
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"account": 456}', response.content)
        response = c.get(self.patch_url)
        self.assertIn('{"account": 456}', response.content)
        response = c.patch(self.patch_url, data={"account": 654})
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"account": 654}', response.content)
        response = c.get(self.patch_url)
        self.assertIn('{"account": 654}', response.content)


class PostLogicTestCase(TestCase):

    """Needed for  testing complicated logic of API mocks """

    def setUp(self):
        MockedApi.objects.create(
            url_to_api="^api/account/(?P<account>\d+)/product_buy/$",
            mocked_return_value="product was bought",
            http_method="POST",
            behavior_after_post="price=int(request.POST['price']);account_url=request.get_raw_uri().split('product_buy')[0];old_account=int(requests.get(account_url+'?format=json').json()['account']);new_account=old_account-price;requests.post(account_url+'?format=json',data={'account':str(new_account)})",
            error_403="Send me Money")

        MockedApi.objects.create(url_to_api="^api/account/(?P<account>\d+)/$",
                                 mocked_return_value={
                                     "account": "555"},
                                 http_method="GET",
                                 easily_updatable=True,
                                 error_403="Send me Money")

    @unittest.skip("I don't want to run this test yet complicated api should be done better")
    def test_mocked_api_set_value(self):
        """check if using PostApi is possible
        It should create new values in old api"""
        c = Client()
        response = c.get("/apimock/mocked/api/account/45/?format=json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"account": "555"}', response.content)
        response = c.post(
            "/apimock/mocked/api/account/45/product_buy/?format=json", data={"price": 100})
        self.assertEqual(response.status_code, 200)
        self.assertIn("product was bought", response.content)
        response = c.get("/apimock/mocked/api/account/45/?format=json")
        self.assertIn({"account": "455"}, response.content)
