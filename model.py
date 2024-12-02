import bs4, requests
import random

def get_dish(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        links = soup.find_all('li', class_='browse-recipe-item')
        links_list = [link.find('a')['href'] for link in links]

        if len(links_list) > 0:
            link = random.choice(links_list)
            return f'https://icook.tw{link}'
        else:
            print('No recipes found!')
    else:
        print(response)

def get_surprise():
    random_num = random.randint(2, 500)
    url = f"https://icook.tw/categories/{random_num}"
    return get_dish(url)
