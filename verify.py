import smtplib
import dns.resolver

def get_mx_record(domain):
	try:
		return str(dns.resolver.resolve(domain, "MX")[0].exchange).rstrip(".")
	except Exception:
		return None

def verify(email):
	domain = email.split("@")[-1]
	mx_server = get_mx_record(domain)

	if not mx_server:
		return "Error: No MX record found"

	try:
		with smtplib.SMTP(mx_server, 25, timeout=10) as server:
			server.helo()
			server.mail("test@example.com")
			code, _ = server.rcpt(email)
			return code == 250 if code in (250, 550) else f"Unknown response: {code}"
	except Exception as e:
		return f"Error: {e}"