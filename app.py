import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import hashlib
import os
import re
from functools import wraps
from flask import Flask, request, render_template, redirect, session, url_for, abort
from database import get_db_connection, database


from datetime import datetime

# Get the current date and time
now = datetime.now()
date = now.strftime("%Y-%m-%d")

app = Flask(__name__)


@app.route("/")
def root():
    try:
        database()
    except Exception as e:
        return render_template("error.html", info=str(e))
    return render_template("dataform.html")

def generate_certificate_number(prefix="DRF-"):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT MAX(Certificate_no) FROM information")
                max_certificate_number = cursor.fetchone()[0]
                if max_certificate_number is None:
                    return prefix + "1"
                else:
                    numeric_part = int(max_certificate_number.split("-")[-1])
                    new_certificate_no = numeric_part + 1
                    return f"{prefix}{new_certificate_no}"
    except Exception as e:
        raise e

@app.route("/registerdataform", methods=["POST"])
def registerdataform():
    try:
        name = request.form.get("name")
        fathername = request.form.get("fathername")
        mothername = request.form.get("mothername")
        grandfathername = request.form.get("grandfathername")
        gender = request.form.get("gender")
        dob = request.form.get("dob")
        education = request.form.get("education")
        employeed = request.form.get("employed")
        abroad = request.form.get("abroad")
        userid = 2
        if employeed == "Unemployed":
            reason_for_unemployment = request.form.get("reason_for_unemployment")
        else:
            reason_for_unemployment = 0
        if education == "Illiterate":
            reason_for_uneducated = request.form.get("reason_for_uneducation")
        else:
            reason_for_uneducated = 0
        if abroad == "Yes":
            reason_for_abroad = request.form.get("reason_for_abroad")
        else:
            reason_for_abroad = 0

        # Generate a unique certificate number
        certificate_no = generate_certificate_number()

        # Insert data into the detail table along with the generated certificate number
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO information(
                            Certificate_no,
                            fullname, 
                            fathername, 
                            mothername, 
                            grandfathername, 
                            dob, 
                            gender, 
                            education, 
                            employeed, 
                            abroad, 
                            issueddate,
                            reason_for_unemployment,
                            reason_for_uneducated,
                            reason_for_abroad,
                            user_id    
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)""",
                        (
                            certificate_no,
                            name,
                            fathername,
                            mothername,
                            grandfathername,
                            dob,
                            gender,
                            education,
                            employeed,
                            abroad,
                            date,
                            reason_for_unemployment,
                            reason_for_uneducated,
                            reason_for_abroad,
                            userid,
                        ),
                    )
                    conn.commit()
                    return redirect("/")
        except Exception as e:
            conn.rollback()
            return str(e)

    except Exception as e:
        return str(e)
