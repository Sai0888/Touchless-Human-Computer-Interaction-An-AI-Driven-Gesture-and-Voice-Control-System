import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import time

# Simulated login credentials
USERNAME = "admin"
PASSWORD = "123"

def validate_login():
    user = entry_username.get()
    pwd = entry_password.get()

    if user == USERNAME and pwd == PASSWORD:
        root.destroy()
        launch_control_app()
    else:
        messagebox.showerror("Access Denied", "Invalid Username or Password")

def launch_control_app():
    subprocess.call([sys.executable, "gesture_and_voice_control.py"])

def exit_app():
    root.destroy()

def show_login():
    global root
    root = tk.Tk()
    root.title("Gesture & Voice Control - Login")
    
    # Fullscreen
    root.state('zoomed')
    root.configure(bg="#3498db")

    # Top frame
    top_frame = tk.Frame(root, bg="#6dd5fa", height=300)
    top_frame.pack(fill="x")

    bottom_frame = tk.Frame(root, bg="#3498db")
    bottom_frame.pack(fill="both", expand=True)

    # Shadow Frame
    shadow = tk.Frame(root, bg="#2d3436", bd=0)
    shadow.place(relx=0.5, rely=0.5, anchor="center", width=460, height=460)

    # Main Login Frame
    frame = tk.Frame(root, bg="#f1f2f6", bd=8, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=450)

    # Title
    tk.Label(frame, text="Gesture & Voice Control", font=("Segoe UI", 24, "bold"), bg="#f1f2f6", fg="#2c3e50").pack(pady=(20, 10))
    tk.Label(frame, text="Touchless Human-Computer Interaction", font=("Segoe UI", 14), bg="#f1f2f6", fg="#636e72").pack(pady=(0, 20))

    # Username
    tk.Label(frame, text="Username", font=("Segoe UI", 13), bg="#f1f2f6", fg="#34495e").pack(pady=(5, 2))
    global entry_username
    entry_username = tk.Entry(frame, font=("Segoe UI", 14), width=28, bd=0, bg="#dfe6e9", relief="flat", highlightbackground="#00cec9", highlightthickness=2)
    entry_username.pack(pady=(0, 10))

    # Password
    tk.Label(frame, text="Password", font=("Segoe UI", 13), bg="#f1f2f6", fg="#34495e").pack(pady=(5, 2))
    global entry_password
    entry_password = tk.Entry(frame, font=("Segoe UI", 14), show="*", width=28, bd=0, bg="#dfe6e9", relief="flat", highlightbackground="#00cec9", highlightthickness=2)
    entry_password.pack(pady=(0, 10))

    # Forgot Password (visual only)
    tk.Label(frame, text="Forgot Password?", font=("Segoe UI", 10, "italic"), bg="#f1f2f6", fg="#0984e3", cursor="hand2").pack()

    # Login Button
    def on_enter(e):
        login_btn['background'] = '#00cec9'
    def on_leave(e):
        login_btn['background'] = '#0984e3'

    login_btn = tk.Button(frame, text="Login", font=("Segoe UI", 15, "bold"), bg="#0984e3", fg="white", activeforeground="white", width=20, pady=5, command=validate_login, bd=0, relief="ridge", cursor="hand2")
    login_btn.pack(pady=(10, 10))
    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)

    # Exit Button
    exit_btn = tk.Button(frame, text="Exit", font=("Segoe UI", 12), bg="#d63031", fg="white", activeforeground="white", width=10, pady=2, command=exit_app, bd=0, relief="ridge", cursor="hand2")
    exit_btn.pack(pady=(5, 10))

    # Footer
    tk.Label(root, text="© 2025 Gesture & Voice Project | All Rights Reserved", font=("Segoe UI", 12), bg="#3498db", fg="#dfe6e9").pack(side="bottom", pady=10)

    root.mainloop()

# Splash screen loading animation
splash = tk.Tk()
splash.overrideredirect(True)
splash.geometry("500x300+600+300")
splash.configure(bg="#1e272e")

tk.Label(splash, text="Gesture & Voice Control System", font=("Segoe UI", 22, "bold"), bg="#1e272e", fg="#00cec9").pack(expand=True)
tk.Label(splash, text="Loading...", font=("Segoe UI", 16), bg="#1e272e", fg="#dfe6e9").pack()

splash.update()
time.sleep(3)  # 3 seconds splash
splash.destroy()

# Show the actual login window
show_login()
