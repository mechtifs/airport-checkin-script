import requests


base_url = 'https://example.com'
email = 'example@example.com'
passwd = 'password'

if __name__ == '__main__':
    r = requests.post(base_url+'/api/token', json={'email': email, 'passwd': passwd})
    r = requests.get(base_url+'/api/user/checkin', headers={'Access-Token': r.json()['token']})
    print(r.json())
