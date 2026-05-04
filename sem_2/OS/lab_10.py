import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import email

email_from = "vikingragnar912@gmail.com"
password = "lgmwvdlvrxvmtnrx"
email_to = "ensherman5@gmail.com"

msg = MIMEMultipart()
msg["From"] = email_from
msg["To"] = email_to
msg["Subject"] = "Test email from Python"

body = "Hello! This is a test email with attachment."
msg.attach(MIMEText(body, "plain"))

filename = "test.txt"
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename={filename}")
msg.attach(part)

log = open("smtp_log.txt", "w")

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    server.login(email_from, password)
    server.send_message(msg)

    log.write("Email sent successfully\n")

except Exception as e:
    log.write(str(e))

finally:
    server.quit()
    log.close()

email_user = "vikingragnar912@gmail.com"
log = open("imap_log.txt", "w")

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    mail.login(email_user, password)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()

    print("Всего писем:", len(mail_ids))
    log.write(f"Total emails: {len(mail_ids)}\n\n")

    for i in mail_ids[-10:]:
        status, msg_data = mail.fetch(i, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"]
        sender = msg["from"]

        print(f"From: {sender} | Subject: {subject}")
        log.write(f"From: {sender} | Subject: {subject}\n")

    latest_email_id = mail_ids[-1]
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    print("\n=== Последнее письмо ===")
    print("From:", msg["from"])
    print("Subject:", msg["subject"])

    log.write("\n=== Last email ===\n")
    log.write(f"From: {msg['from']}\n")
    log.write(f"Subject: {msg['subject']}\n")

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                print("Body:", body[:200])
                log.write(f"Body: {body[:200]}\n")
                break
    else:
        body = msg.get_payload(decode=True).decode()
        print("Body:", body[:200])
        log.write(f"Body: {body[:200]}\n")

except Exception as e:
    log.write(str(e))

finally:
    mail.logout()
    log.close()