from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create folder for storing contact data
if not os.path.exists("contacts"):
    os.makedirs("contacts")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/all_projects", response_class=HTMLResponse)
async def all_projects(request: Request):
    return templates.TemplateResponse("all_projects.html", {"request": request})

@app.get("/prohousing", response_class=HTMLResponse)
async def prohousing(request:Request):
    return templates.TemplateResponse("prohousing.html",{"request":request})





# ======================================================
#  CONTACT FORM API: Save JSON + Send Email
# ======================================================
@app.post("/submit-contact")
async def submit_contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    
    data = {
        "name": name,
        "email": email,
        "message": message,
        "timestamp": str(datetime.now())
    }

    filename = f"contacts/{name.replace(' ', '_').lower()}_{int(datetime.now().timestamp())}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    send_email_to_me(name, email, message)

    return JSONResponse({"status": "success", "message": "Message received!"})


def send_email_to_me(name, email, message):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_APP_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    # Debug prints
    print("SENDER:", sender_email)
    print("PASS:", sender_password)
    print("RECV:", receiver_email)

    subject = f"New Contact Form Message From {name}"
    body = f"""
Name: {name}
Email: {email}

Message:
{message}
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Email failed:", e)
