import requests
import unittest

class TestAPI(unittest.TestCase):
    API_ENDPOINT = "https://restful-booker.herokuapp.com"
    USERNAME = "adikrisna"
    PASSWORD = "password123"

    def setUp(self):
        self.session = requests.Session()
        self.access_token = self.login()

    def tearDown(self):
        self.session.close()

    def login(self):
        response = self.session.post(
            f"{self.API_ENDPOINT}/auth",
            json={
                "username": self.USERNAME,
                "password": self.PASSWORD
            }
        )
        return response.json()["token"]

    def create_booking(self):
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {
            "firstname": "Adikrisna",
            "lastname": "Nugraha",
            "totalprice": 123,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2022-03-01",
                "checkout": "2022-03-02"
            },
            "additionalneeds": "Breakfast"
        }
        response = self.session.post(
            f"{self.API_ENDPOINT}/booking",
            headers=headers,
            json=data
        )
        return response.json()["bookingid"]

    def test_get_booking(self):
        booking_id = self.create_booking()
        headers = {"Authorization": "Bearer " + self.access_token}
        response = self.session.get(
            f"{self.API_ENDPOINT}/booking/{booking_id}",
            headers=headers
        )
        self.assertIn("booking", response.json())

    def test_update_booking(self):
        booking_id = self.create_booking()
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {
            "firstname": "Updated",
            "lastname": "User",
            "totalprice": 123,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2022-03-01",
                "checkout": "2022-03-02"
            },
            "additionalneeds": "Breakfast"
        }
        response = self.session.put(
            f"{self.API_ENDPOINT}/booking/{booking_id}",
            headers=headers,
            json=data
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_booking(self):
        booking_id = self.create_booking()
        headers = {"Authorization": "Bearer " + self.access_token}
        response = self.session.delete(
            f"{self.API_ENDPOINT}/booking/{booking_id}",
            headers=headers
        )
        self.assertEqual(response.status_code, 201)