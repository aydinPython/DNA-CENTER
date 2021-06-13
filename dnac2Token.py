import requests
import base64
import json

# DNA CENTER SANDBOX VARIABLES

USERNAME = 'devnetuser' 
PASSWORD = 'Cisco123!'
BASE_URL = 'https://sandboxdnac2.cisco.com'
PORT = ':443'
REQUEST_RETRIES = 5


def send_request(method,url,payload,headers):

    try_count = 0

    while True:

        try_count += 1
        
        try:
            
            response = requests.request(method, url = url, headers = headers, data = payload)
            if response:
                return response.json()
            response.raise_for_status()

        except requests.ConnectTimeout:
            
            if try_count < REQUEST_RETRIES:
                continue
            else:
                raise



def get_token():

    credential_string = f'{USERNAME}:{PASSWORD}'
    cred = base64.b64encode(credential_string.encode('utf8')).decode('utf8')

    url = BASE_URL + PORT + '/api/system/v1/auth/token'
    print(' Connection to ---> \n', url)
    print(' Getting Token\n')

    payload = {}

    headers = {'Authorization': f'Basic {cred}'}
    resp = send_request('POST', url = url, payload = payload , headers = headers)

    
    return resp['Token']



def get_devices_list(token):

    url = BASE_URL + PORT + '/dna/intent/api/v1/network-device'
    payload = {}
    headers = {'x-auth-token':token}

    resp = send_request('GET', url = url, payload = payload, headers = headers)
    return resp



if __name__ == '__main__':

    token = get_token()
    print(token+'\n')

    devices = get_devices_list(token)

    print('DNA CENTER DEVICES LIST\n\n')
    
    for device in devices['response']:
        print(f'hostname    :{   device["hostname"]}')
        print(f'ip address  :{   device["managementIpAddress"]}')
        print(f'device type :{   device["type"]}')
        print('=========================================================')
        if device["hostname"] == 'T1-1':
            break
    print()

    

    