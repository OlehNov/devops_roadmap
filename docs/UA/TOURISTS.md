# tourists


### Available methods


- ![текст](https://img.shields.io/badge/GET-%2390EE90)
- ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)
- ![текст](https://img.shields.io/badge/POST-%23FFFF00)
- ![текст](https://img.shields.io/badge/PUT-%230000FF)
- ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)
- ![текст](https://img.shields.io/badge/DELETE-%23FF0000)

---
## ![GET](https://img.shields.io/badge/GET-%2390EE90)

#### ➡️ **URL**: [http://localhost:8181/api/v1/tourists/](http://localhost:8181/api/v1/tourists/)

### Вимоги до запиту:
    - Токен Bearer token
    - Користувач з роллю АДМІНІСТРАТОРА або:
        - Користувач із роллю МЕНЕДЖЕР
        - Користувач Стафф


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
            "id": 13,
            "user": {
                "id": 13,
                "email": "1234@gmail.com",
                "role": 3,
                "is_active": true,
                "is_staff": false,
                "created_at": "2024-12-06T16:10:19.503252+02:00",
                "updated_at": "2024-12-06T16:10:53.816969+02:00"
            },
            "created_at": "2024-12-06T16:10:19.507341+02:00",
            "updated_at": "2024-12-06T16:10:19.513771+02:00",
            "first_name": "aaa",
            "last_name": "bbb",
            "status": 1,
            "birthday": "2002-02-02",
            "phone": "+1234567891"
        }
    ]
}
```
---
## ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)

#### ➡️ **URL**: [http://localhost:8181/api/v1/tourists/13/](http://localhost:8181/api/v1/tourists/12/)


### Вимоги до запиту:
    - Токен Bearer token
    - Користувач з роллю АДМІНІСТРАТОРА або:
        - Користувач із роллю МЕНЕДЖЕР
        - Користувач із роллю TOURIST і таким самим ідентифікатором об’єкта
        - Користувач Стафф

### Відповідь
```
{
    "id": 13,
    "user": {
        "id": 13,
        "email": "moon0939110824@gmail.com",
        "role": 3,
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-12-06T16:10:19.503252+02:00",
        "updated_at": "2024-12-06T16:10:53.816969+02:00"
    },
    "created_at": "2024-12-06T16:10:19.507341+02:00",
    "updated_at": "2024-12-06T16:10:19.513771+02:00",
    "first_name": "aaa",
    "last_name": "bbb",
    "status": 1,
    "birthday": "2002-02-02",
    "phone": "+1234567891"
}
```
---
![текст](https://img.shields.io/badge/POST-%23FFFF00)

#### ➡️ **URL**: [http://localhost:8181/api/v1/tourists/](http://localhost:8181/api/v1/tourists/)

### Вимоги до запиту:
 - Будь-який

### Тіло запиту

```
{
  "user": {
    "email": "123@gmail.com",
    "password": "password",
    "confirm_password": "password"
  },
  "first_name": "aaa",
  "last_name": "bbb",
  "phone": "+1234567891",
  "birthday": "2002-02-02"
}
```

### Відповідь
```
{
    "id": 13,
    "user": {
        "id": 13,
        "email": "123@gmail.com",
        "role": 3,
        "is_active": false,
        "is_staff": false,
        "created_at": "2024-12-06T16:10:19.503252+02:00",
        "updated_at": "2024-12-06T16:10:19.511025+02:00"
    },
    "created_at": "2024-12-06T16:10:19.507341+02:00",
    "updated_at": "2024-12-06T16:10:19.513771+02:00",
    "first_name": "aaa",
    "last_name": "bbb",
    "status": 1,
    "birthday": "2002-02-02",
    "phone": "+1234567891"
}
```
<div style="border: 2px solid red; padding: 10px;">
<h2>❗  WARNING ❗ <h2>
    <p>After successful registrations tourist will receive confirmation email</p>
    <p>For activate account, user must follow the link in a message</p>
</div>

---
![текст](https://img.shields.io/badge/POST-%23FFFF00)

#### ➡️ **URL**: [http://localhost:8181/api/v1/tourists/activate-tourist/{token}/](http://localhost:8181/api/v1/tourists/activate-tourist/{token}/)
### Вимоги до запиту::
 - Будь-який

### URL параметр
```
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNjk1MDczMSwiaWF0IjoxNzM2ODY0MzMxLCJqdGkiOiI0NmQ0ZjZkMmQwN2Q0MjhkYmRkMzMwMGRmODRkNWI3NiIsInVzZXJfaWQiOjI0fQ.h83BOnikYEhARAZUMQRUNt4k1tfQ19DiWl_FfBr3Fxk",
}
```

### Відповідь
```
{
    "detail": "Tourist has been activated.",
    "email": "example@gmail.com",
    "user_id": 14,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNzczMDI0MywiaWF0IjoxNzM3NjQzODQzLCJqdGkiOiJmZTQ0YjM5YjcxM2U0YzEyYTM4MDhkZDhlY2YwNWQxMSIsInVzZXJfaWQiOjE0fQ.9F0VJltHvG8sgbNHGKe_n9bCSQ83Wa-QS1Qt_BdjlKw"
}
```
---
## ![текст](https://img.shields.io/badge/PUT-%230000FF)

#### ➡️ **URL**: [http://localhost:8181/api/v1/tourists/12/](http://localhost:8181/api/v1/tourists/)

### Вимоги до запиту:
    - Токен Bearer token
    - Користувач з роллю АДМІНІСТРАТОРА або:
        - Користувач із роллю МЕНЕДЖЕР
        - Користувач із роллю TOURIST і таким самим ідентифікатором об’єкта
        - Користувач Стафф

### Тіло запиту
```
{
    "first_name": "aaa",
    "last_name": "sss",
    "birthday": "2011-11-11",
    "phone": "+0987654321"
}
```

### Відповідь
```
{
    "id": 13,
    "user": {
        "id": 13,
        "email": "123@gmail.com",
        "role": 3,
        "is_active": false,
        "is_staff": false,
        "created_at": "2024-12-06T16:10:19.503252+02:00",
        "updated_at": "2024-12-06T16:10:19.511025+02:00"
    },
    "created_at": "2024-12-06T16:10:19.507341+02:00",
    "updated_at": "2024-12-06T16:10:19.513771+02:00",
    "first_name": "aaa",
    "last_name": "sss",
    "status": 1,
    "birthday": "2011-11-11",
    "phone": "+0987654321"
}
```
---
## ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)


#### ➡️ **URL**: [http://localhost:8181/api/v1/tourists/12/](http://localhost:8181/api/v1/tourists/)


### Вимоги до запиту:
    - Токен Bearer token
    - Користувач з роллю АДМІНІСТРАТОРА або:
        - Користувач із роллю МЕНЕДЖЕР
        - Користувач із роллю TOURIST і таким самим ідентифікатором об’єкта
        - Користувач Стафф

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
    "id": 13,
    "user": {
        "id": 13,
        "email": "123@gmail.com",
        "role": 3,
        "is_active": false,
        "is_staff": false,
        "created_at": "2024-12-06T16:10:19.503252+02:00",
        "updated_at": "2024-12-06T16:10:19.511025+02:00"
    },
    "created_at": "2024-12-06T16:10:19.507341+02:00",
    "updated_at": "2024-12-06T16:10:19.513771+02:00",
    "first_name": "qwer",
    "last_name": "rewq",
    "status": 1,
    "birthday": "2011-11-11",
    "phone": "+0987654321"
}
```
---
## ![текст](https://img.shields.io/badge/DELETE-%23FF0000)


#### ➡️ **URL**: [http://localhost:8181/api/v1/tourists/12/](http://localhost:8181/api/v1/tourists/)


### Вимоги до запиту:
    - Токен Bearer token
    - Користувач з роллю АДМІНІСТРАТОРА або:
        - Користувач із роллю МЕНЕДЖЕР
        - Користувач із роллю TOURIST і таким самим ідентифікатором об’єкта
        - Користувач Стафф

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
