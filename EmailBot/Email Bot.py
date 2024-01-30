import os.path
import csv
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

"""
This script sends emails to all teams in the Build a CubeSat Challenge. It can be modified to send other emails,
just make sure you update the email mapping from the csv file and make sure your body is in html format.

To authenticate follow the guide here: https://developers.google.com/gmail/api/quickstart/python
"""

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

SOURCE_CSV = "test.csv"

def create_message(sender, to, cc, subject, body_html):
    """
    Create a message for an email.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['cc'] = cc
    message['from'] = sender
    message['subject'] = subject

    # Add the HTML body with the hyperlink
    message.attach(MIMEText(body_html, 'html'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_message(service, sender, to, cc, subject, body_html):
    """
    Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        sender: Email address of the sender.
        to: Email address of the receiver.
        cc: Email address of the cc.
        subject: The subject of the email message.
        body_html: The HTML body of the email message.
    """
    message = create_message(sender, to, cc, subject, body_html)
    try:
        print(f"Sending email to coach {to} and mentor {cc}")
        sent_message = service.users().messages().send(userId=sender, body=message).execute()
        print(f'Message Id: {sent_message["id"]}')
        return sent_message
    except Exception as error:
        print(f'An error occurred: {error}')


def main():
    """
    Reads csv file and sends emails to all teams in the Build a CubeSat Challenge
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    #read csv file and stores it as list of lists
    with open(SOURCE_CSV, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        #remove empty rows
        data = [row for row in data if row]
    
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        
        #iterate through each row in the csv file and send an email to the team
        for row in data[1:]:
            info = row[0], row[7], row[8], row[9]
            teamname, mentorname, mentoremail, teamemail = info
            body_html = f"""Hi {teamname},<p>Your mentor for the 2023/2024 Build a CubeSat Challenge will be <a href='mailto:{mentoremail}'>{mentorname}</a>.
            Please work with {mentorname.split(' ')[0]} to schedule a meeting time that works for your team. You are encouraged to meet with your mentor every other week for the duration of the challenge.</p>
            <p>For the safety of your team and our mentors, we ask that students avoid any one-on-one interactions with your mentor. Please keep in mind the following policies:</p>
            <ol type='1'>
            <li>Students should always include another adult when emailing their mentor.  We recommend CC'ing your team coach or bwsi_bacc@mit.edu
            Your team coach should be present during student meetings with your mentor</li>
            <li>Your team coach should be present during student meetings with your mentor</li>
            <li>If a student is alone in a Zoom (or other online meeting) room with a mentor, leave the room until other students or your team coach can join as well</li>
            </ol>
            <p>As always, please reach out on Piazza or email us at bwsi_bacc@mit.edu with any questions.</p>
            <p>Thank you,
            <br>BWSI Build a CubeSat Challenge Team</p>"""
            send_message(service, "me", teamemail, mentoremail, f"{teamname}- mentor assignment", body_html)
            
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()