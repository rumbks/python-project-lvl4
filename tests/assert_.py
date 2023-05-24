from urllib.parse import urlparse

from django.urls import reverse

from tests.constants import HTTP_REDIRECT_STATUS_CODE


def redirects_to(response, url):
    assert (
            response.status_code == HTTP_REDIRECT_STATUS_CODE
    ), f"Expected status code to be {HTTP_REDIRECT_STATUS_CODE}, but it's {response.status_code}"
    redirected_url_path = urlparse(response.url).path
    return redirected_url_path == url

def redirects_to_login(response):
    return redirects_to(response, reverse('login'))

