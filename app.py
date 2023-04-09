import logging
import socket
import boto3

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up SQS client
sqs = boto3.client('sqs', region_name='us-east-1')
queue_url = 'https://sqs.us-east-1.amazonaws.com/<your-account-id>/<your-queue-name>'

# Set up UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 514))

# Listen for messages
while True:
    message, address = udp_socket.recvfrom(4096)
    logging.info(f'Received syslog message from {address[0]}: {message.decode()}')

    # Send message to SQS
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message.decode())
    logging.info(f'Sent message to SQS with message ID {response["MessageId"]}')
