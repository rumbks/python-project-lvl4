import pytest
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from tests.assert_ import redirects_to_login

CREATE_URL = reverse_lazy('labels:create')
UPDATE_URL = '/labels/{id}/update/'
DELETE_URL = '/labels/{id}/delete/'
INPUT_DATA = dict(name='name')


@pytest.fixture
def model():
    return Label


@pytest.fixture
def prepare_object():
    return None

@pytest.fixture
def fill_created_object():
    return None

@pytest.mark.django_db
def test_create(client, model, input_data):
    client.post(CREATE_URL, input_data)
    assert model.objects.get(name=input_data['name'])


@pytest.mark.usefixtures('authorized')
@pytest.mark.django_db
def test_update(client, model, input_data, created_object):
    old_name = created_object.name
    input_data['name'] = 'other_name'
    client.post(UPDATE_URL.format(id=created_object.id), input_data)
    assert model.objects.filter(name=old_name).count() == 0
    assert model.objects.get(name=input_data['name'])


@pytest.mark.usefixtures('authorized')
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
    assert redirects_to_login(response)
    retrieved_status = model.objects.get(id=created_object.id)
    assert retrieved_status == created_object
