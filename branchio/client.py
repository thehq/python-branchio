import json
import sys
try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen

if sys.version_info < (3,):
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes


class Client(object):

    BRANCH_BASE_URI = "https://api.branch.io"

    def __init__(self, branch_key, verbose=False):
        """
        Initializes the Adapter
        :param branch_key: The key used to access the branch API
        :param verbose: True if you want verbose statements
        :return: Nothing
        """
        self.branch_key = branch_key
        self.verbose = verbose

    @classmethod
    def _check_param(cls, name=None, value=None, params=None, optional=True, max_length=None, type=None,
                     gte=None, lte=None, sub_max_length=None, sub_type=None):
        """
        This checks the value for different type, max length, etc.  If all of the checks pass, then the value is placed
        in the params bucket
        :param name: The name of the parameter
        :param value: The value of param
        :param params: The dictionary where the param should go if all of the checks pass
        :param optional: True (default) if the value is optional
        :param max_length: The maximum length of the param
        :param type: The type of the param
        :param gte: Greater than or equal to this number
        :param lte: LEss than or equal to this number
        :param sub_max_length: The sub maximum length (for iterables)
        :param sub_type: The sub type (for iterables)
        :return: Nothing
        """
        assert params is None or isinstance(params, dict)

        if value is None:
            if not optional:
                assert value is not None
        else:
            if type is not None:
                assert isinstance(value, type)
            if max_length is not None:
                assert len(value) <= max_length
            if isinstance(value, list):
                for sub_value in value:
                    if sub_type is not None:
                        assert isinstance(sub_value, sub_type)
                    if sub_max_length is not None:
                        assert len(sub_value) <= sub_max_length
            if isinstance(value, dict):
                for key in value:
                    sub_value = value[key]
                    if sub_type is not None:
                        assert isinstance(sub_value, sub_type)
                    if sub_max_length is not None:
                        assert len(sub_value) <= sub_max_length
            if isinstance(value, int):
                if gte is not None:
                    assert value >= gte
                if lte is not None:
                    assert value <= lte

            if name is not None and params is not None:
                params[name] = value

    def create_deep_link_url(self, data=None, alias=None, type=0, duration=None, identity=None, tags=None,
                             campaign=None, feature=None, channel=None, stage=None, skip_api_call=False):
        """
        Creates a deep linking url

        See the URL https://dev.branch.io/references/http_api/#creating-a-deep-linking-url

        You can also use this method to bulk create deep link by setting "skip_api_call=True" and using the parameters
        returned by the method as an array and call "create_deep_linking_urls"

        :return: params or the response
        """
        url = "/v1/url"
        method = "POST"
        params = {}

        # Check Params
        self._check_param("data", data, params, type=dict)
        self._check_param("alias", alias, params, type=(binary_type, text_type))
        self._check_param("type", type, params, type=int, lte=2, gte=0)
        self._check_param("duration", duration, params, type=int)
        self._check_param("identity", identity, params, type=(binary_type, text_type), max_length=127)
        self._check_param("tags", tags, params, type=list, sub_type=(binary_type, text_type), sub_max_length=64)
        self._check_param("campaign", campaign, params, type=(binary_type, text_type), max_length=128)
        self._check_param("feature", feature, params, type=(binary_type, text_type), max_length=128)
        self._check_param("channel", channel, params, type=(binary_type, text_type), max_length=128)
        self._check_param("stage", stage, params, type=(binary_type, text_type), max_length=128)

        if skip_api_call is True:
            return params
        else:
            self._check_param("branch_key", self.branch_key, params, optional=False, type=(binary_type, text_type))
            return self.make_api_call(method, url, json_params=params)

    def create_deep_linking_urls(self, url_params):
        """
        Bulk Creates Deep Linking URLs

        See the URL https://dev.branch.io/references/http_api/#bulk-creating-deep-linking-urls

        :param url_params: Array of values returned from "create_deep_link_url(..., skip_api_call=True)"
        :return: The response
        """

        url = "/v1/url/bulk/%s" % self.branch_key
        method = "POST"

        # Checks params
        self._check_param(value=url_params, type=list, sub_type=dict, optional=False)

        return self.make_api_call(method, url, json_params=url_params)

    def make_api_call(self, method, url, json_params=None):
        """
        Accesses the branch API
        :param method: The HTTP method
        :param url: The URL
        :param json_params: JSON parameters
        :return: The parsed response
        """

        url = self.BRANCH_BASE_URI+url

        if self.verbose is True:
            print("Making web request: {}".format(url))

        if json_params is not None:
            encoded_params = json.dumps(json_params)
            headers = {'Content-Type': 'application/json'}
        else:
            encoded_params = None
            headers = {}

        if encoded_params is not None and self.verbose is True:
            print("Params: {}".format(encoded_params))

        request = Request(url, encoded_params, headers)
        request.get_method = lambda: method
        response = urlopen(request).read()
        return json.loads(response)
