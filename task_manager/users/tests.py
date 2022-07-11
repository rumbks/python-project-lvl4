from copy import copy

import pytest
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User

STATUS_CODE_REDIRECT = 302
USER_CREATE_URL = reverse_lazy('users:create')
USER_UPDATE_URL = '/users/{id}/update/'
USER_DELETE_URL = '/users/{id}/delete/'
PASSWORD = 'password'
USER_DATA = dict(username="jsmith", first_name='John', last_name='smith')


@pytest.fixture
def user_data():
    return copy(USER_DATA)


@pytest.fixture
def create_user(django_user_model, user_data):
    def create(**kwargs):
        user_data.update(kwargs)
        user = django_user_model(**user_data)
        user.set_password(PASSWORD)
        user.save()
        return user

    return create


@pytest.fixture
def created_user(django_user_model, create_user):
    return create_user()


@pytest.fixture
def logged_in_user(django_user_model, created_user, client):
    client.force_login(created_user)
    return created_user


@pytest.mark.django_db
def test_create(client, django_user_model, user_data):
    client.post(
        USER_CREATE_URL,
        {**user_data, 'password1': PASSWORD, 'password2': PASSWORD},
    )
    assert django_user_model.objects.get(username=user_data['username'])


@pytest.mark.django_db
def test_update_self(client, django_user_model, user_data, logged_in_user):
    old_username = logged_in_user.username
    user_data['username'] = 'johnsmith'
    client.post(
        USER_UPDATE_URL.format(id=logged_in_user.id),
        {**user_data, 'password1': PASSWORD, 'password2': PASSWORD},
    )
    assert django_user_model.objects.filter(username=old_username).count() == 0
    assert django_user_model.objects.get(username=user_data['username'])


@pytest.mark.django_db
def test_delete_self(client, django_user_model, logged_in_user):
    client.post(
        USER_DELETE_URL.format(id=logged_in_user.id),
    )
    assert (
        django_user_model.objects.filter(username=logged_in_user).count() == 0
    )


@pytest.mark.parametrize(
    ('url', 'params'),
    [(USER_UPDATE_URL, {'username': 'other'}), (USER_DELETE_URL, {})],
)
@pytest.mark.django_db
def test_change_unauthorized(
    client, django_user_model, created_user, url, params, user_data
):
    body_params = (
        {**user_data, **params, 'password1': PASSWORD, 'password2': PASSWORD}
        if params
        else {}
    )
    response = client.post(url.format(id=created_user.id), body_params)
    assert response.status_code == 302
    retrieved_user = django_user_model.objects.get(id=created_user.id)
    assert retrieved_user == created_user


@pytest.mark.usefixtures('logged_in_user')
@pytest.mark.parametrize(
    ('url', 'params'),
    [(USER_UPDATE_URL, {'username': 'other'}), (USER_DELETE_URL, {})],
)
@pytest.mark.django_db
def test_change_other(
    client, django_user_model, create_user, user_data, url, params
):
    other_user = create_user(username='other')
    body_params = (
        {**user_data, **params, 'password1': PASSWORD, 'password2': PASSWORD}
        if params
        else {}
    )
    response = client.post(
        url.format(id=other_user.id),
        body_params
    )
    assert response.status_code == 302
    retrieved_user = django_user_model.objects.get(id=other_user.id)
    assert retrieved_user == other_user
