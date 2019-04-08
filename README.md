# Отложенные посты для VK, Facebook и Telegram 
Скрипт берет данные из [Google таблицы](https://docs.google.com/spreadsheets/d/17r4QRW_m0clut772bRnUL-U1-JiazImiZMm43SkgS9Q/edit#gid=0)
и делат посты в указанное время. Посты публикуются в VK, Facebook, Telegram.

### Как установить 
* Должен быть установлен `python3`. Затем используйте `pip`(или `pip3`, 
 если есть конфликт с `Python2`) для установки зависимостей: 
 ```bash
 pip install -r requirements.txt
 ```
 * Для изоляции проекта рекомендуется использовать 
 [virtualenv/venv](https://docs.python.org/3/library/venv.html)
 ### Настройка доступа для Google Sheets
 * Авторизоваться в Google
 * Перейти на [страницу](https://developers.google.com/sheets/api/quickstart/python?refresh=1)
 и кликнуть на кнопку "Enable the Google sheets API".
 * Скачать файл "Client configuration" и положить в одну директорию с программой
 * Создайте файл `.env` в одной директории со скриптом
 * Скопировать id Вашей таблицы в `.env`:
 ```text
SHEET_ID='id'
```
 ### Настройка скрипта для VK
 Чтобы получить доступ к API VK, необходимо:
 * Узнать id вашей группы ([узнать его можно здесь](http://regvk.com/id/))
 * Получить access_token:
 * Создайте приложение vk. Создать приложение можно в разделе 
        [**Мои приложения**](https://vk.com/apps?act=manage). В качестве типа
         приложения следует указать **standalone**
 * В настройках приложения скопируйте **client_id** и поместите в ссылку:
        https://oauth.vk.com/authorize?client_id=`CLIENT_ID`&scope=photos,groups,wall,offline&response_type=token
 * Вставьте полученную ссылку в адресную строку браузера и перейдите по
        ней 
 * Вы получите access_token — строку наподобие
         533bacf01e1165b57531ad114461ae8736d6506a3. Она появится в адресной
         строке, подписанная как access_token
 * Запишите в `.env` access_token, id группы, id альбома, логин и пароль:
 ```txt
 ACCESS_TOKEN='your_access_token'
 VK_GROUP_ID=123456789
 VK_ALBUM_ID=123456789
 LOGIN_FOR_VK='ваш логин'
PASSWORD_FOR_VK='ваш пароль'
  ```
### Настройка скипта для Telegram
* Вам необходимо создать канал и бота, если те еще не созданы, получите API ключ
бота. [Как обойти блокировку Telegram](https://bigpicture.ru/?p=913797),
[Как создать канал, бота и получить токе](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)
* Запишите в `.env` ключ и id вашего канала(telegram.org/#/im?p=`@ваш_id`)
```txt
TOKEN_FOR_TELEGRAM='ваш токен'
TELEGRAM_CHAT_ID='@ваш_id'
```
### Настройка скрипта для Facebook
* Получите API ключ, именуемый в Facebook `маркер доступа пользователя`. 
C разрешением `publish_to_groups`. [См. руководство](https://developers.facebook.com/docs/graph-api/explorer/)
* Продлите полученный токен с 2 часов до 2 месяцев. [Ссылка](https://developers.facebook.com/tools/debug/accesstoken/)
* Запишите ключ и id вашей группы в `.env`
```txt
ACCESS_TOKEN_FOR_FB='ваш токен'
FB_GROUP_ID=1234567890
```

### Как запустить
```bash
python3 main.py
```
 
 ### Цель проекта
 Код написать в образовательных целях на онлайн-курсе для веб-разработчиков 
 [dvmn.org](dvmn.org)