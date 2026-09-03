from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Mechanic, ServiceRequest

#for automated testing so that we dont have to test manually like in browser or postman
#after testing is complete, the testing data is wiped out so that the real data is not polluted
#on running the test, we will get '.' for every pass and 'F' for fail
class MechanicAPITests(APITestCase):
    def setUp(self):        #to start the testing with at least one clean known value
        self.mechanic = Mechanic.objects.create(
            name="Bob's Garage",
            phone="9876543210",
            location="Pune",
            rating=4.5,
            is_open=True,
            services="Oil Change, Tire Repair"
        )

    def test_list_mechanics(self):
        url = reverse('mechanic-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_mechanic_success(self):
        url = reverse('mechanic-list')
        data = {
            "name": "Speedy Auto",
            "phone": "9123456780",
            "location": "Mumbai",
            "rating": 4.0,
            "is_open": True,
            "services": "Brake Service"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mechanic.objects.count(), 2)

    def test_create_mechanic_invalid_phone(self):
        url = reverse('mechanic-list')
        data = {
            "name": "Bad Phone Garage",
            "phone": "123",
            "location": "Mumbai",
            "services": "Brake Service"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)

    def test_create_mechanic_missing_required_field(self):
        url = reverse('mechanic-list')
        data = {"name": "Incomplete Garage"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)
        self.assertIn('location', response.data)

    def test_get_mechanic_by_id(self):
        url = reverse('mechanic-detail', kwargs={'pk': self.mechanic.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Bob's Garage")

    def test_delete_mechanic(self):
        url = reverse('mechanic-detail', kwargs={'pk': self.mechanic.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mechanic.objects.count(), 0)


class ServiceRequestAPITests(APITestCase):
    def setUp(self):
        self.mechanic = Mechanic.objects.create(
            name="Bob's Garage",
            phone="9876543210",
            location="Pune",
            rating=4.5,
            is_open=True,
            services="Oil Change, Tire Repair"
        )

    def test_create_service_request_success(self):
        url = reverse('servicerequest-list')
        data = {
            "customer_name": "Alice",
            "customer_phone": "9988776655",
            "vehicle_number": "MH12AB1234",
            "mechanic": self.mechanic.pk,
            "service": "Oil Change",
            "problem_description": "Engine noise"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'PENDING')

    def test_create_service_request_invalid_mechanic(self):
        url = reverse('servicerequest-list')
        data = {
            "customer_name": "Alice",
            "customer_phone": "9988776655",
            "vehicle_number": "MH12AB1234",
            "mechanic": 9999,
            "service": "Oil Change",
            "problem_description": "Engine noise"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('mechanic', response.data)

    def test_create_service_request_invalid_service(self):
        url = reverse('servicerequest-list')
        data = {
            "customer_name": "Alice",
            "customer_phone": "9988776655",
            "vehicle_number": "MH12AB1234",
            "mechanic": self.mechanic.pk,
            "service": "Wheel Alignment",
            "problem_description": "Engine noise"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('service', response.data)
