from typing import List, DefaultDict
from collections import defaultdict, namedtuple


Route = namedtuple("Route", "verb path handlers")


def dictify_routes(routes: List[Route]) -> DefaultDict[str, dict]:
    def _group_by_verb(routes: List[Route]):
        for route in routes:
            yield route.verb, route

    def _group_by_url(routes: List[Route], verb: str):
        for route in routes:
            if route.verb == verb:
                yield route.path, route

    dicted_routes: DefaultDict[str, dict] = defaultdict(dict)

    for verb, _ in _group_by_verb(routes):
        dicted_routes[verb] = dict(_group_by_url(routes, verb))

    return dicted_routes
