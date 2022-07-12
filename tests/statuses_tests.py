import pytest
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status

STATUS_CODE_REDIRECT = 302
CREATE_URL = reverse_lazy('statuses:create')
UPDATE_URL = '/statuses/{id}/update/'
DELETE_URL = '/statuses/{id}/delete/'
INPUT_DATA = dict(name='name')


@pytest.fixture
def model():
    return Status


@pytest.mark.django_db
def test_create(client, model, input_data):
    client.post(CREATE_URL, input_data)
    assert model.objects.get(name=input_data['name'])


@pytest.mark.usefixtures('logged_in_user')
@pytest.mark.django_db
def test_update(client, model, input_data, created_object):
    old_name = created_object.name
    input_data['name'] = 'other_name'
    client.post(UPDATE_URL.format(id=created_object.id), input_data)
    assert model.objects.filter(name=old_name).count() == 0
    assert model.objects.get(name=input_data['name'])


@pytest.mark.usefixtures('logged_in_user')
@pytest.mark.django_db
def test_delete(client, model, created_object):
    client.post(
        DELETE_URL.format(id=created_object.id),
    )
    assert model.objects.filter(id=created_object.id).count() == 0


@pytest.mark.parametrize(
    ('url', 'params'),
    [(UPDATE_URL, {'name': 'other'}), (DELETE_URL, {})],
)
@pytest.mark.django_db
def test_change_unauthorized(
    client, model, created_object, url, params, input_data
):
    body_params = (
        {**input_data, **params}
        if params
        else {}
    )
    response = client.post(url.format(id=created_object.id), body_params)
    assert response.status_code == 302
    retrieved_status = model.objects.get(id=created_object.id)
    assert retrieved_status == created_object
