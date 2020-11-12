class RouteNotFound(Exception):
    """
    `RouteNotFound` deve ser lançada quando uma rota é requisitada
    para o web service e não é encontrada.
    """

    def __init__(self, verb, path):
        super().__init__(f"A rota {verb} {path} não foi mapeada.")
        self.verb = verb
        self.path = path
