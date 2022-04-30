import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

SERVER_ADDR = "http://127.0.0.1:5000"

def get_cookie():
    headers = {
        "Host": "localhost:5000",
        "User-Agent": "Bot/1.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }

    data = {
        "username": "admin",
        "password": "CookieMonster123!$"
    }

    req = requests.post(SERVER_ADDR+"/login", headers=headers, data=data)
    # print(f"login req status: {req.status_code}")
    cookiejar = req.history[0].cookies
    cookie = cookiejar.get_dict()['session']
    # print(f"admin cookie: {cookie}")

    return cookie

def xss(cookie):
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-sync')
    options.add_argument('--disable-translate')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--metrics-recording-only')
    options.add_argument('--mute-audio')
    options.add_argument('--no-first-run')
    options.add_argument('--dns-prefetch-disable')
    options.add_argument('--safebrowsing-disable-auto-update')
    options.add_argument('--media-cache-size=1')
    options.add_argument('--disk-cache-size=1')
    try:
        browser = webdriver.Firefox(options=options)
    except Exception as e:
        print(e)
    browser.get(SERVER_ADDR)
    browser.add_cookie({
        'name': 'session',
        'value': cookie
    })
    
    try:
        browser.get(SERVER_ADDR+"/messages")
        WebDriverWait(browser, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')
    except:
        print("selenium failed")
        pass
    finally:
        browser.quit()

def run():
    cookie = False
    while not cookie:
        try:
            cookie = get_cookie()
        except:
            time.sleep(5)
            pass
    
    try:
        xss(cookie)
    except:
        pass

if __name__ == "__main__":
    run()