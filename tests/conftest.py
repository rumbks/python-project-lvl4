from copy import copy
from urllib.parse import urlparse

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from tests import users_tests
from tests.constants import HTTP_REDIRECT_STATUS_CODE


@pytest.fixture(scope='session')
def redirects_to():
    def redirects_to_(response, url):
        assert (
            response.status_code == HTTP_REDIRECT_STATUS_CODE
        ), f"Expected status code to be {HTTP_REDIRECT_STATUS_CODE}, but it's {response.status_code}"
        redirected_url_path = urlparse(response.url).path
        return redirected_url_path == url

    return redirects_to_


@pytest.fixture(scope='session')
def redirects_to_login(redirects_to):
    def redirects_(response):
        return redirects_to(response, reverse('login'))

    return redirects_


@pytest.fixture
def input_data(request):
    return copy(request.module.INPUT_DATA)


@pytest.fixture
def create_object(prepare_object, fill_created_object, model, input_data):
    def create(**kwargs):
        input_data.update(kwargs)
        object_ = model(**input_data)
        if prepare_object is not None:
            prepare_object(object_)
        object_.save()
        if fill_created_object is not None:
            fill_created_object(object_)
        return object_
    return create


@pytest.fixture
def created_object(create_object):
    return create_object()


@pytest.fixture
def user():
    user_model = get_user_model()
    user_ = user_model(**users_tests.INPUT_DATA)
    user_.set_password(users_tests.PASSWORD)
    user_.save()
    return user_


@pytest.fixture
def logged_in_user(client, user):
    client.login(username=user.username, password=users_tests.PASSWORD)
    return user

@pytest.fixture
def authorized(logged_in_user):
    pass
