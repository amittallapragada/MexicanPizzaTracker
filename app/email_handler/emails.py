import os 
from io import StringIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, BaseLoader
import requests 
from requests.auth import HTTPBasicAuth

#authenticate
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
login_email = str(os.environ.get("GMAIL_EMAIL"))
login_password = str(os.environ.get("GMAIL_PASSWORD"))
smtpObj.login(login_email, login_password)
print("email service successfully authenticated")


#by default always send to myself for now
sender = 'amithypeeats@gmail.com'
receivers = 'amittallapragada@gmail.com'

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""
def read_email_template(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    text_file = open(f"{dir_path}/templates/mjml_templates/{file_name}")
    data = text_file.read()
    text_file.close()
    return data 

def send_email(html=None, text=None, subject=None):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receivers
        # Create the body of the message (a plain-text and an HTML version).
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        smtpObj.sendmail(sender, receivers, msg.as_string())         
        print("Successfully sent email")
    except smtplib.SMTPException as e:
        print(f"Error: unable to send email: {e}")

def render_template(render_string, template_req_params):
    template = Environment().from_string(render_string)
    hydrated_template =  template.render(**template_req_params)
    return hydrated_template

def render_mjml_to_html(template_name, params, use_cache=False):
    mjml_string = read_email_template(f"{template_name}.mjml")
    mjml_template = render_template(mjml_string, params)
    MJML_URL = "https://api.mjml.io/v1/render"
    body = {
        "mjml":mjml_template
    }
    basic = HTTPBasicAuth('af1b46e5-eee5-4d8a-87b9-4d63bf08af74', 'b5331fb0-8458-4bfd-bf20-930d82c60c02')
    response = requests.post(MJML_URL, json=body, auth=basic)
    if response.ok:
        data = response.json()
        return data['html']
    else:
        html_params = ["<html>"]
        for key,value in params.items():
            html_params.append(f"<li>{key} : {value}</li>")
        html_params.append("</html>")
        return "\n".join(html_params)

def generate_email(template_name='feature_request', params={"from_email":'a@a', 'message':'asdasdasd', 'subject':"Feature Request"}):
    try:
        html = render_mjml_to_html(template_name, params)
        text = str(params)
        send_email(html, text, params['subject'])
    except Exception as e:
        raise e


