import os
import re
import subprocess
from notification_client.notification_alert import start_monitoring
from notification_client.email_alert import start_email_consumer
import threading

# Email validation function
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


if __name__ == "__main__":
    
    receiver_email = os.getenv("RECEIVER_EMAIL")
    if not receiver_email or not is_valid_email(receiver_email):
        raise ValueError("Invalid or missing RECEIVER_EMAIL environment variable.")
    print(f"Using receiver email: {receiver_email}")
    
    # Start email and notification logic in separate threads
    notification_thread = threading.Thread(target=start_monitoring)
    email_thread = threading.Thread(target=start_email_consumer)
    
    notification_thread.start()
    email_thread.start()
    
    # Wait for both threads to finish
    email_thread.join()
    notification_thread.join()
