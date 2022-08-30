import requests
import json

if __name__ == '__main__':
    token_url = "https://api.ingrammicro.com:443/oauth/oauth30/token"

    test_api_url = "https://api.ingrammicro.com:443/resellers/v6/catalog/?pageNumber=1&pageSize=100&keyword=Epson"

    #client (application) credentials on apim.byu.edu
    client_id = 'j1H7bixxxxxxxxxxxxxxxxxxxxxxxxxx'
    client_secret = 'uOIPhxxxxxxxxxx'

    #step A, B - single call with client credentials as the basic auth header - will return access_token
    data = {'grant_type': 'client_credentials'}

    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

    #print(access_token_response.headers)
    #print(access_token_response.text)

    tokens = json.loads(access_token_response.text)

    #print("access token: " + tokens['access_token'])

    #step B - with the returned access_token we can make as many calls as we want

    api_call_headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': 'Bearer ' + tokens['access_token'],
                        'IM-CustomerNumber': '20-222222',
                        'IM-CorrelationID': 'fbac82ba-cf0a-4bcf-fc03-0c508457f219-bw0a102j',
                        'IM-CountryCode': 'BR',
                        'IM-SenderID': 'SampleUser-Best-Buy'}
                    
    api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)
    print(api_call_response.text)
