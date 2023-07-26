import requests

def load_cookies_from_file(file_path):
    with open(file_path, 'r') as f:
        cookies_data = f.read()
    cookies_array = cookies_data.split('###')
    return cookies_array

cookies_file_path = 'Accounts/cookies.txt'
cookies_array = load_cookies_from_file(cookies_file_path)


def convert(cookies_list):
    headers = {
        "Host": "accovod.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "1126",
        "Origin": "https://accovod.com",
        "Connection": "keep-alive",
        "Referer": "https://accovod.com/cookieConverter/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "TE": "trailers"
    }

    url = "https://accovod.com/cookieConverter/"
    
    for cookie_data in cookies_list:
        data = {"cookie": cookie_data}
        response = requests.post(url, headers=headers, data=data)
        print(response.text)
        
        
cookies_list = load_cookies_from_file("Accounts/cookies.txt")
convert(cookies_list)