from copy import copy

import pytest
from django.contrib.auth import get_user_model
from tests import users_tests


@pytest.fixture
def input_data(request):
    return copy(request.module.INPUT_DATA)


@pytest.fixture
def create_object(prepare_object, model, input_data):
    def create(**kwargs):
        input_data.update(kwargs)
        object_ = model(**input_data)
        if prepare_object is not None:
            prepare_object(object_)
        object_.save()
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
