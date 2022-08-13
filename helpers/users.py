
def users_helper(users) -> dict:
    return{
        "_id": str(users["_id"]),
        "email": users["email"],
        "nome": users["nome"]
    }

def get_email(nome) -> str:
    return f'{nome["email"]}'