import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd


# query string parameters:
# %3 is ?
# %20 is space
# %22 is quotes
# %5B is '['
# %5D is ']'


# * nama produk
# * harga produk
# * nama toko
# * link produk
# * lokasi toko


def get_all_items(page, search_keyword):
    url = 'https://www.bukalapak.com/products?'
    params = {
        'page': page,
        'search[keywords]': search_keyword
    }
    res = requests.get(url, params=params)

    newlist = []
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all('div', 'bl-flex-item mb-8')

    for i in items:
        try:
            title = i.find('p', 'bl-text bl-text--body-14 bl-text--ellipsis__2').text.strip()
            price = i.find('p', 'bl-text bl-text--subheading-20 bl-text--semi-bold bl-text--ellipsis__1').text.strip()
            store_name = i.find('span',
                                'bl-product-card__store bl-text bl-text-'
                                '-body-14 bl-text--subdued bl-text--ellipsis__1').text
            links = i.find('a', 'bl-link')['href']
            location = i.find('span', 'mr-4 bl-product-card__location bl-text bl-text--body-14 bl-text--subdued '
                                      'bl-text--ellipsis__1').text

        except AttributeError:
            pass
        # Sorting data
        data_dict = {
            'product': title,
            'price': price,
            'store': store_name,
            'link': links,
            'location': location
        }
        newlist.append(data_dict)

    # Delete data berlebih di list
    del newlist[50:len(newlist)]

    # Writing json file
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    with open(f'json_result/search_{search_keyword}_page_{page}.json', 'w+') as json_data:
        json.dump(newlist, json_data)
    print('json created')

    # Writing csv and Excel file
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass

    # Create CSV
    df = pd.DataFrame(newlist)
    df.to_csv(f'data_result/{search_keyword}_page_{page}.csv', index=False)
    df.to_excel(f'data_result/{search_keyword}_page_{page}.xlsx', index=False)

    # html file
    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/result.html', 'w', encoding="utf-8") as f:
        f.write(res.text)
        f.close()

    return newlist


def run():
    search = input('Search: ')
    page = input('Page(1-99): ')

    total = get_all_items(page, search)
    print(total)


if __name__ == '__main__':
    run()
