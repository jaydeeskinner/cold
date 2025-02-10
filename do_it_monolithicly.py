import os
import sys
import json
import csv
import smtplib
import random
import time
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from verify import verify

REACHED_DIR, SEQUENCE_DIR, SENDERS_FILE = "reached", "sequences", "senders.json"

def load_json(file):
	if not os.path.exists(file):
		raise FileNotFoundError(f"{file} not found")
	with open(file, "r", encoding="utf-8") as f:
		return json.load(f)

def get_sequence_files():
	return [os.path.join(SEQUENCE_DIR, f) for f in os.listdir(SEQUENCE_DIR) if f.endswith(".ml")] if os.path.isdir(SEQUENCE_DIR) else []

def read_sequence(path):
	with open(path, "r", encoding="utf-8") as f:
		parts = f.read().split("---", 1)
		if len(parts) < 2:
			raise ValueError(f"Invalid format in {path}")
		return parts[0].strip(), parts[1].strip()

def render_template(text, sender_name, row):
	text = text.replace("{{sender}}", sender_name)
	for k, v in row.items():
		text = text.replace(f"{{{{{k}}}}}", v)
	return text

def send_email(sender, to_addr, subject, body):
	msg = MIMEMultipart()
	msg["From"], msg["To"], msg["Subject"] = sender["email"], to_addr, subject
	msg["List-Unsubscribe"] = f"<https://mail.{sender["domain"]}/unsubsribe?{to_addr}>"
	msg.attach(MIMEText(body, "plain"))
	try:
		with smtplib.SMTP(sender["server"], sender["port"]) as smtp:
			smtp.starttls()
			smtp.login(sender["username"], sender["password"])
			smtp.sendmail(sender["email"], to_addr, msg.as_string())
			print(f"{sender["email"]} -> {to_addr} ({subject})")
	except Exception as e:
		print(f"Email failed: {e}")

def process_sender(sender, recipients, sequences):
	time.sleep(sender["interval"] * random.random())
	for row in recipients:
		if (email := row.get("email")) and verify(email):
			subj, body = map(lambda x: render_template(x, sender["fullname"], row), read_sequence(random.choice(sequences)))
			try:
				send_email(sender, email, subj, body)
				os.makedirs(REACHED_DIR, exist_ok=True)
				with open(os.path.join(REACHED_DIR, email), "w", encoding="utf-8") as f:
					f.write("1")
			except Exception as e:
				print(f"Failed to send to {email}: {e}")
			time.sleep(sender["interval"] + random.random() * sender["variance"])

def filter_recipients(recipients):
	return [r for r in recipients if not os.path.exists(os.path.join(REACHED_DIR, r.get("email", "")))]

def run_senders(senders, recipients):
	sequences = get_sequence_files()
	if not sequences or not senders or not (recipients := filter_recipients(recipients)):
		print("No sequences, senders, or new recipients.")
		return
	threads = [threading.Thread(target=process_sender, args=(sender, recipients[i::len(senders)], sequences)) for i, sender in enumerate(senders)]
	[t.start() for t in threads]
	[t.join() for t in threads]

def main(csv_file):
	with open(csv_file, newline="", encoding="utf-8") as f:
		recipients = list(csv.DictReader(f))
	if recipients:
		run_senders(load_json(SENDERS_FILE), recipients)
	else:
		print("No recipients found.")

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python script.py <csv_file>")
		sys.exit(1)
	main(sys.argv[1])