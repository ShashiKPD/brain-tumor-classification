import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, prediction):
    sender_email = st.secrets["email"]["address"]
    sender_password = st.secrets["email"]["password"]

    subject = "Brain Tumor Classification Result"
    body = f"Hello,\n\nThe result of your MRI scan is: **{prediction}**.\n\nStay healthy!"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail SMTP and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        