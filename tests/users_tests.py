import pytest
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model

from tests.assert_ import redirects_to_login, redirects_to
from tests.constants import USER_DATA, USER_PASSWORD

CREATE_URL = reverse_lazy('users:create')
UPDATE_URL = '/users/{id}/update/'
DELETE_URL = '/users/{id}/delete/'
INPUT_DATA = USER_DATA


@pytest.fixture
def model():
    return get_user_model()


@pytest.fixture
def prepare_object():
    def prepare(user):
        user.set_password(USER_PASSWORD)
    return prepare

@pytest.fixture
def fill_created_object():
    return None


@pytest.mark.django_db
def test_create(client, model, input_data):
    client.post(
        CREATE_URL,
        {**input_data, 'password1': USER_PASSWORD, 'password2': USER_PASSWORD},
    )
    assert model.objects.get(username=input_data['username'])


@pytest.mark.django_db
def test_update_self(client, model, input_data, logged_in_user):
    old_username = logged_in_user.username
    input_data['username'] = 'johnsmith'
    client.post(
        UPDATE_URL.format(id=logged_in_user.id),
        {**input_data, 'password1': USER_PASSWORD, 'password2': USER_PASSWORD},
    )
    assert model.objects.filter(username=old_username).count() == 0
    assert model.objects.get(username=input_data['username'])


@pytest.mark.django_db
def test_delete_self(client, model, logged_in_user):
    client.post(
        DELETE_URL.format(id=logged_in_user.id),
    )
    assert (
        model.objects.filter(id=logged_in_user.id).count() == 0
    )


@pytest.mark.parametrize(
    ('url', 'params'),
    [(UPDATE_URL, {'username': 'other'}), (DELETE_URL, {})],
)
@pytest.mark.django_db
def test_change_unauthorized(
    client, model, created_object, url, params, input_data
):
    body_params = (
        {**input_data, **params, 'password1': USER_PASSWORD, 'password2': USER_PASSWORD}
        if params
        else {}
    )
    response = client.post(url.format(id=created_object.id), body_params)
    assert redirects_to_login(response)
    retrieved_user = model.objects.get(id=created_object.id)
    assert retrieved_user == created_object


@pytest.mark.usefixtures('authorized')
@pytest.mark.parametrize(
    ('url', 'params'),
    [(UPDATE_URL, {'username': 'other'}), (DELETE_URL, {})],
)
@pytest.mark.django_db
def test_change_other(
    client, model, create_object, input_data, url, params
):
    other_user = create_object(username='other')
    body_params = (
        {**input_data, **params, 'password1': USER_PASSWORD, 'password2': USER_PASSWORD}
        if params
        else {}
    )
    response = client.post(
        url.format(id=other_user.id),
        body_params
    )
    assert redirects_to(response, reverse('users:list'))
    retrieved_user = model.objects.get(id=other_user.id)
    assert retrieved_user == other_user
