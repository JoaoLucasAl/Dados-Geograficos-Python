def dados_helper(dados) -> dict:
    return {
        "_id": str(dados["_id"]),
        "latitude": dados["latitude"],
        "longitude": dados["longitude"],
        "description": dados["description"],
        "email": dados["email"]
    }


def dados_get_email(dados) -> str:
    return f'{dados["email"]}'
