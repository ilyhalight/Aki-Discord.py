## ШАГ 1
### Установка Python
- Заходим на сайт https://www.python.org/
- Нажимаем кнопку "Download"
- Выбираем последнюю версию
- Скачиваете установщик для вашей ОС
- Открываете установщик
- Не забываем поставить галочку ADD TO PATH
- Устанавливаем
- Готово

## ШАГ 2
### Установка библиотек для Python
- Открываем консоль
- Вписываем в консоль эти команды:
  - pip install discord.py
  - pip install datetime
  - pip install youtube_dl
  - pip install wikipedia
  - pip install requests
  - pip install asyncio
- Готово

## ШАГ 3
### Загрузка и настройка БОТА
- Заходим в мой репозиторий https://github.com/ilyhalight/Aki-Discord.py
- Нажимаем кнопку "Code"
  - Нажимаем "Download ZIP"
- Распаковываем в удобное место
- С помощью текстового редактора открываем config.py
- Находим строку: 'NAME BOT': 'Your Name'
  - Заместо "Your Name" пишем имя вашего бота
  - Пример:  'NAME BOT': 'Toil'
- Находим строку: 'TOKEN': 'Your Token'
  - Заместо "Your Token" пишем имя вашего бота [ШАГ 5]
- Находим строку: 'ID': 'Your ID'
  - Заместо "Your ID" пишем ID нашего бота [ШАГ 5]
  
## ШАГ 4
### Установка ffmpeg
- Заходим на сайт https://ffmpeg.org/
- Нажимаем "Download"
- Наводим на вашу ОС и снизу видим ссылку
- Нажимаем на ссылку
  - Нас перекидывает на другой сайт
- Нажимаем кнопку Download build
- Открываем скачанный архив
- Папку из архива скидываем на диск С
- После переименовываем папку в "ffmpeg"
- Заходим в папку ffmpeg
- Копируем путь до папки ffmpeg\bin
  - В моём случае это C:\ffmpeg\bin
- Теперь заходим в сведенья о системе
- Нажимаем дополнительные параметры системы
- Нажимаем переменные среды...
- Видим переменные среды для пользователя [Ваше имя пользователя]
- Выбираем PATH
  - Нажимаем изменить
- В открывшемся окне нажимаем "Создать"
  - Вставляем путь к папке ffmpeg\bin
- Нажимаем ОК
- Нажимаем ОК
- Нажимаем ОК
- Готово

## ШАГ 5
### Создание учетной записи бота
- Заходим на сайт https://discord.com/developers/applications
- Нажимаем на кнопку "New application"
- Вводим имя нашего бота
- Нажимаем создать
- Теперь заходим в "Bot"
- Нажимаем кнопку "Add bot"
- Подтверждаем, что хотим создать бота
  - Готово бот создан
#### Приглашаем бота на сервер
- Заходим в OAuth2
- Видим таблицу "SCOPES"
- В таблице выбираем "bot"
- В появившейся таблице выбираем "Administator"
- Копируем ссылку из "SCOPES" и вставляем в поисковую строку
- Выбираем сервер на который хотим добавить нашего бота
  - Нажимаем продолжить
  - Нажимаем авторизовать
  - Проходим капчу
- Готово бот на сервере
#### Получение TOKEN и CLIENT ID
- Возвращаемся на сайт https://discord.com/developers/applications
- Выбираем нашего бота
- В "General Information" находим CLIENT ID
  - Нажимаем "Copy"
  - CLIENT ID скопирован можете вставлять его в config.py [ШАГ 3]
- В "Bot" находим TOKEN
  - Нажимаем "Copy"
  - TOKEN скопирован можете вставлять его в config.py [ШАГ 3]
- Готово

## ШАГ 6
### Первый запуск бота
- Открываем папку с ботом
- Находим server.bat
- Открываем server.bat
- Ждём надписи: "Logged on as Your Name"
- Готово. Бот запущен
- Проверяем написав команду $help
- Если команда отобразится, то у вас всё получилось

## ШАГ 7
### Помощь в пастинге
- Заходим в config.py
- Меняем "OWNER", "CREATOR NAME"
  - Пример: 'OWNER':'ilyhalight#1605'
  - Пример: 'CREATOR NAME':'ilyhalight'
- Готово, теперь во вех командах будет ваш ник и ваш Nick#id
- Для добавления команд рекомендую ознакомится с документацией:
  - https://discordpy.readthedocs.io/en/latest/api.html







