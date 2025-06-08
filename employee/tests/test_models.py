from django.test import TestCase
from employee.models import Status, Position, Employee, Department


class StatusModelTest(TestCase):
    def test_create_status(self):
        status = Status.objects.create(name="Active")
        self.assertEqual(status.name, "Active")

    def test_str_representation(self):
        status = Status.objects.create(name="On Leave")
        self.assertEqual(str(status), "On Leave")


class PositionModelTest(TestCase):
    def test_create_position(self):
        pos = Position.objects.create(name="Designer", salary=35000.00)
        self.assertEqual(pos.name, "Designer")
        self.assertEqual(pos.salary, 35000.00)

    def test_update_salary(self):
        pos = Position.objects.create(name="Tester", salary=30000)
        pos.salary = 40000
        pos.save()
        self.assertEqual(pos.salary, 40000)


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Normal")
        self.position = Position.objects.create(
            name="Engineer", salary=45000.00)

    def test_create_employee_with_all_fields(self):
        emp = Employee.objects.create(
            name="John Doe",
            address="123 Somewhere",
            is_manager=True,
            status=self.status,
            position=self.position
        )
        self.assertEqual(emp.name, "John Doe")
        self.assertEqual(emp.position.name, "Engineer")
        self.assertTrue(emp.is_manager)

    def test_create_employee_without_position(self):
        emp = Employee.objects.create(
            name="Alice Smith",
            address="No Position St",
            is_manager=False,
            status=self.status
        )
        self.assertIsNone(emp.position)
        self.assertFalse(emp.is_manager)

    def test_default_is_manager_false(self):
        emp = Employee.objects.create(
            name="Temp",
            address="Temp St",
            status=self.status
        )
        self.assertFalse(emp.is_manager)

    def test_employee_image_nullable(self):
        emp = Employee.objects.create(
            name="Image Test",
            address="Img St",
            is_manager=False,
            status=self.status
        )
        self.assertFalse(emp.image)

    def test_update_employee_status(self):
        emp = Employee.objects.create(
            name="Update Me",
            address="Old Addr",
            status=self.status
        )
        new_status = Status.objects.create(name="Updated")
        emp.status = new_status
        emp.save()
        self.assertEqual(emp.status.name, "Updated")


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Active")
        self.position = Position.objects.create(name="Lead", salary=60000)
        self.manager = Employee.objects.create(
            name="Manager John",
            address="456 Admin Rd",
            is_manager=True,
            status=self.status,
            position=self.position
        )

    def test_create_department_with_manager(self):
        dept = Department.objects.create(name="HR", manager=self.manager)
        self.assertEqual(dept.name, "HR")
        self.assertEqual(dept.manager.name, "Manager John")

    def test_create_department_without_manager(self):
        dept = Department.objects.create(name="Unassigned")
        self.assertIsNone(dept.manager)

    def test_update_department_manager(self):
        new_manager = Employee.objects.create(
            name="New Boss",
            address="999 New Rd",
            is_manager=True,
            status=self.status,
            position=self.position
        )
        dept = Department.objects.create(name="Tech", manager=self.manager)
        dept.manager = new_manager
        dept.save()
        self.assertEqual(dept.manager.name, "New Boss")
