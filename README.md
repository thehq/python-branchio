# BranchIo

[![PyPi version](https://img.shields.io/pypi/v/branchio.svg)](https://pypi.python.org/pypi/branchio)
[![PyPi downloads](https://img.shields.io/pypi/dm/branchio.svg)](https://pypi.python.org/pypi/branchio)
[![Circle CI](https://img.shields.io/circleci/token/ba05cb60f8cf01d2611264ef8fba82d0e07a4b68/project/thehq/python-branchio/master.svg)](https://circleci.com/gh/thehq/python-branchio/tree/master)
[![Codecov](https://img.shields.io/codecov/c/github/thehq/python-branchio/master.svg)](https://codecov.io/github/thehq/python-branchio)
[![PyPi license](https://img.shields.io/pypi/l/branchio.svg)](https://pypi.python.org/pypi/branchio)

This library is intended to make API calls to the Branch.io API.

## Revision History

  - v0.1.0:
    - Initial Revision

## Installation

    %> pip install branchio
    
## Usage

To create a client, do the following

    import branchio
    
    client = branchio.Client("BRANCH KEY")

### Create a Deep Linking URL

    response = client.create_deep_link_url(
        data={
            branchio.DATA_BRANCH_IOS_URL="<customer iOS download link>",
            "user": {
                "name": "John Doe"
            }
        },
        channel="facebook"
    )
    
    url = response[branchio.RETURN_URL]
    
### Bulk Create Deep Linking URLs

    params1 = client.create_deep_link_url(
        data={
            "user": {
                "name": "John Doe"
            }
        },
        channel="facebook",
        skip_api_call=True
    )
    
    params2 = client.create_deep_link_url(
        data={
            "user": {
                "name": "Jane Doe"
            }
        },
        channel="facebook",
        skip_api_call=True
    )
    
    response = client.create_deep_linking_urls([params1, params2])
    
## Testing
To test locally, simply cd into the project directory and run

    %> coverage run --source branchio/ -m unittest discover
    
If you do not define the environment variable "BRANCH_IO_KEY" the test will run using stubbed responses.
    
## Contributing
I haven't setup the other calls yet but will get to that at some point.  If you would like to contribute, simply fork
the repository and submit a pull request.