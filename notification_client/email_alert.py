import pika
import json
import smtplib
import os
from email.mime.text import MIMEText

print("Before SMTP initialization")

# Outlook SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "sysmon7082@gmail.com"
SENDER_PASSWORD = "ixlmehzicmyxjryj"  
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

if not RECEIVER_EMAIL:
    raise ValueError("Receiver email not provided. Set RECEIVER_EMAIL environment variable.")

def send_email_alert(subject, message, recipient_email):
    # Create the email content
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    try:
        # Connect to the Outlook SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
            print(f"Email sent to {recipient_email}: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def callback(ch, method, prop, body):
    # Parse the alert message from RabbitMQ
    alert = json.loads(body)
    alert_type, message, timestamp = alert.get("type"), alert.get("message"), alert.get("timestamp")
    
    # Prepare email details
    subject = f"System Alert: {alert_type}"
    email_message = f"Time: {timestamp}\n\nAlert: {alert_type}\n\nDetails: {message}"
    recipient_email = RECEIVER_EMAIL  # Replace with actual recipient email

    # Send the email alert
    send_email_alert(subject, email_message, recipient_email)
    
    # Acknowledge the message in the queue
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_email_consumer():
    # Connect to RabbitMQ and declare the queue
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='alerts_queue', durable=True)
    
    # Set up the consumer
    channel.basic_consume(queue='alerts_queue', on_message_callback=callback)
    print("Listening for alerts...")
    
    # Start consuming messages from the queue
    channel.start_consuming()

if __name__ == "__main__":
    # Run the email consumer
    start_email_consumer()