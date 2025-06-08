from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
from io import BytesIO

from employee.models import Status, Position, Department, Employee

class LoginAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='loginuser', password='loginpass')

    def test_login_success(self):
        response = self.client.post(reverse('api_token_auth'), {
            'username': 'loginuser',
            'password': 'loginpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_failure(self):
        response = self.client.post(reverse('api_token_auth'), {
            'username': 'wrong',
            'password': 'invalid'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)


class APITestSetup(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.status = Status.objects.create(name="normal")
        self.position = Position.objects.create(name="Software Developer", salary=50000.00)

        self.employee = Employee.objects.create(
            name="Anan Krahan",
            address="123 Sukhumvit Road, Wattana District, Bangkok",
            position=self.position,
            status=self.status,
            is_manager=True
        )

        self.department = Department.objects.create(name="Information Technology", manager=self.employee)


class StatusAPITests(APITestSetup):
    def test_create_status(self):
        response = self.client.post(reverse('status-list'), {"name": "resigned"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_status_list(self):
        response = self.client.get(reverse('status-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_status(self):
        response = self.client.put(reverse('status-detail', args=[self.status.id]), {"name": "in probation period"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_status(self):
        response = self.client.delete(reverse('status-detail', args=[self.status.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PositionAPITests(APITestSetup):
    def test_create_position(self):
        response = self.client.post(reverse('position-list'), {"name": "Quality Assurance", "salary": 45000.00})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_position_list(self):
        response = self.client.get(reverse('position-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_position(self):
        response = self.client.put(reverse('position-detail', args=[self.position.id]), {
            "name": "Senior Developer",
            "salary": 60000.00
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_position(self):
        response = self.client.delete(reverse('position-detail', args=[self.position.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DepartmentAPITests(APITestSetup):
    def test_create_department(self):
        response = self.client.post(reverse('department-list'), {
            "name": "Human Resources",
            "manager": self.employee.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_department_list(self):
        response = self.client.get(reverse('department-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_department(self):
        response = self.client.put(reverse('department-detail', args=[self.department.id]), {
            "name": "Technology Division",
            "manager": self.employee.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_department(self):
        response = self.client.delete(reverse('department-detail', args=[self.department.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EmployeeAPITests(APITestSetup):
    def test_create_employee(self):
        response = self.client.post(reverse('employee-list'), {
            "name": "Jarupat Srisuwan",
            "address": "789 Ngamwongwan Road, Mueang District, Nonthaburi",
            "position_id": self.position.id,
            "status_id": self.status.id,
            "department_id": self.department.id,
            "is_manager": False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Jarupat Srisuwan")

    def test_get_employee_list(self):
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_employee(self):
        response = self.client.get(reverse('employee-list'), {'search': 'Anan Krahan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_by_status(self):
        response = self.client.get(reverse('employee-list'), {'status': self.status.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_employee(self):
        response = self.client.put(reverse('employee-detail', args=[self.employee.id]), {
            "name": "Nopparat Jareonwongsak",
            "address": "456 Ladprao Soi 101, Bangkapi, Bangkok",
            "position_id": self.position.id,
            "status_id": self.status.id,
            "department_id": self.department.id,
            "is_manager": True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Nopparat Jareonwongsak")

    def test_partial_update_employee(self):
        response = self.client.patch(reverse('employee-detail', args=[self.employee.id]), {
            "address": "New Address Only"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], "New Address Only")

    def test_delete_employee(self):
        response = self.client.delete(reverse('employee-detail', args=[self.employee.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upload_employee_image(self):
        image = generate_test_image()

        response = self.client.post(reverse('employee-list'), {
            "name": "Suda Thongchai",
            "address": "Phahonyothin Road, Chatuchak, Bangkok",
            "position_id": self.position.id,
            "status_id": self.status.id,
            "is_manager": False,
            "department_id": self.department.id,
            "image": image
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("employee_images/", response.data["image"])

    def test_unauthenticated_access(self):
        self.client.credentials()
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def generate_test_image():
    image = Image.new('RGB', (100, 100), color='blue')
    byte_io = BytesIO()
    image.save(byte_io, 'JPEG')
    byte_io.seek(0)
    return SimpleUploadedFile("test.jpg", byte_io.read(), content_type="image/jpeg")