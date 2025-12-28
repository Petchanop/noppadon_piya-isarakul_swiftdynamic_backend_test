from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

from apis.models import (
    Student, School, Classroom, GradeLevel, Province, SubDistrict, District, Address
)

class StudentAPITest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.province = Province.objects.create(name="Ratchaburi")
        self.district = District.objects.create(name="Banpong", province=self.province)
        self.sub_district = SubDistrict.objects.create(
            name="Banpong", district=self.district
        )

        self.address = Address.objects.create(
            province=self.province,
            district=self.district,
            sub_district=self.sub_district,
            house_no="10",
            village_number="",
            alley="",
            junstion="",
            road="",
            postal_code="70110",
        )

        self.school = School.objects.create(
            name="Benjamarachutit",
            name_abbreviation="บ.ม.",
            address=self.address,
        )

        self.grade = GradeLevel.objects.create(name="ป.3")

        self.classroom = Classroom.objects.create(
            school=self.school,
            grade=self.grade,
            room=4
        )

        self.student_payload = {
            "first_name": "Akradech",
            "last_name": "Yuenyong",
            "gender": "Male",
            "school": self.school.name,
            "classroom": {
                "grade": "ป.3",
                "room": 4
            }
        }

        self.url = reverse('v1:student-list')  # DRF router name
        
    def test_create_student_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url,
            self.student_payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)

        student = Student.objects.get()
        self.assertEqual(student.first_name, "Akradech")
        self.assertEqual(student.classroom, self.classroom)
        
    def test_list_students(self):
        Student.objects.create(
            first_name="Somchai",
            last_name="Dee",
            gender="M",
            school=self.school,
            classroom=self.classroom
        )

        response = self.client.get(self.url, format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)

    def test_filter_students_by_school_name(self):
        Student.objects.create(
            first_name="Somchai",
            last_name="Dee",
            gender="M",
            school=self.school,
            classroom=self.classroom
        )

        response = self.client.get(
            self.url,
            {"school": "Benja"},
            format='json'
        )
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)

    def test_student_detail(self):
        student = Student.objects.create(
            first_name="Somchai",
            last_name="Dee",
            gender="M",
            school=self.school,
            classroom=self.classroom
        )

        detail_url = reverse("v1:student-detail", args=[student.pk])

        response = self.client.get(detail_url, format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["first_name"], "Somchai")


    def test_update_student_classroom(self):
        student = Student.objects.create(
            first_name="Somchai",
            last_name="Dee",
            gender="M",
            school=self.school,
            classroom=self.classroom
        )

        payload = {
            "classroom": {
                "grade": "ป.3",
                "room": 4
            }
        }

        detail_url = reverse("v1:student-detail", args=[student.pk])

        response = self.client.patch(
            detail_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_invalid_school(self):
        payload = self.student_payload.copy()
        payload["school"] = "UnknownSchool"

        response = self.client.post(
            self.url,
            payload,
            format="json"
        )
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("school", data)


