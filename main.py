##################### Extra Hard Starting Project ######################
import smtplib

# 1. Update the birthdays.csv
# 2. Check if today matches a birthday in the birthdays.csv
# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
# 4. Send the letter generated in step 3 to that person's email address.

import pandas as pd
import datetime as dt
from random import randint
# from dotenv import load_dotenv
import os


BIRTHDAYS_DF_PATH = "./birthdays.csv"
birthdays_people = {}


# 1. Read birthdays_df
birthdays_df = pd.read_csv(BIRTHDAYS_DF_PATH)


# 2. Check if there are any birthday match today date
today = dt.datetime.today()
today_year = today.year
today_month = today.month
today_day = today.day


# 3. Birthday people
for _, row in birthdays_df.iterrows():
    if row.month == today_month and row.day == today_day:
        random_letter = randint(1,3)
        with open(f"./letter_templates/letter_{random_letter}.txt", "r") as letter:
            letter_template = letter.read()
            new_letter = letter_template.replace("[NAME]", row.p_name.title())

        birthdays_people[row.p_name] = {
            "email": row.email,
            "msg": new_letter,
        }
print(birthdays_people)


# 4. Mail people
if len(birthdays_people) != 0:
    # load_dotenv()
    # EMAIL = os.getenv("EMAIL")
    # PASSWORD = os.getenv("PASSWORD")
    EMAIL = os.environ.get("MY_EMAIL")
    PASSWORD = os.environ.get("MY_PASSWORD")

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        for person in birthdays_people:
            person_data = birthdays_people[person]
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=person_data["email"],
                msg=f"Subject: Happy Birthday!\n\n"
                    f"{person_data['msg']}",
            )
    print("Email sent!")
else:
    print("No birthdays found!")
