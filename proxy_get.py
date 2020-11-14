
import json
import requests
from lxml import etree
from p_tqdm import p_map
from fake_useragent import UserAgent

ua = UserAgent()
proxy_list = []
proxy_url = 'https://www.sslproxies.org/'   # 免費ip網站
test_url = 'http://icanhazip.com'           # 用來測試ip代理是否可用
head = {'User-Agent':ua.random}             # 設定隨機user

def get_html():
    res_proxy = requests.get(url=proxy_url,headers=head)
    page = etree.HTML(res_proxy.text)
    need = page.xpath('//tbody//tr')
    return need

def get_proxy(graph):
    for i in graph[:-8]:
        if i.xpath('td/text()'):
            proxy = f'{i.xpath("td/text()")[0]}:{i.xpath("td/text()")[1]}'
            proxy_list.append({"http":"http://"+proxy,"https":"https://"+proxy})

def test_proxy(proxy):
    try:
        res_test = requests.get(url=test_url, headers=head, proxies=proxy)
        if res_test.status_code == 200: pass
        else:
            print(f'delete no responds proxy: {proxy}')
            del proxy
    except: pass

def store_ip():
    with open('./proxies.json','w') as file:
        js = json.dumps(proxy_list)
        file.write(js)

def main():
    need = get_html()
    get_proxy(need)
    # p_map(test_proxy, proxy_list)
    store_ip()
    print('Proxy got already.')

if __name__ == '__main__':
    main()



