import orjson
import uvicorn
from typing import List

from wspython.core.route import Route
from wspython.core.handler import handle_request
from wspython.core.route import dictify_routes
from wspython.core.exceptions import RouteNotFound


class App:
    def __init__(self, routes: List[Route]):
        self.routes = dictify_routes(routes)

    def get_route_from_path(self, verb, path):
        try:
            return self.routes[verb][path]
        except KeyError:
            raise RouteNotFound(verb, path)

    async def send_404(self, exception: RouteNotFound, send):
        await send(
            {
                "type": "http.response.start",
                "status": 404,
                "headers": [
                    [b"content-type", b"application/json"],
                ],
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": orjson.dumps(
                    {
                        "message": f"Rota {exception.verb} \
                            {exception.path} não encontrada.",
                        "verb": exception.verb,
                        "path": exception.path,
                    }
                ),
            }
        )

    async def __call__(self, scope, receive, send):
        assert scope["type"] == "http"

        try:
            route = self.get_route_from_path(
                verb=scope["method"],
                path=scope["path"],
            )

            await handle_request(route, scope, receive, send)
        except RouteNotFound as exception:
            await self.send_404(send=send, exception=exception)


if __name__ == "__main__":
    uvicorn.run("wspython:app")
