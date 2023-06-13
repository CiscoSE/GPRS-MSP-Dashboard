import requests
import credentials

# Replace <YOUR_ACCESS_TOKEN> with your bot's access token
ACCESS_TOKEN = credentials.BOT_ACCESS_TOKEN

# Function to retrieve a list of webhooks
def get_webhooks():
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get('https://webexapis.com/v1/webhooks', headers=headers)
    return response.json().get('items', [])

# Function to delete a webhook by ID
def delete_webhook(webhook_id):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    response = requests.delete(f'https://webexapis.com/v1/webhooks/{webhook_id}', headers=headers)
    if response.status_code == 204:
        print(f"Webhook with ID '{webhook_id}' deleted successfully.")
    else:
        print(f"Failed to delete webhook with ID '{webhook_id}'.")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

# Main entry point
if __name__ == '__main__':
    # Retrieve a list of webhooks
    webhooks = get_webhooks()
    
    # Delete each webhook
    for webhook in webhooks:
        webhook_id = webhook.get('id')
        delete_webhook(webhook_id)
    
    # Replace <YOUR_WEBHOOK_URL> with the URL that should receive the webhook events
    WEBHOOK_URL = 'https://4bd5-2001-428-ce01-2320-5c7-fcef-8b5e-32b7.ngrok-free.app'

    # Define the webhook payload
    webhook_data = {
        'name': 'My Webhook',
        'targetUrl': WEBHOOK_URL,
        'resource': 'messages',
        'event': 'created',
        'filter': 'roomId=Y2lzY29zcGFyazovL3VzL1JPT00vYjc3ZjFhYTAtZDQ4Ni0xMWVkLThjOTgtMGIyNDQ4YjZmYzU4'  # Replace with the roomId where your bot is listening
    }

    # Send the request to register the webhook
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}
    response = requests.post('https://api.ciscospark.com/v1/webhooks', json=webhook_data, headers=headers)

    # Check the response status code
    if response.status_code == requests.codes.ok:
        print('Webhook registered successfully')
    else:
        print('Error registering webhook: ' + response.text)

