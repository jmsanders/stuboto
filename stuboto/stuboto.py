from botocore.stub import Stubber


def func_factory(method, action):
    def func(self, **kwargs):
        self.method = method
        self.expected_params = kwargs or None
        return self
    func.__name__ = method
    return func


def stub(client):
    class Stuboto(Stubber):
        def with_response(self, response={}):
            self.add_response(self.method, response, self.expected_params)

    for method, action in client.meta.method_to_api_mapping.items():
        setattr(Stuboto, method, func_factory(method, action))

    class_name = f"{client.__class__.__name__}Stubber"
    Stuboto.__name__ = class_name
    Stuboto.__qualname__ = class_name
    stubber = Stuboto(client)
    stubber.activate()
    return stubber
