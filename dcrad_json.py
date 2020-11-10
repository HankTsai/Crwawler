
import os
import json
import requests
from urllib.request import urlretrieve
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
from bs4 import BeautifulSoup as BS

url = "https://www.dcard.tw/service/api/v2/forums/photography/featuredPosts"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
      "AppleWebKit/537.36 (KHTML, like Gecko) " \
      "Chrome/84.0.4147.89 Safari/537.36"'}

os.mkdir('d_photo')
ses = requests.session()
res = ses.get(url=url,headers=headers)
dcard = json.loads(res.text)

for art in dcard:
    art_url = "https://www.dcard.tw/f/photography/p/" +str(art['id'])
    art_title = art['title']
    image_list = art['mediaMeta']
    print(art_title)
    print(art_url)

    try: os.mkdir('d_photo/'+ art_title)
    except:
        art_title = 'unknown'
        try: os.mkdir('d_photo/'+ art_title)
        except: pass

    for img_url in image_list:
        print('\t'+img_url['url'])
        img_name = img_url['url'].split('/')[-1]

        # try:
        #     urlretrieve(img_url['url'],'d_photo/'+ art_title+'/'+img_name)
        # except Exception as e:
        #     print(e)
        with open(f'/d_photo/{art_title}/{img_name}','w') as f:
            url_res = requests.get(img_url['url'],headers=headers)
            f.write(url_res.content)

    print('=========================================')




