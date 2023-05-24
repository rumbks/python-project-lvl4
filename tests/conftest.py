from copy import copy

import pytest
from django.contrib.auth import get_user_model

from tests import constants


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
    user_ = user_model(**constants.USER_DATA)
    user_.set_password(constants.USER_PASSWORD)
    user_.save()
    return user_


@pytest.fixture
def logged_in_user(client, user):
    client.login(username=user.username, password=constants.USER_PASSWORD)
    return user

@pytest.fixture
def authorized(logged_in_user):
    pass
