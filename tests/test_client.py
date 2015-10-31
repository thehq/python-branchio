import unittest
import branchio
import os
import mock


class ClientCheckParamTests(unittest.TestCase):

    def setUp(self):
        self.branch_client = branchio.Client(None)
        self.params = {}

    def test_optional(self):

        self.branch_client._check_param("test", None, self.params)
        self.assertFalse("test" in self.params)

        with self.assertRaises(Exception) as context:
            self.branch_client._check_param("test", None, self.params, optional=False)

    def test_max_length(self):

        self.branch_client._check_param("test", "test_length", self.params, max_length=50)
        self.assertTrue("test" in self.params)

        with self.assertRaises(Exception) as context:
            self.branch_client._check_param("test", "test_length", self.params, max_length=5)

    def test_type(self):

        self.branch_client._check_param("test", "test_length", self.params, type=str)
        self.assertTrue("test" in self.params)

        with self.assertRaises(Exception) as context:
            self.branch_client._check_param("test", "test_length", self.params, type=list)

    def test_gte(self):

        # Ignored unless it is an integer
        self.branch_client._check_param("test", "string", self.params, gte=5)
        self.assertTrue("test" in self.params)

        self.params = {}

        self.branch_client._check_param("test", 10, self.params, gte=5)
        self.assertTrue("test" in self.params)

        with self.assertRaises(Exception) as context:
            self.branch_client._check_param("test", 10, self.params, gte=15)

    def test_lte(self):

        # Ignored unless it is an integer
        self.branch_client._check_param("test", "string", self.params, lte=5)
        self.assertTrue("test" in self.params)

        self.params = {}

        self.branch_client._check_param("test", 10, self.params, lte=15)
        self.assertTrue("test" in self.params)

        with self.assertRaises(Exception) as context:
            self.branch_client._check_param("test", 10, self.params, lte=5)

    def test_sub_type(self):

        self.branch_client._check_param("test", ["something", "something else"], self.params, sub_type=str, sub_max_length=15)
        self.assertTrue("test" in self.params)

        with self.assertRaises(Exception) as context:
            self.branch_client._check_param("test", ["something", "something else"], self.params, sub_type=str, sub_max_length=5)

    def test_sub_type_no_name_or_params(self):

        no_exception = True
        try:
            self.branch_client._check_param(["something", "something else"], type=list, sub_type=str)
        except Exception:
            no_exception = False

        self.assertTrue(no_exception)


class ClientCheckApiTests(unittest.TestCase):

    def get_client(self, return_value):
        branch_key = os.environ.get('BRANCH_IO_KEY')
        if branch_key is None:
            print "WARNING!  Environment variable 'BRANCH_IO_KEY' is not defined." + \
                  "  Branch API Tests will return stubbed responses."
            branch_key = "FAKE KEY"
            branchio.Client.make_api_call = mock.MagicMock(return_value=return_value)

        return branchio.Client(branch_key)

    def test_create_deep_link_skip_api(self):
        client = self.get_client(None)
        params = client.create_deep_link_url(
            data={
                branchio.DATA_BRANCH_IOS_URL: "https://www.google.com",
                "custom": "payload"
            },
            channel="facebook",
            skip_api_call=True
        )

        self.assertTrue("data" in params)
        self.assertEqual(params["data"][branchio.DATA_BRANCH_IOS_URL], "https://www.google.com")
        self.assertEqual(params["data"]["custom"], "payload")
        self.assertEqual(params["channel"], "facebook")

    def test_create_deep_link(self):
        client = self.get_client({"url": "https://www.example.com/"})
        response = client.create_deep_link_url(
            data={
                branchio.DATA_BRANCH_IOS_URL: "https://www.google.com",
                "custom": "payload"
            },
            channel="facebook",
            tags=["signup"]
        )

        self.assertTrue(branchio.RETURN_URL in response)

    def test_create_deep_links(self):
        client = self.get_client([{"url": "https://www.example.com/"}, {"url": "https://www.example.com/"}])
        params1 = client.create_deep_link_url(
            data={
                branchio.DATA_BRANCH_IOS_URL: "https://www.google.com",
                "custom": "payload"
            },
            channel="facebook",
            tags=["signup"],
            skip_api_call=True
        )
        params2 = client.create_deep_link_url(
            data={
                branchio.DATA_BRANCH_IOS_URL: "https://www.google.com",
                "custom": "payload"
            },
            channel="facebook",
            tags=["signup"],
            skip_api_call=True
        )

        response = client.create_deep_linking_urls([params1, params2])

        self.assertTrue(branchio.RETURN_URL in response[0])
        self.assertTrue(branchio.RETURN_URL in response[1])
