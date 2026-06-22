import imaplib
import email
import re
import time


def get_otp(max_wait=60):
    username = "kayfinmetrics1@gmail.com"
    password = "veip zrrx yfvj shit"

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")

    start_time = time.time()

    while time.time() - start_time < max_wait:

        result, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        for email_id in reversed(email_ids[-10:]):

            result, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() in ["text/plain", "text/html"]:
                        try:
                            body += part.get_payload(decode=True).decode()
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode()
                except:
                    body = ""

            match = re.search(r"\b\d{6}\b", body)

            if match:
                otp = match.group()


                print("OTP:", otp)

                return otp

        time.sleep(5)

    raise Exception("OTP not received")