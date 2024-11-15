# CATEGORIES

## Отримання списку всіх категорій 

```Url``` - http://localhost:8181/api/v1/glamps/categories/

### Запит GET

#### Приклад відповіді

```
{
    "count": 2,
    "next": null,
    "previous": null,
    "page": 1,
    "pageSize": 10,
    "results": [
        {
            "id": 2,
            "created_at": "2024-10-31T13:49:13.430040+02:00",
            "updated_at": "2024-10-31T13:49:13.430089+02:00",
            "name": "nnnn",
            "slug": "nnnn",
            "title": "nn",
            "description": "nnn",
            "is_active": true,
            "is_hidden": false
        },
        {
            "id": 1,
            "created_at": "2024-10-31T13:44:49.485673+02:00",
            "updated_at": "2024-10-31T13:44:49.485752+02:00",
            "name": "dddd",
            "slug": "dddd",
            "title": "ddd",
            "description": "ddd",
            "is_active": true,
            "is_hidden": false
        }
    ]
}
```

## Отримання конкретної категорії (за id)

```Url``` - http://localhost:8181/api/v1/glamps/categories/{category_id} замість category_id вставляєм id тієї категорії що хочем отримати.

### Запит GET

#### Приклад відповіді на ```Url``` - http://localhost:8181/api/v1/glamps/categories/3

```
{
    "id": 3,
    "created_at": "2024-10-31T13:54:07.542563+02:00",
    "updated_at": "2024-10-31T13:54:07.542605+02:00",
    "name": "Bobre",
    "slug": "bobr-kurwa",
    "title": "dd",
    "description": "dd",
    "is_active": true,
    "is_hidden": false
}
```

## Створення категорії 

```Url``` - http://localhost:8181/api/v1/glamps/categories/

### Запит POST

Для створення категорії потрібно вказати наступні поля: 

```
{
    "name": "testname",
    "slug": "testslug",
    "title": "testtitle",
    "description": "testdescription"
}
```

***Пояснення за Slug - це поле за яким відбувається пошук конкретної категорії (дивитись вище). Слаг має бути унікальним і відповідати певним вимогам. Він може бути тільки з латинських символів, цифр, дефісів та нижніх підкреслювань.***

*Ще момент, якщо створювати категорію через адмінку то слаг буде автоматично формуватися в реальному часі, але його можна буде змінити (це просто зручність). Проте якщо створювати через Postman як я показав раніше поле slug потрібно прописувати ручками.*

#### Приклад відповіді

```
{
    "id": 5,
    "created_at": "2024-10-31T14:11:56.531689+02:00",
    "updated_at": "2024-10-31T14:11:56.531721+02:00",
    "name": "testname",
    "slug": "testslug",
    "title": "testtitle",
    "description": "testdescription",
    "is_active": false,
    "is_hidden": false
}
```