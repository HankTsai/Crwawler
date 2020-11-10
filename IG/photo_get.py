
import os
import re
import sys
import json
import time
import random
import requests
from lxml import etree
from hashlib import md5
from p_tqdm import p_imap
from functools import partial
from fake_useragent import UserAgent


# request setting.
base_url = 'https://www.instagram.com'
query_url = 'https://www.instagram.com/graphql/query/?' \
            'query_hash=a5164aed103f24b03e7b7747a2d94e3c&' \
            'variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'
headers = {
    'User-Agent':UserAgent().random,
    'accept': "text/html,application/xhtml+xml,application/xml;"\
              "q=0.9,image/avif,image/webp,image/apng,*/*;"\
              "q=0.8,application/signed-exchange;v=b3;q=0.9",
    'cookie':"ig_did=303D7F64-0944-424F-AE39-85479C600EF7; "\
             "mid=XxMEaQAEAAHp2Ub9eMwFdgfwY-pn; fbm_124024574287414=base_domain=.instagram.com; "\
             "csrftoken=2LhUpFNPAu9fSIlR1txHPgZaF9Whpr5e; "\
             "ds_user_id=4267188850; sessionid=4267188850%3Ak7cuLSxMXCIfZw%3A17; "\
             "shbid=16067; rur=RVA; shbts=1599916468.3608112; "\
             "urlgen=\"{\"2001:b400:e358:963f:d118:3b0b:9f80:112b\": 17421}:1kHVxR:1SHmW9Mz6vtF2d4SJawci40NiQ4\""}
os.chdir('/Users/BlackSung/Code/Python/Project/crawler')
# if want to use fake proxy.
# proxies = json.loads(open('./proxies.json','r',encoding='utf8').read())

# to store img link.
photo_urls = []
video_urls = []

# to store social network data.
# follower_num =[]      # how many people follow target_user.
# follow_num = []       # how many people target_user follow.
# img_text = []         # the text of image set by target_user.
# img_tag = []          # the tage of image set by target_user.
# photo_feature = []    # the feature in each photo set by ig.
# video_view_num = []   # the sum views of each video counted by ig. 
# img_push = []         # the sum push_num of all event counted by ig.
# comment_num = []      # the sum comment of each event counted by ig
# like_num = []         # the sum like of each event counted by ig.


def get_html(url):
    try:
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            page = etree.HTML(res.text)
            element = page.xpath('//body//script[@type="text/javascript"][1]//text()')
            html = json.loads(''.join(element[0][21:-1]))
            html = html["entry_data"]["ProfilePage"][0]["graphql"]["user"]
            return html
        else: print(f'Status_Code：{res.status_code}')
    except Exception as e: print(e)


def get_json(url):
    try:
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            html = json.loads(res.text)
            js = html['data']['user']
            return js
        else: print(f'Status_Code：{res.status_code}')
    except Exception as e: print(e)


def download_img(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)      #proxies=proxies[proxy_id]
        if res.status_code == 200: return res.content
        else:
            print(f'Status_Code：{res.status_code}')
            return None
    except Exception as e: print(e)


def get_img_info(figure):
    # 將影像網址儲存成串列
    for item in figure:    

        if item['node'].get('edge_sidecar_to_children'):
            for sub_item in item['node']['edge_sidecar_to_children']['edges']:
                if sub_item['node'].get('is_video'): pass
                    # video_urls.append(sub_item['node']['video_url'])
                    # video_view_num = sub_item['node']['video_view_count']
                else: photo_urls.append(sub_item['node']['display_url'])
                    # photo_feature = subitem['node']['accessibility_caption']
        else:
            if item['node'].get('is_video'): pass
                # video_urls.append(item['node']['video_url'])
                # video_view_num = item['node']['video_view_count']
            else: photo_urls.append(item['node']['display_url'])
                # photot_feature = item['node']['accessibility_caption']

        # 影像周邊資訊
        # comment_num.append(item['node']['edge_media_to_comment']['count'])
        # like_num.append(item['node']['edge_media_preview_like']['count'])
        #
        # if item['edge_media_to_caption'].get(['edges']):
        #     img_text.append(item['edge_media_to_caption']['edges']['node']['text'])
        # else: img_text.append('')
        # if item['edge_media_to_tagged_user'].get(['edges']):
        #     img_tag.append(item['edge_media_to_tagged_user']['edges'][0]['node']['user']['username'])
        # else: img_tag.append('')


def get_user_info(data):
    # 頁面資訊收集
    # img_push = user_info["edge_owner_to_timeline_media"]['count']
    # follower_num = user_info['edge_followed_by']['count']
    # follow_num = user_info['edge_follow']['count']

    # 用來爬取全部影像使用的標籤
    # while next_page:
    # next_page = page_info['has_next_page']

    user_id = data['id']
    for _ in range(total_num):
        # 影像資訊收集
        page_info = data["edge_owner_to_timeline_media"]['page_info']
        figure = data["edge_owner_to_timeline_media"]['edges']
        get_img_info(figure)

        # 換頁資訊收集
        cursor = page_info['end_cursor']
        url = query_url.format(user_id=user_id, cursor=cursor)
        data = get_json(url)


def store_img(img_list,f_format,path):
    if not os.path.exists(path): os.mkdir(path)
    # 下載並儲存所有影像檔
    try:
        img = p_imap(download_img,img_list)
        for index,item in enumerate(img):
            content = f'{path}/{index}.{f_format}'
            if not os.path.exists(content):
                with open(content, 'wb') as file:
                    file.write(item)
    except Exception as e:
        print(f'影像下載失敗，原因：{e}')


def main():
    # 爬取數據
    url = f'{base_url}/{user_name}/'
    html = get_html(url)
    get_user_info(html)
    photo_num = len(photo_urls)
    video_num = len(video_urls)
    try:
        if photo_num == len(set(photo_urls)): print(photo_num)
        if video_num == len(set(video_urls)): print(video_num)
        print('影像擷取數量正確，3秒後開始下載。')
        time.sleep(3)
    except Exception as e: print(e)
    
    # 儲存數據
    path = f'{store_path}/{user_name}'
    if not os.path.exists(path): os.mkdir(path)
    print(f'\n正在下载photo...')
    if photo_urls: store_img(photo_urls,'jpg',f'{path}/photo')
    # print(f'\n正在下载video...')
    # if video_urls: store_img(video_urls,'mp4',f'{path}/video')
    print('\n影像下載完成')


if __name__ == '__main__':
    user_name = 'jennyyen249'                       # sys.argv[1]
    store_path = '/Users/BlackSung/Pictures/IG'     # sys.argv[2]
    total_num = int('5')                            # sys.argv[3]
    
    start = time.time()
    main()
    end = time.time()
    spend = end - start
    hour = spend // 360
    min = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * min
    print(f'共花费了{hour}小时{min}分钟{sec}秒')