import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, prediction):
    sender_email = st.secrets["email"]["address"]
    sender_password = st.secrets["email"]["password"]

    subject = "Brain Tumor Diagnosis Result"
    # body = f"Hello,\n\nThe result of your MRI scan is: {prediction}.\n\nStay healthy!"
    html = f"""
      <html>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px 0;">
            <tr>
              <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0,0,0,0.05); padding: 30px;">
                  <!-- Header -->
                  <tr>
                    <td align="center" style="padding-bottom: 20px;">
                      <h1 style="color: #2c3e50; margin: 0;">🧠 TumorDetect Diagnostics</h1>
                      <p style="color: #888888; font-size: 14px; margin: 5px 0 0;">Your trusted AI-based MRI tumor diagnosis</p>
                    </td>
                  </tr>
                  
                  <!-- Greeting -->
                  <tr>
                    <td>
                      <p style="font-size: 16px; color: #333333;">Dear Patient,</p>
                      <p style="font-size: 16px; color: #333333;">
                        Thank you for using our MRI brain tumor classification system. Based on our deep learning analysis of your uploaded scan, we have generated the following result:
                      </p>
                    </td>
                  </tr>

                  <!-- Result Section -->
                  <tr>
                    <td align="center" style="padding: 20px 0;">
                      <div style="background-color: #eaf6f6; padding: 20px; border-radius: 8px;">
                        <h2 style="color: #e74c3c; font-size: 24px; margin: 0;">Diagnosis Result:</h2>
                        <p style="font-size: 22px; font-weight: bold; color: #34495e; margin: 10px 0 0;">{prediction}</p>
                      </div>
                    </td>
                  </tr>

                  <!-- Explanation -->
                  <tr>
                    <td>
                      <p style="font-size: 15px; color: #555555;">
                        Please note that this is an AI-generated result and should not replace professional medical consultation. We strongly recommend sharing this report with your healthcare provider for further evaluation and diagnosis.
                      </p>
                    </td>
                  </tr>

                  <!-- Footer -->
                  <tr>
                    <td align="center" style="padding-top: 30px;">
                      <p style="font-size: 13px; color: #999999;">
                        Sent securely from <a href="tumordetect.streamlit.app" style="color: #3498db; text-decoration: none;">TumorDetect.ai</a> — a research initiative in medical imaging and AI.
                      </p>
                      <p style="font-size: 12px; color: #cccccc;">© 2025 TumorDetect. All rights reserved.</p>
                    </td>
                  </tr>

                </table>
              </td>
            </tr>
          </table>
        </body>
      </html>

      """
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(html, "html"))

    # Connect to Gmail SMTP and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        