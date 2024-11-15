import random, os, ctypes, httpx, threading, time
from colorama import init, Fore
import sys
from fake_useragent import UserAgent
ua = UserAgent()

init()
os.system("cls||clear")

checked, available, valid_proxies, start_time = 0, 0, [], [], time.time()

usernames = list(open("usernames.txt", "r").read().splitlines()) if (os.path.isfile("usernames.txt") and os.path.getsize("usernames.txt") > 0) else (print("Put your usernames in usernames.txt"), input("Press Enter to exit..."), sys.exit())

def worker(usernames, thread_id):
    global check
    while check[thread_id] < len(usernames):
        while True:
            if not valid_proxies:
                continue
            proxy = random.choice(valid_proxies)
            headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "en-US,en;q=0.5","Cache-Control": "no-cache","Connection": "keep-alive","Host": "guns.lol","Pragma": "no-cache","Priority": "u=0, i","Sec-Fetch-Dest": "document","Sec-Fetch-Mode": "navigate","Sec-Fetch-Site": "none","Sec-Fetch-User": "?1","TE": "trailers","Upgrade-Insecure-Requests": "1","User-Agent": ua.random}
            try:
                response = httpx.get(f"https://guns.lol/{usernames[check[thread_id]]}", headers=headers, proxies=proxy)
                if response.status_code == 429:
                    continue
                break
            except:
                continue
        seek(usernames[check[thread_id]], response.cookies, headers)
        check[thread_id] += 1

def runner():
    threadsAmount = 100
    global check
    check = [0 for _ in range(threadsAmount)]
    for i in range(threadsAmount):
        sliced_combo = usernames[int(len(usernames) / threadsAmount * i) : int(len(usernames) / threadsAmount * (i + 1))]
        threading.Thread(target=worker,args=(sliced_combo,i,)).start()


def seek(username, cookie, headers):
    global checked, available
    while True:
        if not valid_proxies:
            continue
        proxy = random.choice(valid_proxies)
        try:
            response1 = httpx.get(f"https://guns.lol/{username}", headers=headers, cookies=cookie, proxies=proxy)
            if "Claim this name fast by clicking on the button below!" in response1.text:
                print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {username}")
                available+=1
                with open("hits.txt", "a") as file: file.write(username+"\n")
            elif response1.status_code == 429:
                continue
            else:
                print(f"{Fore.WHITE}[{Fore.RED}+{Fore.WHITE}] {username}")
        except:
            continue
        checked+=1
        break

def get_valid_proxies():
    for _ in range(10):
        try:
            with open("proxies.txt") as f:
                valid_proxies[:] = f.read().splitlines()
            break
        except:
            print(f"{Fore.WHITE}[{Fore.RED}-{Fore.WHITE}] Put proxies in proxies.txt")
            time.sleep(3)
    else:
        print(f"{Fore.WHITE}[{Fore.RED}-{Fore.WHITE}] Put proxies in proxies.txt")


def proxier():
    while True:
        get_valid_proxies()
        time.sleep(random.randint(5,30))

threading.Thread(target=proxier).start()

def updateTitle():
    global checked, available
    while True: ctypes.windll.kernel32.SetConsoleTitleW(f"Usernames Checked: {checked} - Available: {available} - Proxies: {len(valid_proxies)}")

threading.Thread(target=updateTitle).start(); threading.Thread(target=runner).start()