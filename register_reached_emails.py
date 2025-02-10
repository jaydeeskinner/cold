import os
import csv
import sys

os.makedirs("reached", exist_ok=True)
with open(sys.argv[1], newline='', encoding='utf-8') as file:
	for row in csv.DictReader(file):
		email = row.get("email")
		if email:
			email_file_path = f"reached/{email}"
			if not os.path.exists(email_file_path):
				with open(email_file_path, 'w') as f:
					f.write("1")