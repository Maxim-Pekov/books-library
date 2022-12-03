# download_books.py

Это проект для скачивания книг и информации по книгам с сайта [https://tululu.org/](https://tululu.org/). 
Проект содержит два скрипта:
* `download_books.py` - Для скачивания набора произвольных книг с указанием порядкового первого номера и последнего.
* `parse_tululu_category.py` - Для скачивания книг постранично в категории фантастика с указанием первой и последней страницы для скачивания.
* `render_website.py` - Для создания html страниц по шаблону

## Пример одной из страниц сайта
![](./media/books.png)

Ссылка на рабочую страницу сайта [books-library](https://maxim-pekov.github.io/books-library). 
## Как он работает:

1. `download_books.py`
   Вы запускаете скрипт командой ниже, параметры <first_id> <last_id> - это id книги с какой по какую вы хотите скачать.
   Если параметры оставить пустыми то скрипт по умолчанию скачает с 1 по 10-ю книгу.

```python
python3 download_books.py <first_id> <last_id>
```
2. `parse_tululu_category.py` Вы запускаете скрипт командой ниже, с указанием необязательных аргументов.
   
```python
python3 parse_tululu_category.py -s <start_page> -l <last_page> -f <dest_folder> -i <save_img>
                                 -t <save_txt> -j <json_path>
```
* --<start_page> - Этот аргумент указывает на первую страницу для скачивания книг, по умолчанию 1
* --<last_page> - Этот аргумент указывает на последнюю страницу которая уже не будет скачена, по умолчанию последняя странница в выбранной категории
* --<dest_folder> - Этот аргумент указывает куда будут скачены книги, по умолчанию это папка 'static'.
* --<save_img> - Этот аргумент принимает yes/no, если указать no, то обложки не будут скачиваться.
* --<save_txt> - Этот аргумент принимает yes/no, если указать no, то книги не будут скачиваться.
* --<json_path> - Этот аргумент принимает название пути к папке куда скачать json файл, если не указать, по умолчанию указывается папка 'static'.

3. `python3 render_website.py` Вы создаете страницы сайта на своем локальном компьютере.
## Установка

Используйте данную инструкцию по установке этого скрипта

1. Установить

```python
git clone https://github.com/Maxim-Pekov/books-library.git
```

2. Создайте виртуальное окружение:

```python
python -m venv venv
```

3. Активируйте виртуальное окружение:
```python
.\venv\Scripts\activate`    # for Windows
```
```python
source ./.venv/bin/activate    # for Linux
```

4. Перейдите в `books-library` директорию.

3. Установите зависимости командой ниже:
```python
pip install -r requirements.txt
```

---

## About me

[<img align="left" alt="maxim-pekov | LinkedIn" width="30px" src="https://img.icons8.com/color/48/000000/linkedin-circled--v3.png" />https://www.linkedin.com/in/maxim-pekov/](https://www.linkedin.com/in/maxim-pekov/)
</br>

[<img align="left" alt="maxim-pekov" width="28px" src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Telegram_Messenger.png" />https://t.me/MaxPekov/](https://t.me/MaxPekov/)
</br>

[//]: # (Карточка профиля: )
![](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=Maxim-Pekov&theme=solarized_dark)

[//]: # (Статистика языков в коммитах:)

[//]: # (Статистика языков в репозиториях:)
![](https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=Maxim-Pekov&theme=solarized_dark)
![](https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=Maxim-Pekov&theme=solarized_dark)


[//]: # (Статистика профиля:)

[//]: # (Данные по коммитам за сутки:)
![](https://github-profile-summary-cards.vercel.app/api/cards/stats?username=Maxim-Pekov&theme=solarized_dark)
![](https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=Maxim-Pekov&theme=solarized_dark)

[//]: # ([![trophy]&#40;https://github-profile-trophy.vercel.app/?username=Maxim-Pekov&#41;]&#40;https://github.com/ryo-ma/github-profile-trophy&#41;)

