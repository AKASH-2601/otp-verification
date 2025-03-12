import smtplib
import random
import string
import time
import tkinter as tk
from tkinter import messagebox
from threading import Thread


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_otp(receiver_email):
    sender_email = "akash26242931@gmail.com" 
    sender_password = "sxyv poir uylt blfx"

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
        messagebox.showerror("Error", f"Failed to send OTP: {e}")
        return None, None


def verify_otp():
    global generated_otp, otp_timestamp
    user_otp = otp_entry.get()
    if time.time() - otp_timestamp > 60:
        messagebox.showerror("Error", "OTP has expired! Request a new one.")
        return
    
    if user_otp == generated_otp:
        messagebox.showinfo("Success", "OTP Verified Successfully! ✅")
        root.quit()
    else:
        messagebox.showerror("Error", "Invalid OTP. ❌ Try again.")

def countdown():
    timer_label = tk.Label(root, text="Time Left: 60s", font=("Arial", 12))
    timer_label.pack(pady=10)
    global otp_timestamp
    remaining_time = 60
    while remaining_time > 0:
        timer_label.config(text=f"Time Left: {remaining_time}s")
        time.sleep(1)
        remaining_time -= 1
    timer_label.config(text="OTP Expired!")


def request_otp():
    global generated_otp, otp_timestamp
    email = email_entry.get()
    if not email:
        messagebox.showerror("Error", "Please enter an email!")
        return
    
    generated_otp, otp_timestamp = send_otp(email)
    if generated_otp:
        messagebox.showinfo("Success", "OTP Sent! Check your email.")
        Thread(target=countdown, daemon=True).start()


root = tk.Tk()
root.title("Login with OTP")
root.geometry("400x300")

tk.Label(root, text="Enter Email:").pack(pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.pack(pady=5)

tk.Button(root, text="Request OTP", command=request_otp).pack(pady=5)

tk.Label(root, text="Enter OTP:").pack(pady=5)
otp_entry = tk.Entry(root, width=10)
otp_entry.pack(pady=5)

tk.Button(root, text="Verify OTP", command=verify_otp).pack(pady=5)

root.mainloop()
