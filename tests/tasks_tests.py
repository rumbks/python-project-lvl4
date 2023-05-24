import pytest
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from tests import users_tests
from tests.assert_ import redirects_to_login, redirects_to

STATUS_CODE_REDIRECT = 302
CREATE_URL = reverse_lazy('tasks:create')
UPDATE_URL = '/tasks/{id}/update/'
DELETE_URL = '/tasks/{id}/delete/'
STATUS_NAME = 'status'
LABEL_NAME = 'label'
INPUT_DATA = dict(name='name', description='description')
User = get_user_model()


@pytest.fixture
def model():
    return Task


@pytest.fixture
def status():
    return Status.objects.create(name=STATUS_NAME)


@pytest.fixture
def label():
    return Label.objects.create(name=STATUS_NAME)


@pytest.fixture
def other_user():
    user_data = {**users_tests.INPUT_DATA, 'username': 'other'}
    user = User.objects.create(**user_data)
    user.set_password('password')
    user.save()
    return user


@pytest.fixture
def prepare_object(status, user):
    def prepare(task):
        task.status = status
        task.author = user
        task.executor = user

    return prepare


@pytest.fixture
def fill_created_object(label):
    def fill(task):
        task.labels.set([label])

    return fill

@pytest.mark.usefixtures('authorized')
@pytest.mark.django_db
def test_create(client, model, input_data, status):
    body_params = {**input_data, 'status': status.id}
    client.post(CREATE_URL, body_params)
    assert model.objects.get(name=input_data['name'])


@pytest.mark.usefixtures('authorized')
@pytest.mark.django_db
def test_update(client, model, input_data, created_object, status):
    old_name = created_object.name
    input_data['name'] = 'other_name'
    input_data['status'] = status.id
    client.post(UPDATE_URL.format(id=created_object.id), input_data)
    assert model.objects.filter(name=old_name).count() == 0
    updated_task = model.objects.get(name=input_data['name'])
    assert updated_task.status == status


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
    body_params = {**input_data, **params} if params else {}
    response = client.post(url.format(id=created_object.id), body_params)
    assert redirects_to_login(response)
    retrieved_task = model.objects.get(id=created_object.id)
    assert retrieved_task == created_object


@pytest.mark.usefixtures('authorized')
@pytest.mark.django_db
def test_delete_without_ownership(
    client, model, created_object, other_user
):
    created_object.author = other_user
    created_object.save()
    response = client.post(
        DELETE_URL.format(id=created_object.id),
    )
    assert redirects_to(response, reverse('tasks:list'))
    retrieved_task = model.objects.get(id=created_object.id)
    assert retrieved_task == created_object


@pytest.mark.usefixtures('authorized')
@pytest.mark.django_db
def test_delete_linked_label(client, created_object, label):
    response = client.post(reverse('labels:delete', kwargs={'pk': label.id}))
    assert redirects_to(response, reverse('labels:list'))
    assert Label.objects.get(id=label.id)
