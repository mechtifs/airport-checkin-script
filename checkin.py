import requests
import telebot
import time


# Information
url = 'example.com'
email = 'example@example.com'
passwd = 'password'
botapi = 'botapi'
teleid = 'teleid'

# Main function
headers = {
    'Host': url,
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="98"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://'+url,
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://'+url+'/user/login?redirect=%%2F',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}
url = 'https://www.'+url
r = requests.post(url+'/api/token', headers=headers,
                  json={'email': email, 'passwd': passwd})
headers.update({'Access-Token': r.json()['token']})
headers['Referer'] = url+'/user/index'
time.sleep(2)
r = requests.get(url+'/api/user/checkin', headers=headers)

# Telegram bot API
bot = telebot.TeleBot(botapi)
if r.json()['ret']:
    checkin = 'Gained '+r.json()['result'].split()[1]+'MB!'
else:
    checkin = 'Already checked in today!'
r = requests.get(url+'/api/user/info',
                 headers=headers).json()['result']
while True:
    try:
        bot.send_message(teleid, checkin+'\nUsed: '+r['usedTraffic']+'\nUnused: '+r['unusedTraffic']+'\nUnconverted: '+str(
            r['data']['transfer_checkin']//1048576)+'MB'+'\nReset: '+r['nextRestTraffic'])
    except requests.exceptions.ConnectionError:
        continue
    break
