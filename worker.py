import time
import threading
from queue import Queue
from email_sender import send_email

def send_email_thread(profile, email_queue):
    """Thread function to send emails using a specific SMTP profile."""
    while not email_queue.empty():
        to_email, subject, body = email_queue.get()
        time.sleep(profile["send_interval"] * 60)  # Convert minutes to seconds
        send_email(profile, to_email, subject, body)

def start_email_threads(profiles, email_queue):
    """Start threads for sending emails using multiple profiles."""
    threads = [threading.Thread(target=send_email_thread, args=(profile, email_queue)) for profile in profiles]
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
