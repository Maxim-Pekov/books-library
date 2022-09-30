from pprint import pprint

import requests


def main():
    url = "https://tululu.org/txt.php"
    params = {'id': 32168}
    response = requests.get(url, params=params)
    response.raise_for_status()
    filename = 'dvmn.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)


if __name__ == '__main__':
    main()


