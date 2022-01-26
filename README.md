# support_application


## Настройка:
- Запуск
```
- docker-compose up -d

```
- Остановка
```
- docker-compose stop
```
- Создание администратора
```
- docker-compose exec backend python manage.py createsuperuser
```
### Основные эндпоинты
- Регистрация пользователя: POST запрос с username и password 
```
- localhost/auth/users/ 
```
- Получение токена: POST запрос с username и password зарегистрированного пользователя
```
- localhost/auth/jwt/create/
```
- Создание тикетов: POST запрос с title и text. Список своих тикетов по GET запросу
```
localhost/tickets/
```
### flower
```
- localhost:5555/
```