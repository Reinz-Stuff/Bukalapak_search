import requests
from bs4 import BeautifulSoup

url = 'https://www.bukalapak.com/products?from=omnisearch&from_keyword_history=false&search%5Bkeywords%5D=ssd' \
      '&search_source=omnisearch_keyword&source=navbar '
res = requests.get(url)


# * nama produk
# * harga produk
# * nama toko
# * link produk
# * lokasi toko

def get_total_page():
    total_pages = []

    soup = BeautifulSoup(res.text, 'html.parser')
    listing = soup.find('ul', 'bl-pagination__list')
    page = listing.find_all('li')
    for i in page:
        total_pages.append(i.text.strip())
    total_pages.remove('…')
    total = int(max(total_pages))
    return total


def get_all_items():
    j = 1
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all('div', 'bl-flex-item mb-8')
    # print(items)
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
            print(j, f'Product Name: {title}\nPrice: {price}\nStore: {store_name}\nLink: {links}\nLocation: {location}\n'

            )
            j += 1
        except AttributeError:
            pass



if __name__ == '__main__':
    get_all_items()
