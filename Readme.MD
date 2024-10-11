# Описание #

## API для управления пользователями и реферальными кодами с использованием FastAPI и SQLAlchemy. ##
### Модели ###

    User: Таблица пользователей.
    UserCode: Таблица с реферальными кодами.

### Сериализаторы ###

    UserReadSerializer: Для данных пользователя.
    ReferralCodeCreateSerializer: Для создания реферального кода.
    ReferralCodeGetSerializer: Для получения реферального кода.
    ReferrerCodeGetSerializer: Для получения реферального кода пользователя.
    ReferralsSerializer: Для списка рефералов.

### Эндпоинты ###

    POST /set_ref_code: Устанавливает реферальный код.
    POST /delete_ref_code: Удаляет реферальный код.
    GET /get_ref_code: Получает реферальный код по email.
    GET /get_referrals/{referrer_id}/: Получает список рефералов.


## Запуск и тестирование ##
### docker-compose up --build ###
### http://localhost:8000/docs#/ ###