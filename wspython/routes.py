from wspython.core import Route
from wspython.handlers import hello_world

routes = [
    Route(
        verb="GET",
        path="/",
        handlers=[hello_world.get_hello_world_message],
    ),
]
