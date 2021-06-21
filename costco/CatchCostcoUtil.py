import time
import requests
from bs4 import BeautifulSoup, NavigableString, Comment
from Public import VerifyCode
from Public import PublicFun
import json
        
def get_session() :
    """取得session
    return:
        session
    """
    session = requests.Session()
    return session

def get_header_with_hostname(hostname) :
    """取得包含hostname的request header
    return:
        reques header
    """
    return {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            , "Accept-Encoding": "gzip, deflate"
            , "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8,en-US;q=0.7"
            , "Connection": "keep-alive"
            , "Upgrade-Insecure-Requests" : "1"
            , "Cache-Control" : "max-age=0"
            , "Host": hostname
            , "Upgrade-Insecure-Requests": "1"
            , "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36" }
            
def send_get_request(logger, session, url, header, timeout = 180) :
    """送出get method的request
    args:
        logger: logger
        session: session
        url: url
        header: request header
        timeout: timeout
    return
        response
    """
    retry_limit = 10
    retry_times = 0
    resp = None
    while True :
        try:
            resp = session.get(url, headers = header, timeout = timeout)
            if url not in resp.url : 
                url = resp.url
                raise Exception("重新導向URL : " + resp.url)
            break
        except Exception as e :
            if logger:
                logger.error(e)
            retry_times += 1
            time.sleep(2)
            if retry_times > retry_limit:
                raise Exception("URL:" + url + " ,超過最大重試次數")
            
    return resp