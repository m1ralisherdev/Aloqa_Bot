import requests
import uuid

def create_transactions():
    charge_id = str(uuid.uuid4())

    url = "https://checkout.paycom.uz"

    # Data to be sent in the POST request
    data = {
        'merchant': '672b8224c628bf0c13f3c4ef',
        'amount': '500000',
        'account[charge_id]': charge_id
    }
    # Sending POST request
    response = requests.post(url, data=data)
    # Check the response
    if response.status_code == 200:
        # Extract and print the form name="redirect"
        if '<form name="redirect"' in response.text:
            start_index = response.text.find('<form name="redirect"')
            end_index = response.text.find('>', start_index) + 1
            html_content = response.text
            start = html_content.find('property="og:description" content="') + len(
                'property="og:description" content="')
            end = html_content.find('"', start_index)
            meta_description = html_content[start:end]

            # Split the content to find 'Номер чека'
            parts = meta_description.split(',')
            check_id = parts[1].split(':')[1]
            a = 'https://checkout.paycom.uz/' + response.text[start_index:end_index].split('/')[5]
            b = response.text[start_index:end_index].split('/')[5]
            return [a,b]

        else:
            print("Redirect form not found in the response.")
    else:
        print(f"Failed to send request. Status code: {response.status_code}")



def check_transactions(check_id):
    a = "SmchgGopUu5rAxpCsjOpr64ridAP3VrrDutv"
    b = "672b8224c628bf0c13f3c4ef"
    url = "https://checkout.paycom.uz/api"
    headers = {
        "X-auth": f"{b}:{a}",
        "Content-Type": "application/json"
    }
    payload = {
        "id": check_id,  # This is a random ID for your request
        "method": "receipts.check",
        "params": {
            "id": f"{check_id}" # Your transaction ID
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        # Check if the request was successful
        if 'result' in response_data:
            transaction_state = response_data['result'].get('state')
            # If the payment was successful
            if transaction_state != 0:
                return True # Payment successful
            else:
                return False # Payment not successful or in another state
        else:
            # Handle errors
            error_message = response_data.get('error', {}).get('message', 'Unknown error')
            print(f"Error: {error_message}")
    except Exception as e:
        print(f"An error occurred while checking transaction status: {e}")
