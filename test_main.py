from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {
        "message": "Hello World!"
    }

def test_API():

    # Criando usuario
    email = 'teste@gmail.com'
    nome = 'teste'
    resp = client.post(f"/AdicionarUsuario/?email={email}&nome={nome}")
    assert resp.status_code == 200, resp.text
    post = resp.json()
    assert post["email"] == 'teste@gmail.com'
    assert post["nome"] == 'teste'

    # Verificando existencia do usuario
    resp = client.get("/ConsultarUsuarios")
    id = resp.json()[1][0]["_id"]
    assert resp.json()[1][0]["email"] == email
    assert resp.json()[1][0]["nome"] == nome


    # Alterando nome do usuario ---- Obs.: É possivel trocar tanto o nome quanto o email, podendo ser feito ao mesmo tempo ou em requisições diferentes
    novo_nome = 'teste2'
    resp = client.patch(f'/AlterarUsuario/?id={id}&nome={novo_nome}')
    resp = client.get("/ConsultarUsuarios")
    assert resp.json()[1][0]["email"] == email
    assert resp.json()[1][0]["nome"] == novo_nome


    # Criando Ponto
    lat = 1
    long = 2
    desc = 'Loja' # Opcional
    resp = client.post(f"/AdicionarPonto/?latitude={lat}&longitude={long}&email={email}&description={desc}")
    assert resp.json() == {
        "latitude": lat,
        "longitude": long,
        "description": desc,
        "email": email
    }

    # Verificando existencia do ponto
    resp = client.get('/ConsultarPontos')
    id = resp.json()[1][0]["_id"]
    assert resp.json()[1][0]["description"] == desc

    # Alterando o ponto
    nova_lat = 10
    nova_long = 20
    novo_email = 'novoteste@gmail.com'
    novo_nome = 'teste novo'
    resp = client.post(f"/AdicionarUsuario/?email={novo_email}&nome={novo_nome}")
    resp = client.patch(f"/AlterarPonto/?id={id}&latitude={nova_lat}&longitude={nova_long}&email={novo_email}")
    assert resp.json() == "Ponto alterado com sucesso"

    # Deletando ponto
    resp = client.delete(f"/DeletarPonto/?id={id}&user={novo_nome}")
    assert resp.json() == "Ponto deletado com sucesso"

    # Deletando usuarios
    resp = client.delete(f"/DeletarUsuario/?email={email}")
    resp = client.delete(f"/DeletarUsuario/?email={novo_email}")
    assert resp.json() == "Usuario deletado com sucesso"






