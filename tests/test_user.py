from fastapi.testclient import TestClient

from src.main import app
from src.fake_db import db

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

unexisted_user = {
    'id': 4,
    'name': 'James Jonson',
    'email': 'j.j.jonson@mail.com',
}

new_user = {
    "name": "Kate Willow",
    "email": "k.k.willow@mail.com"
}

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("api/v1/user", params={'email': unexisted_user['email']})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    response = client.post("api/v1/user", json=new_user)
    assert response.status_code == 201
    assert response.json() == db.get_user_by_email(new_user['email'])['id']

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    response = client.post("api/v1/user", json=new_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    response = client.delete("api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 204

    response = client.get("api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}