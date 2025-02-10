import json
import random
import os

def create_profile(email, smtp_server, smtp_port, smtp_username, smtp_password, name, min_interval=21, max_interval=31):
	"""
	Creates a profile JSON file containing email sending details.
	"""
	profile = {
		"email": email,
		"smtp_server": smtp_server,
		"smtp_port": smtp_port,
		"smtp_username": smtp_username,
		"smtp_password": smtp_password,
		"name": name,
		"send_interval": random.randint(min_interval, max_interval) # Interval in minutes
	}

	filename = f"profiles/{email}.json"
	os.makedirs("profiles", exist_ok=True)

	with open(filename, "w", encoding="utf-8") as f:
		json.dump(profile, f, indent=4)

	print(f"Profile created: {filename}")
	return filename

def load_profiles():
	"""Loads all profiles from the profiles directory."""
	profiles = []
	os.makedirs("profiles", exist_ok=True)

	for filename in os.listdir("profiles"):
		if filename.endswith(".json"):
			with open(os.path.join("profiles", filename), "r", encoding="utf-8") as f:
				profiles.append(json.load(f))

	return profiles

def delete_profile(email):
	"""Deletes a profile by email."""
	filename = f"profiles/{email.replace('@', '_at_')}.json"
	if os.path.exists(filename):
		os.remove(filename)
		print(f"Profile deleted: {filename}")
	else:
		print("Profile not found.")

def load_smtp_profiles():
    """Load all SMTP profiles from JSON files in the profiles folder."""
    profiles = []
    for file in os.listdir("profiles"):
        if file.endswith(".json"):
            with open(os.path.join("profiles", file), "r", encoding="utf-8") as f:
                profiles.append(json.load(f))
    return profiles
