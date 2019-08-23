from botocore.stub import Stubber


class StubotoCall(object):
    def __init__(self, stubber, method, expected_params):
        self.stubber = stubber
        self.method = method
        self.expected_params = expected_params

    def add_response(self, **kwargs):
        response = kwargs
        self.stubber.add_response(self.method, response, self.expected_params)
        return response


def method_factory(method):
    def patch_method(self, **kwargs):
        return StubotoCall(self, method, kwargs or None)

    patch_method.__name__ = method
    return patch_method


def Stuboto(client):
    class Stuboto(Stubber):
        __name__ = __qualname__ = f"{client.__class__.__name__}Stubber"

    for method in client.meta.method_to_api_mapping.keys():
        setattr(Stuboto, method, method_factory(method))

    return Stuboto(client)
