
import re
from crawler_conf import RequestsConf, SaveAndRead
request_conf = RequestsConf()
save_read = SaveAndRead()


def definite_product_info(link):
    product_info = {}; info_list = []
    try:
        page = request_conf.get_html(link)
        name = page.xpath('//h3[@id="goodsName"]/text()')
        brand_name = re.search(r'【.*】', name[0]).group(0)
        product_info['brand_name'] = brand_name[1:-1]
        product_name = re.search(r'】.*', name[0]).group(0)
        product_info['product_name'] = product_name[1:]
        product_price = page.xpath('//td[@class="priceArea"]/b/text()')
        if not product_price: product_price = '0'
        product_info['product_price'] = product_price[0]
        info_list = page.xpath('//div[@class="Area101"]/text()')
    except IndexError: pass
    except AttributeError: pass
    return product_info, info_list

def definite_detail_info(link):
    product_info, info_list = definite_product_info(link)
    company_info = {}; other_info = []
    if info_list:
        for item in info_list:
            try:
                content = item.replace('\n', '').strip()
                key = re.search(r'(.*：)|(.*:)|(.*")|(.*】)|(.*/)', content).group(0)[:-1]
                value = re.search(r'(：.*)|(:.*)|(".*)|(】.*)|(/.*)', content).group(0)[1:]

                if re.search(r'(.*廠.*)|(.*業者.*)', key):
                    if not re.search(r'(.*內文.*)', value):
                        if not re.search(r'(.*字號.*)', key):
                            if re.search(r'(.*名稱.*)|(.*業者.*)|(.*字號.*)', key):
                                company_info['factory_name'] = value
                        elif re.search(r'(.*電話.*)', key):
                            company_info['factory_phone'] = value
                        elif re.search(r'(.*地址.*)', key):
                            company_info['factory_address'] = value
                else:
                    if re.search(r'(.*產地.*)', key):
                        product_info['product_place'] = value
                    elif re.search(r'(.*規格.*)', key):
                        product_info['product_format'] = value
                    else: other_info.append(value)
            except AttributeError:pass
        product_info['other_info'] = "".join(other_info)

    return company_info, product_info





