import csv
from queue import Queue
from verify import verify
from profile import load_smtp_profiles
from worker import start_email_threads

def process_csv(file_path):
    """Read the CSV file and distribute emails across SMTP profiles."""
    profiles = load_smtp_profiles()
    if not profiles:
        print("⚠️ No SMTP profiles found in 'profiles' folder.")
        return

    email_queue = Queue()
    
    with open(file_path, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if verify(row['email']):
                email_queue.put((row['email'], row['subject'], row['body']))

    start_email_threads(profiles, email_queue)
