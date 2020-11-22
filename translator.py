import requests
from bs4 import BeautifulSoup
import sys

BASE_URL = 'https://context.reverso.net/translation'
langs = ['Arabic', 'German', 'English', 'Spanish',
         'French', 'Hebrew', 'Japanese', 'Dutch',
         'Polish', 'Portuguese', 'Romanian',
         'Russian', 'Turkish']


def top_num(data, num):
    return '\n' + '\n'.join(data[:num]) + '\n'


def translate(src, trg, word):
    direction = f'{langs[src].lower()}-{langs[trg].lower()}'
    url = '/'.join((BASE_URL, direction, word))
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    response = requests.get(url, headers={'User-Agent': user_agent})
    try:
        if response.status_code == 404:
            print(f"Sorry, unable to find {word}")
            exit()
        if response.status_code != 200:
            print("Something wrong with your internet connection")
            exit()
    except ConnectionError:
        exit()

    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find_all('a', class_='translation ltr dict no-pos')
    translations = [el.text.strip() for el in elements]
    elements = soup.find_all('div', class_=['src ltr', 'trg ltr'])
    examples = [el.text.strip() for el in elements]
    examples = [f'{examples[i]}:\n{examples[i+1]}' for i in range(0, len(examples), 2)]
    return f'\n{langs[trg]} Translations:\n{top_num(translations, 5)}' \
           f'\n{langs[trg]} Examples:\n{top_num(examples, 5)}'


def print_report(output):
    print(output)
    with open(f'{word}.txt', 'w', encoding='utf-8') as f:
        f.write(output)


args = sys.argv
src = langs.index(args[1].capitalize())
word = args[3]

if args[2] == 'all' or args[2] == 'All':
    output = ''
    for i in range(13):
        output += translate(src, i, word)
    print_report(output)
else:
    try:
        trg = langs.index(args[2].capitalize())
    except ValueError:
        print(f"Sorry, the program doesn't support {args[2]}")
    else:
        print_report(translate(src, trg, word))