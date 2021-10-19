import requests
from datetime import datetime
import smtplib
import os

MY_LAT = os.environ.get("SECRET_LAT")
MY_LONG = os.environ.get("SECRET_LONG")

suzy_email = os.environ.get("SECRET_EMAIL_1")
suzy_password = os.environ.get("SECRET_PASSWORD")
josh_email = os.environ.get("SECRET_EMAIL_2")


def is_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if sunset <= time_now.hour <= sunrise:
        return True


if is_night() and is_close():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=suzy_email, password=suzy_password)
        connection.sendmail(from_addr=suzy_email, to_addrs=josh_email, msg="Subject:Look up!!\n\n"
                                                                           "The international space station"
                                                                           " is above you!!\n Right now!")
