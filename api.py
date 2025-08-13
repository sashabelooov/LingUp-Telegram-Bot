from decouple import config
import requests

BASE_URL = config('BASE_URL')




def create_user(full_name, phone, tg_id, description=None):
    url = f"{BASE_URL}/api/contact/contact_via_bot/"


    payload = {
        "full_name": full_name,
        "phone_number": str(phone),
        "tg_id": tg_id,
        "description": description,

    }

    try:
        response = requests.post(url=url, data=payload)
        print(response.json(),"keldi")
        if response.status_code == 201:
            print("User created successfully.")
            return True

        return response.status_code

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
        return False

