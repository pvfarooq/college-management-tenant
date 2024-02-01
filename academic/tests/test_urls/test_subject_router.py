from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import routers

from academic.api.views import SubjectViewSet


class SubjectURLsTestCase(TestCase):
    def setUp(self):
        self.router = routers.DefaultRouter()
        self.router.register("subjects", SubjectViewSet)

    def test_subject_list_url(self):
        url = reverse("subject-list")
        self.assertEqual(url, "/academic/subjects/")
        self.assertEqual(resolve(url).func.cls, SubjectViewSet)

    def test_subject_detail_url(self):
        url = reverse("subject-detail", kwargs={"pk": "1"})
        self.assertEqual(url, "/academic/subjects/1/")
        self.assertEqual(resolve(url).func.cls, SubjectViewSet)

    def test_subject_create_url(self):
        url = reverse("subject-list")
        self.assertEqual(url, "/academic/subjects/")
        self.assertEqual(resolve(url).func.cls, SubjectViewSet)

    def test_subject_update_url(self):
        url = reverse("subject-detail", kwargs={"pk": "1"})
        self.assertEqual(url, "/academic/subjects/1/")
        self.assertEqual(resolve(url).func.cls, SubjectViewSet)

    def test_subject_delete_url(self):
        url = reverse("subject-detail", kwargs={"pk": "1"})
        self.assertEqual(url, "/academic/subjects/1/")
        self.assertEqual(resolve(url).func.cls, SubjectViewSet)
