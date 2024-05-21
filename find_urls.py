import requests
from time import sleep

baseurl = "https://rutracker.net/forum/tracker.php?f="

def get_cookies():
    cookies = {}
    with open("cookies.txt", 'r') as f:
        for line in f:
            if not line.startswith("#") and len(line) > 1:
                line_fields = line.strip().split('\t')
                cookies[line_fields[5]] = line_fields[6]
    return cookies

def check_url(url, cookies):
    print(url, end = '\t')
    try:
        resp = requests.get(url, cookies=cookies)

        if len(resp.text) < 165400:
            print("bad")
        else:
            with open("urls.txt", "a") as f:
                f.write(url+"\n")
            print("OK")
    
    except:
        print("bad")


if __name__ == "__main__":
    cookies = get_cookies()
    position = 1

    while True:
        check_url(baseurl+str(position), cookies=cookies)
        position += 1
