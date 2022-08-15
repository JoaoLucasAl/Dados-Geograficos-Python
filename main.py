from fastapi import FastAPI, HTTPException
from config.database import colection_dados, colection_users
from helpers.dados import dados_helper, dados_get_email
from helpers.users import users_helper, get_email
from email_validator import validate_email
from bson import ObjectId

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Hello World!"
    }


@app.get('/ConsultarPontos')
async def get_all_dados():
    dados = []
    for dado in colection_dados.find():
        dados.append(dados_helper(dado))
    return "Pontos:", dados


@app.get('/ConsultarUsuarios')
async def get_all_users():
    users = []
    for user in colection_users.find():
        users.append(users_helper(user))
    return "Usuarios", users


@app.post('/AdicionarPonto/')
async def post_dados(latitude: float, longitude: float, email: str, description: str | None = None):
    if validate_email(email):
        if colection_users.find_one({"email": email}):
            colection_dados.insert_one({
                "latitude": latitude,
                "longitude": longitude,
                "description": description,
                "email": email
            })
            return {
                "latitude": latitude,
                "longitude": longitude,
                "description": description,
                "email": email
            }
        else:
            raise HTTPException(status_code=400, detail="Usuario não existe")
    else:
        raise HTTPException(status_code=400, detail="Email invalido")


@app.post('/AdicionarUsuario/')
async def post_user(email: str, nome: str):
    if colection_users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        if validate_email(email):

            colection_users.insert_one({
                "email": email,
                "nome": nome
            })
            return {
                "email": email,
                "nome": nome
            }
        else:
            raise HTTPException(status_code=400, detail="Email invalido")


@app.delete('/DeletarPonto/')
async def delete_dado(id: str, user: str):
    id = ObjectId(id)
    emails = []
    for item in colection_users.find({"nome":user}):
        emails.append(get_email(item))

    if colection_dados.find_one({"_id": id}):
        if dados_get_email(colection_dados.find_one({"_id": id})) in emails:
            colection_dados.delete_one({"_id": id})
            return "Ponto deletado com sucesso"
        else:
            raise HTTPException(status_code=400, detail="Email não atrelado ao ponto")
    else:
        raise HTTPException(status_code=400, detail="ID invalido")


@app.delete('/DeletarUsuario/')
async def delete_user(email: str):
    if colection_users.find_one({"email": email}):
        if colection_dados.find_one({"email": email}):
            raise HTTPException(status_code=400, detail="Delete todos os pontos atrelados ao usuario antes")
        else:
            colection_users.delete_one({"email": email})
            return "Usuario deletado com sucesso"
    else:
        raise HTTPException(status_code=400, detail="Usuario invalido")


@app.patch('/AlterarPonto/')
async def alter_dados(id: str, latitude: float | None = None, longitude: float | None = None,
                      description: str | None = None, email: str | None = None):
    id = ObjectId(id)
    if colection_dados.find_one({"_id": id}):
        if latitude is not None:
            colection_dados.update_one({"_id": id}, {"$set": {"latitude": latitude}})
        if longitude is not None:
            colection_dados.update_one({"_id": id}, {"$set": {"longitude": longitude}})
        if description is not None:
            colection_dados.update_one({"_id": id}, {"$set": {"description": description}})
        if email is not None:
            if colection_users.find_one({"email": email}):
                emails = []
                for item in colection_users.find({"email": email}):
                    emails.append(get_email(item))
                if email in emails:
                    colection_dados.update_one({"_id": id}, {"$set": {"email": email}})
                else:
                    raise HTTPException(status_code=400, detail="Email incorreto")
            else:
                raise HTTPException(status_code=400, detail="Usuario invalido")
        return "Ponto alterado com sucesso"
    else:
        raise HTTPException(status_code=400, detail="ID invalido")


@app.patch('/AlterarUsuario/')
async def alter_user(id: str, email: str | None = None, nome: str | None = None):
    id = ObjectId(id)
    if colection_users.find_one({"_id": id}):
        if email is not None:
            colection_users.update_one({"_id": id}, {"$set": {"email": email}})
        if nome is not None:
            colection_users.update_one({"_id": id}, {"$set": {"nome": nome}})
        return "Usuario alterado com sucesso"
    else:
        raise HTTPException(status_code=400, detail="ID invalido")
