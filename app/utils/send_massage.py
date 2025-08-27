from kavenegar import KavenegarAPI, APIException, HTTPException
import os

api_key = os.getenv("KAVENEGAR_API_KEY")

def send_sms(to_number: str, message: str):
    try:
        api = KavenegarAPI(api_key)
        params = {
            'sender': '2000660110',
            'receptor': to_number,
            'message': message,
        }
        response = api.sms_send(params)
        return response
    except APIException as e:
        print(f"API Exception: {e}")
    except HTTPException as e:
        print(f"HTTP Exception: {e}")