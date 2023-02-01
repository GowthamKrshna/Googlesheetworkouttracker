import datetime
import requests
import os

GENDER = 'male'
WEIGHT_KG = '72'
HEIGHT_CM = '182'
AGE = '31'
API_KEY = os.environ['API_KEY']
APP_ID = os.environ['APP_ID']
END_POINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'
exercise = input('Tell me what exercise you did today? :')
SHEET_URL = os.environ['SHEET_URL']
SHEET_AUTH = os.environ['SHEET_AUTH']
header = {
    'x-app-id': APP_ID,
    'x-app-key':API_KEY
}

parameters = {
    "query": exercise,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
response = requests.post(END_POINT,json=parameters, headers=header)
result = response.json()
print(result)
today_date = datetime.datetime.now().strftime("%d/%m/%Y")
now_time = datetime.datetime.now().strftime("%X")

for exercise in result["exercises"]:
    print(exercise)
    sheet_detail = {'workout':
        {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
           }
    }
sheet_auth = {
    'Authorization': SHEET_AUTH
}
sheet_response = requests.post(SHEET_URL, json=sheet_detail, headers=sheet_auth)

print(sheet_response.status_code)
print(sheet_response.json())