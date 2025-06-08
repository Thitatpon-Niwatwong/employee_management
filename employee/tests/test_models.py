from django.test import TestCase
from employee.models import Status, Position, Employee, Department


class StatusModelTest(TestCase):
    def test_create_status(self):
        status = Status.objects.create(name="in recruitment process")
        self.assertEqual(status.name, "in recruitment process")

    def test_str_representation(self):
        status = Status.objects.create(name="resigned")
        self.assertEqual(str(status), "resigned")


class PositionModelTest(TestCase):
    def test_create_position(self):
        pos = Position.objects.create(name="UX Designer", salary=35000.00)
        self.assertEqual(pos.name, "UX Designer")
        self.assertEqual(pos.salary, 35000.00)

    def test_update_salary(self):
        pos = Position.objects.create(name="QA Tester", salary=30000)
        pos.salary = 40000
        pos.save()
        self.assertEqual(pos.salary, 40000)


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="normal")
        self.position = Position.objects.create(name="Software Engineer", salary=45000.00)

    def test_create_employee_with_all_fields(self):
        emp = Employee.objects.create(
            name="Decha Phongthong",
            address="123 Sukhumvit Road, Bangkok",
            is_manager=True,
            status=self.status,
            position=self.position
        )
        self.assertEqual(emp.name, "Decha Phongthong")
        self.assertEqual(emp.position.name, "Software Engineer")
        self.assertTrue(emp.is_manager)

    def test_create_employee_without_position(self):
        emp = Employee.objects.create(
            name="Kanya Srisuwan",
            address="88 Rama IV Road, Bangkok",
            is_manager=False,
            status=self.status
        )
        self.assertIsNone(emp.position)
        self.assertFalse(emp.is_manager)

    def test_default_is_manager_false(self):
        emp = Employee.objects.create(
            name="Charlie Brown",
            address="77 Phahonyothin Road, Bangkok",
            status=self.status
        )
        self.assertFalse(emp.is_manager)

    def test_employee_image_nullable(self):
        emp = Employee.objects.create(
            name="Nattapong Chaiyo",
            address="99 Ladprao Road, Bangkok",
            is_manager=False,
            status=self.status
        )
        self.assertFalse(emp.image)

    def test_update_employee_status(self):
        emp = Employee.objects.create(
            name="Somchai Supap",
            address="55 Silom Road, Bangkok",
            status=self.status
        )
        new_status = Status.objects.create(name="in probation period")
        emp.status = new_status
        emp.save()
        self.assertEqual(emp.status.name, "in probation period")


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="waiting for onboarding")
        self.position = Position.objects.create(name="Team Lead", salary=60000)
        self.manager = Employee.objects.create(
            name="Somsak Rojanasakul",
            address="12 Ratchadaphisek Road, Bangkok",
            is_manager=True,
            status=self.status,
            position=self.position
        )

    def test_create_department_with_manager(self):
        dept = Department.objects.create(name="Human Resources", manager=self.manager)
        self.assertEqual(dept.name, "Human Resources")
        self.assertEqual(dept.manager.name, "Somsak Rojanasakul")

    def test_create_department_without_manager(self):
        dept = Department.objects.create(name="Unassigned Department")
        self.assertIsNone(dept.manager)

    def test_update_department_manager(self):
        new_manager = Employee.objects.create(
            name="Panida Wongchai",
            address="88 Sathorn Road, Bangkok",
            is_manager=True,
            status=self.status,
            position=self.position
        )
        dept = Department.objects.create(name="Technology", manager=self.manager)
        dept.manager = new_manager
        dept.save()
        self.assertEqual(dept.manager.name, "Panida Wongchai")
