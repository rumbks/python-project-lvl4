from copy import copy

import pytest
from django.contrib.auth import get_user_model
from tests import users_tests

@pytest.fixture
def input_data(request):
    return copy(request.module.INPUT_DATA)


@pytest.fixture
def create_object(request, model, input_data):
    def create(**kwargs):
        input_data.update(kwargs)
        object_ = model(**input_data)
        prepare = getattr(request.module, 'prepare_object', None)
        if prepare is not None:
            prepare(object_)
        object_.save()
        return object_
    return create


@pytest.fixture
def created_object(create_object):
    return create_object()


@pytest.fixture
def logged_in_user(client):
    user_model = get_user_model()
    user = user_model(**users_tests.INPUT_DATA)
    user.set_password(users_tests.PASSWORD)
    user.save()
    client.force_login(user)
    return user
