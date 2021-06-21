import json
import re

def check_target_brand_file():
    with open('target_brand_file.json', 'r') as file:
        target_brand_file = json.loads(file.read())
        for key, value in target_brand_file.items():
            print(len(value))

#def check_product_link_file():
#    with open('product_link_file.json', 'r') as file:
#        product_link_file = json.loads(file.read())
#        for key, value in product_link_file.items():
#            print(f'##########{key}###########')
#            print(f'number of {key} is {len(value)}.')
#            for item in value[:5]:
#                brand = re.search(r'kw=.+', item[0]).group(0)
#                print(brand[3:])

def check_product_link_file():
    with open('product_link_file_test.json', 'r') as file:
        product_link_file = json.loads(file.read())
        print(product_link_file)
        # for category, brand_links in product_link_file.items():
            # print(brand_links)
            # for brand, links in brand_links.items():
            #     print(brand, len(links), links[0])


def check_single_product_link():
    with open('product_daily_necessities.json', 'r') as file:
        product_link_file = json.loads(file.read())
        for brand, links in product_link_file.items():
            for link in links:
                print(link)
            break

check_single_product_link()

