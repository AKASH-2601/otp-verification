import smtplib
import random
import string
import time
import streamlit as st
from threading import Thread



# Function to generate OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# Function to send OTP
def send_otp(receiver_email):
    sender_email = "akash26242931@gmail.com"
    sender_password = "tqzt azhm ktyh bpze"

    otp = generate_otp()
    subject = "Your OTP Code"
    body = f"Subject: {subject}\n\nYour OTP is: {otp}\nIt is valid for 1 minute."

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, body)
        server.quit()

        return otp, time.time()
    except Exception as e:
        st.error(f"Failed to send OTP: {e}")
        return None, None

# Streamlit App
st.title("Login with OTP")


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

email = st.text_input("Enter Email:")
generated_otp = None
otp_timestamp = None

if st.button("Request OTP"):
    if not email:
        st.error("Please enter an email!")
    else:
        generated_otp, otp_timestamp = send_otp(email)
        if generated_otp:
            st.success("OTP Sent! Check your email.")
            st.session_state["generated_otp"] = generated_otp
            st.session_state["otp_timestamp"] = otp_timestamp
            st.session_state["otp_requested"] = True

if "otp_requested" in st.session_state:
    otp = st.text_input("Enter OTP:", max_chars=6)

    if st.button("Verify OTP"):
        if time.time() - st.session_state["otp_timestamp"] > 60:
            st.error("OTP has expired! Request a new one.")
        elif otp == st.session_state["generated_otp"]:
            st.success("OTP Verified Successfully! ✅")
        else:
            st.error("Invalid OTP. ❌ Try again.")

