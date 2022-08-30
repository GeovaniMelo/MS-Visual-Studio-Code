import traceback
import httplib2
import difflib
import json
import webbrowser
import requests as requests
import time

if __name__ == '__main__':
    token_url = "https://www.nuvemshop.com.br/apps/authorize/token"
                
    client_id = '35xx'
    client_secret = '70ngJxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    access_token = '414fexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    api_call_headers = {
    'Authentication': 'bearer ' + access_token,
    'Content-Type': 'application/json',
    'User-Agent': 'AdcProdutos (geovanibarbosa@live.com)'
    }

    vet = []
    for i in range(1, 10):
        a = 1
        while(a == 1):
            try: 
                api_call_url = "https://api.nuvemshop.com.br/v1/18xxxxx/products?page={}&per_page=200".format(str(i))
                api_call_response = requests.get(api_call_url, headers=api_call_headers)
                vet.append(json.loads(api_call_response.text))
                time.sleep(2)
                a = 0
            except: 
                print(traceback.print_exc())

    for i in range(len(vet)): 
        for j in range(len(vet[i])): 
            a = 1
            while (a == 1):
                try: 
                    api_call_url = "https://api.nuvemshop.com.br/v1/18xxxxx/products/{}".format(str(vet[i][j]['id']))
                    api_call_response = requests.delete(api_call_url, headers=api_call_headers)
                    print(api_call_response)
                    time.sleep(2)
                    a = 0
                except: 
                    print(traceback.print_exc())

