from unittest import TestCase

from .helpers import configure_django

# this has to be called before we try to import anything from DRF
configure_django()

from asterism import views
from rest_framework.test import APIRequestFactory

OBJECTS = ['123', '456']
MESSAGE = "this is a wake-up call"


class ServiceView(views.BaseServiceView):
    def get_service_response(self, request):
        return (MESSAGE, OBJECTS)


class BadView(views.BaseServiceView):
    def get_service_response(self, request):
        raise Exception(MESSAGE, OBJECTS)


class TestViews(TestCase):
    def test_prepare_response(self):
        INPUTS = (
            ("This is a string", 0),
            (("This is a tuple", "object1"), 1),
            (Exception("This is an Exception", ["object2", "object3"]), 2)
        )
        for i in INPUTS:
            response = views.prepare_response(i[0])
            self.assertIsInstance(response, dict)
            self.assertIsInstance(response['detail'], str)
            self.assertIsInstance(response['objects'], list)
            self.assertIsInstance(response['count'], int)
            self.assertEqual(response['count'], i[1])


class TestViewClasses(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_base_service_view(self):
        for view, expected_code in [(ServiceView, 200), (BadView, 500)]:
            request = self.factory.post(
                '/', '{}', content_type='application/json')
            response = view.as_view()(request)
            self.assertEqual(response.status_code, expected_code)
            self.assertEqual(response.data.get("objects"), OBJECTS)
            self.assertEqual(response.data.get("detail"), MESSAGE)
