Project for COMP-7082

For Server:
    Create/ Slash start the virtual environment

    Install the Requirements:
        pip install -r requirements.txt
        run: uvicorn server:app --reload

For RabbitMQ:
    docker run -d --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management

To use notification and email service:
    make sure RabbitMQ is installed or Docker is up
    python3 monitoring_service.py
    python3 email_service.py