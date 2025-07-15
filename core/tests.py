from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import UserProgress

class BookRecommenderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'testuser'
        self.session['jwt_token'] = 'fake-jwt-token'
        self.session.save()

        # Create initial progress for user
        UserProgress.objects.create(
            username='testuser',
            course='Intro to Python',
            progress=50,
            last_updated=timezone.now()
        )

    def test_course_progress_api_authenticated(self):
        response = self.client.get(reverse('course-progress-api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_course_progress_api_unauthenticated(self):
        self.client.session.flush()
        response = self.client.get(reverse('course-progress-api'))
        self.assertEqual(response.status_code, 401)

    def test_add_course_progress(self):
        response = self.client.post(
            reverse('add_course_progress'),
            content_type='application/json',
            data={'title': 'Django Advanced'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(UserProgress.objects.filter(course='Django Advanced').exists())

    def test_add_duplicate_course_progress(self):
        response = self.client.post(
            reverse('add_course_progress'),
            content_type='application/json',
            data={'title': 'Intro to Python'}  # Already exists
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Course already exists")

    def test_book_recommendations_with_valid_session(self):
        response = self.client.get(reverse('book-recommendations'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_book_recommendations_unauthorized(self):
        self.client.session.flush()
        response = self.client.get(reverse('book-recommendations'))
        self.assertEqual(response.status_code, 401)

    def test_login_and_redirect(self):
        # Simulate login failure
        response = self.client.post(reverse('login'), data={'username': 'fake', 'password': 'wrong'})
        self.assertContains(response, 'Invalid credentials', status_code=200)

    def test_progress_view_requires_login(self):
        self.client.session.flush()
        response = self.client.get(reverse('progress'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
