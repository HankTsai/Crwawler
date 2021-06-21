def getNewRequests(requestURL,Host):
    import requests
    import Public.PublicFun as PublicFun
    request = requests.Session()

    JobID=PublicFun.createID()
    Chromedriver=PublicFun.getWebDriver("chrome",DataFolderName=JobID)
    Chromedriver.get(requestURL)
    cookies = Chromedriver.get_cookies()
    userAgent=Chromedriver.execute_script("return navigator.userAgent")
    PublicFun.closeWebDriver(JobID,Chromedriver)
    
    header={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': Host,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': userAgent
    }
    request.headers.update(header)

    for cookie in cookies:
        request.cookies.set(cookie['name'], cookie['value'])

    return request

def getRequestFromWebDriver(webdriver):
    #建立Request回傳
    import requests
    request = requests.Session()
    cookies = webdriver.get_cookies()
    userAgent=webdriver.execute_script("return navigator.userAgent")
    header={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'DNT': '1',
    #'Host': 'www.104.com.tw',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': userAgent
    }
    request.headers.update(header)

    for cookie in cookies:
        request.cookies.set(cookie['name'], cookie['value'])

    return request

#單純取得request 不使用chromeDriver
def getNewRequestWithoutDriver(host):
    import requests
    request = requests.Session()    
    header={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': host,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    request.headers.update(header)

    #for cookie in cookies:
    #    request.cookies.set(cookie['name'], cookie['value'])

    return request

#取得返回為JSON格式的web API request
def getNewRequestWithoutDriverForJson(host, refererURL) :
    request = getNewRequestWithoutDriver(host)
    headers = request.headers
    headers["Referer"] = refererURL
    headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
    headers["X-Requested-With"] = "XMLHttpRequest"
    request.headers.update(headers)
    return request