import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(profile, reach):
	"""Send an email using SMTP profile credentials."""
	msg = MIMEMultipart()
	msg['From'], msg['To'], msg['Subject'] = profile.username, reach.email, reach.subject
	msg.attach(MIMEText(reach.get_current(), 'plain'))

	try:
		with smtplib.SMTP(profile.server, profile.port) as server:
			server.starttls()
			server.login(profile.username, profile.password)
			server.send_message(msg)
		print(f"✅ Email sent to {reach.email}")
		reach.proceed()
	except Exception as e:
		print(f"❌ Email failed: {e}")