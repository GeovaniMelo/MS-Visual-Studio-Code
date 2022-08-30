from email import header
import json
import time
from h11 import Data
import requests

def get_access_token():
        
        headers = {'Accept':  'application/json'}
        
        url_autorize = 'https://www.nuvemshop.com.br/apps/42xx/authorize'

        url_token = 'https://www.nuvemshop.com.br/apps/authorize/token'

        payload = {
            'client_id': '42xx',
            'client_secret': '3wCaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'grant_type': 'authorization_code',
            'code': '50a689xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        }

        resp = requests.post(url_token, data=payload, headers=headers)
                            
        print(resp.text)

if __name__ == '__main__': 
    token_url = "https://www.nuvemshop.com.br/apps/authorize/token"
    api_url = "https://api.nuvemshop.com.br/v1/18xxxxx/shipping_carriers"

    client_id = '42xx'
    client_secret = '3wCaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    access_token = '3501d9exxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    api_call_headers = {
    'Authentication': 'bearer ' + access_token,
    'Content-Type': 'application/json',
    'User-Agent': 'TransportadorasPersonalizadas (geovanibarbosa@live.com)'
    }

    api_call_payload = json.dumps({ 
        "name": "Jadlog",
        "callback_url": "https://www.bling.com.br/Api/v2/webhook/kabum/2038xxxxx/freight",
        "types": "ship"
    })

    #api_call_response = requests.get(api_url, headers=api_call_headers)
    api_call_response = requests.post(api_url, data=api_call_payload, headers=api_call_headers)
    print(api_call_response.text)

