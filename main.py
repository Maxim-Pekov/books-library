import requests


def print_hi(name):


    url = "https://dvmn.org/filer/canonical/1542890876/16/"

    response = requests.get(url)
    response.raise_for_status()

    filename = 'dvmn.svg'
    with open(filename, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    print_hi('PyCharm')


