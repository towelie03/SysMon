import subprocess
import sys

def main():
    try:
        # Start the monitoring service
        print("Starting Monitoring Service...")
        monitoring_process = subprocess.Popen([sys.executable, "monitoring_service.py"])

        # Start the email consumer
        print("Starting Email Consumer...")
        email_process = subprocess.Popen([sys.executable, "email.py"])

        # Wait for both processes to complete (this will run indefinitely unless terminated)
        monitoring_process.wait()
        email_process.wait()

    except KeyboardInterrupt:
        print("\nShutting down...")
        # Terminate both processes on interrupt
        monitoring_process.terminate()
        email_process.terminate()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
