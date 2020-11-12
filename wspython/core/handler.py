import orjson
from urllib import parse
from wspython.core.route import Route


class Request:
    def __init__(self, scope, receive):
        self.scope = scope
        self.receive = receive
        self._body = None

    @staticmethod
    async def build(scope, receive):
        request = Request(scope, receive)
        request.body = await request.read_body()

        return request

    async def read_body(self):
        body = b""
        more_body = True

        while more_body:
            message = await self.receive()
            body += message.get("body", b"")
            more_body = message.get("more_body", False)

        return orjson.loads(body) if body else {}

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def query_string(self):
        query = parse.parse_qs(self.scope["query_string"])

        return dict(
            (k.decode(), [item.decode() for item in v] if len(v) > 1 else v[0].decode())
            for k, v in query.items()
        )

    @property
    def headers(self):
        return self.scope["headers"]


class Response:
    def __init__(self, asgi_sender):
        self.asgi_sender = asgi_sender
        self.data = None

    def status(self, status):
        self.status = status

        return self

    async def send(self, data):
        await self.asgi_sender(
            {
                "type": "http.response.start",
                "status": self.status,
                "headers": [
                    [b"content-type", b"application/json"],
                ],
            }
        )
        await self.asgi_sender(
            {
                "type": "http.response.body",
                "body": orjson.dumps(data),
            }
        )


async def handle_request(route: Route, scope, receive, send):
    request = await Request.build(scope, receive)
    response = Response(send)

    handlers_iterator = (handler for handler in route.handlers)
    return await next(handlers_iterator)(
        request,
        response,
        handlers=handlers_iterator,
    )
