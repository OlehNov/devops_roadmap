# MANAGERS


### Доступні методи


- ![текст](https://img.shields.io/badge/GET-%2390EE90)
- ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)
- ![текст](https://img.shields.io/badge/POST-%23FFFF00)
- ![текст](https://img.shields.io/badge/PUT-%230000FF)
- ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)
- ![текст](https://img.shields.io/badge/DELETE-%23FF0000)

---
## ![GET](https://img.shields.io/badge/GET-%2390EE90)

#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/](http://localhost:8181/api/v1/managers/)

### Вимоги до запиту:
 - Токен Bearer token
 - Користувач із роллю АДМІНІСТРАТОРА
 - Користувач із роллю МЕНЕДЖЕР
 - Адміністратор


#### Відповідь

```
{
    "count": 1,
    "next": null,
    "previous": null,
    "page": 1,
    "pageSize": 10,
    "results": [
        {
            "user": {
                "id": 12,
                "email": "a@gmail.com",
                "is_active": true,
                "is_staff": false,
                "created_at": "2024-11-12T13:02:51.156186+02:00",
                "updated_at": "2024-11-12T13:02:51.185555+02:00"
            },
            "first_name": "aaa",
            "last_name": "bbb",
            "status": 1,
            "role": 2
        }
    ]
}
```
---
## ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)

#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/12/](http://localhost:8181/api/v1/managers/12/)


### Вимоги до запиту:
 - Токен Bearer token
 - Користувач із роллю АДМІНІСТРАТОРА
 - Користувач із роллю МЕНЕДЖЕР та тим самим ідентифікатором об’єкта
 - Адміністратор

#### Відповідь
```
{
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-11-12T15:10:12.433051+02:00",
        "updated_at": "2024-11-12T15:10:12.442579+02:00"
    },
    "first_name": "aaa",
    "last_name": "bbb",
    "status": 1,
    "role": 2
}
```
---
![текст](https://img.shields.io/badge/POST-%23FFFF00)

#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/](http://localhost:8181/api/v1/managers/)

### Вимоги до запиту:
 - Токен Bearer token
 - Користувач із роллю АДМІНІСТРАТОРА
 - Адміністратор

#### Тіло запиту

```
{
  "user": {
    "email": "a@gmail.com",
    "password": "ri43ydQXb",
    "confirm_password": "ri43ydQXb"
  },
  "first_name": "aaa",
  "last_name": "bbb"
}
```

#### Відповідь
```
{
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "is_active": true,
        "is_staff": false,
        "role": 2
    },
    "status": 1,
    "first_name": "aaa",
    "last_name": "bbb"
}
```
---
## ![текст](https://img.shields.io/badge/PUT-%230000FF)

#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/12/](http://localhost:8181/api/v1/managers/)

### Вимоги до запиту:
 - Токен Bearer token
 - Користувач із роллю АДМІНІСТРАТОРА
 - Адміністратор

### Тіло запиту
```
{
    "role": 2,
    "first_name": "aaa",
    "last_name": "sss"
}
```

### Відповідь
```
{
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-11-12T15:10:12.433051+02:00",
        "updated_at": "2024-11-12T15:10:12.442579+02:00"
    },
    "first_name": "aaa",
    "last_name": "sss",
    "status": 1,
    "role": 2
}
```

## ❗Попередження❗
*Якщо роль було змінено, користувача буде автоматично деактивовано та створено нову роль профілю*
---
## ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)
#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/12/](http://localhost:8181/api/v1/managers/)

### Вимоги до запиту:
 - Токен Bearer token
 - Користувач із роллю АДМІНІСТРАТОРА
 - Користувач із роллю МЕНЕДЖЕР та тим самим ідентифікатором об’єкта
 - Адміністратор

## Тіло запиту
```
{
    "first_name": "qwer",
    "last_name": "rewq"
}
```

## Відповідь
```
{
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-11-12T15:10:12.433051+02:00",
        "updated_at": "2024-11-12T15:10:12.442579+02:00"
    },
    "first_name": "qwer",
    "last_name": "rewq",
    "status": 1,
    "role": 2
}
```
---
## ![текст](https://img.shields.io/badge/DELETE-%23FF0000)
#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/12/](http://localhost:8181/api/v1/managers/)

### Вимоги до запиту:
 - Токен Bearer token
 - Користувач із роллю АДМІНІСТРАТОРА
 - Користувач із роллю МЕНЕДЖЕР та тим самим ідентифікатором об’єкта
 - Адміністратор

## Тіло запиту
```
None
```

## Відповідь
```
{
    "detail": "Object deactivated successfully."
}
```
