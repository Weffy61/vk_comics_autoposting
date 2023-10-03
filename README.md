# Vk auto posting comics script

Скрипт постит в [vk](https://vk.com) рандомные комиксы  с [xkcd.com](https://xkcd.com/) c коментариями авторов.

## Установка

```commandline
git clone https://github.com/Weffy61/vk_comics_autoposting.git
```

## Установка зависимостей
Переход в директорию с исполняемым файлом

```commandline
cd vk_comics_autoposting
```

Установка
```commandline
pip install -r requirements.txt
```

## Подготовка к запуску

[Создайте сообщество](https://vk.com/groups_create) в vk. Вы должны увидеть данное сообщество во вкладке `Управление`.
Создайте Standalone-приложение в вк и запустите его. Получите `ACCESS_TOKEN` методом 
[Implicit flow](https://dev.vk.com/ru/api/access-token/implicit-flow-user). При получении токена укажите следующие 
необходимые разрешения: groups,photos,wall,offline. Также не забудьте указать ваш `vk_app_id` в аргументе 
`client_id`, который указан в адресной строке вашего браузера, когда вы находитесь в настройках приложения.

## Создание и настройка .env

Создайте в корне папки `vk_comics_autoposting` файл `.env`. Откройте его для редактирования любым текстовым редактором
и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступны следующие переменные:
 - VK_ACCESS_TOKEN - полученный шагом ранее токен
 - VK_GROUP_ID - `group_id` вашего сообщества в [vk](https://vk.com). Узнать `group_id` для вашей группы можно 
[здесь](https://regvk.com/id/)
 

## Запуск

```commandline
python main.py
```

После запуска в течении нескольких секунд будет создан новый пост в вашей группе с комиксом и забавным коментарием.  

## Цели проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.