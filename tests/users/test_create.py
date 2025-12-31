from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/api/v1/users/',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
