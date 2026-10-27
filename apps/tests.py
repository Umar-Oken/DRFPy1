import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class SwaggerSessionCsrfTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        get_user_model().objects.create_user(
            username="swagger-user",
            password="strong-test-password",
        )

    def test_login_rotates_csrf_token_and_task_can_be_created(self):
        swagger_response = self.client.get("/")
        self.assertEqual(swagger_response.status_code, 200)
        self.assertContains(swagger_response, "document.cookie")
        initial_token = self.client.cookies["csrftoken"].value

        login_response = self.client.post(
            "/api/login/",
            data=json.dumps(
                {"username": "swagger-user", "password": "strong-test-password"}
            ),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=initial_token,
        )
        self.assertEqual(login_response.status_code, 200)
        rotated_token = self.client.cookies["csrftoken"].value
        self.assertNotEqual(initial_token, rotated_token)

        stale_token_response = self.client.post(
            "/api/tasks/",
            data=json.dumps({"title": "said", "is_done": True}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=initial_token,
        )
        self.assertEqual(stale_token_response.status_code, 403)

        task_response = self.client.post(
            "/api/tasks/",
            data=json.dumps({"title": "said", "is_done": True}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=rotated_token,
        )
        self.assertEqual(task_response.status_code, 201)
        self.assertEqual(task_response.json()["title"], "said")
        self.assertTrue(task_response.json()["is_done"])
