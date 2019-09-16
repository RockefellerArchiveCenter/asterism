from unittest import TestCase

from asterism import views


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
