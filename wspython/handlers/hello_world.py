from wspython.core.handler import Request, Response


async def get_hello_world_message(
    request: Request,
    response: Response,
    **kwargs,
):
    """
    `hello_world` retorna a mensagem "Hello World".
    """

    msg = {
        "message": f"Hello, {request.query_string.get('nome', 'World')}",
    }

    await response.status(200).send(msg)
