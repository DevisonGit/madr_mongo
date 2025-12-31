from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_health_ok(client):
    response = await client.get('/api/v1/health/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'ok'}
