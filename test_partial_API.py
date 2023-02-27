import requests
import json
import pytest

@pytest.fixture
def create_booking():
    # Membuat booking baru untuk digunakan dalam test case
    url = "https://restful-booker.herokuapp.com/api/booking"
    headers = {"Content-Type": "application/json"}
    data = {
        "firstname": "Adikrisna",
        "lastname": "Nugraha",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2022-03-01",
            "checkout": "2022-03-05"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    booking = json.loads(response.text)
    yield booking
    # Menghapus booking setelah test case selesai
    url = f"https://restful-booker.herokuapp.com/api/booking/{booking['bookingid']}"
    response = requests.delete(url, headers=headers)
    assert response.status_code == 204

def test_partial_update_booking(create_booking):
    # Memperbarui data booking yang sudah dibuat sebelumnya
    booking_id = create_booking["bookingid"]
    url = f"https://restful-booker.herokuapp.com/api/booking/{booking_id}"
    headers = {"Content-Type": "application/json"}
    data = {"firstname": "Adikrisnakrisna"}
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    assert response.status_code == 200
    # Memeriksa apakah data booking sudah diperbarui dengan benar
    response = requests.get(url)
    booking = json.loads(response.text)
    assert booking["firstname"] == "Adikrisnakrisna"
    assert booking["lastname"] == "Nugraha"
    assert booking["totalprice"] == 100
    assert booking["depositpaid"] == True
    assert booking["bookingdates"]["checkin"] == "2022-03-01"
    assert booking["bookingdates"]["checkout"] == "2022-03-05"
    assert booking["additionalneeds"] == "Breakfast"
