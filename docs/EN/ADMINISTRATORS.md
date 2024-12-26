# ADMINISTRATORS


### Available methods


- ![текст](https://img.shields.io/badge/GET-%2390EE90)
- ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)
- ![текст](https://img.shields.io/badge/POST-%23FFFF00)
- ![текст](https://img.shields.io/badge/PUT-%230000FF)
- ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)
- ![текст](https://img.shields.io/badge/DELETE-%23FF0000)

---
## ![GET](https://img.shields.io/badge/GET-%2390EE90)

#### ➡️ **URL**: [http://localhost:8181/api/v1/administrators/](http://localhost:8181/api/v1/administrators/)

### Request Requirements:
 - Authentication Bearer token
 - User with ADMINISTRATOR role or:
    - User stuff


#### Response

```
{
    "count": 1,
    "next": null,
    "previous": null,
    "page": 1,
    "pageSize": 10,
    "results": [
        {
            "id": 12,
            "user": {
                "id": 12,
                "email": "a@gmail.com",
                "role": 1,
                "is_active": true,
                "is_staff": false,
                "created_at": "2024-12-06T15:30:15.275682+02:00",
                "updated_at": "2024-12-06T15:30:15.295190+02:00"
            },
            "created_at": "2024-12-06T15:30:15.284291+02:00",
            "updated_at": "2024-12-06T15:30:15.306452+02:00",
            "first_name": "aaa",
            "last_name": "bbb",
            "status": 1
        }
    ]
}
```
---
## ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)

#### ➡️ **URL**: [http://localhost:8181/api/v1/administrators/12/](http://localhost:8181/api/v1/administrators/12/)


### Request Requirements:
 - Authentication Bearer token
 - User with ADMINISTRATOR role or:
    - User with ADMINISTRATOR role and same object id
    - User stuff

#### Response
```
{
    "id": 12,
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "role": 1,
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-12-06T15:30:15.275682+02:00",
        "updated_at": "2024-12-06T15:30:15.295190+02:00"
    },
    "created_at": "2024-12-06T15:30:15.284291+02:00",
    "updated_at": "2024-12-06T15:30:15.306452+02:00",
    "first_name": "aaa",
    "last_name": "bbb",
    "status": 1
}
```
---
![текст](https://img.shields.io/badge/POST-%23FFFF00)

#### ➡️ **URL**: [http://localhost:8181/api/v1/administrators/](http://localhost:8181/api/v1/administrators/)

### Request Requirements:
 - Authentication Bearer token
 - User with ADMINISTRATOR role or:
    - User stuff

#### Request Body

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

#### Response
```
{
    "id": 12,
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "role": 1,
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-12-06T15:30:15.275682+02:00",
        "updated_at": "2024-12-06T15:30:15.295190+02:00"
    },
    "created_at": "2024-12-06T15:30:15.284291+02:00",
    "updated_at": "2024-12-06T15:30:15.306452+02:00",
    "first_name": "aaa",
    "last_name": "bbb",
    "status": 1
}
```
---
## ![текст](https://img.shields.io/badge/PUT-%230000FF)

#### ➡️ **URL**: [http://localhost:8181/api/v1/administrators/12/](http://localhost:8181/api/v1/administrators/)

### Request Requirements:
 - Authentication Bearer token
 - User with ADMINISTRATOR role or:
    - User with ADMINISTRATOR role and same id
    - User stuff

### Request Body
```
{
    "first_name": "aaa",
    "last_name": "sss"
}
```

### Response
```
{
    "id": 12,
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "role": 1,
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-12-06T15:30:15.275682+02:00",
        "updated_at": "2024-12-06T15:30:15.295190+02:00"
    },
    "created_at": "2024-12-06T15:30:15.284291+02:00",
    "updated_at": "2024-12-06T15:36:18.724026+02:00",
    "first_name": "sss",
    "last_name": "fff",
    "status": 1
}
```
---
## ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)

#### ➡️ **URL**: [http://localhost:8181/api/v1/administrators/12/](http://localhost:8181/api/v1/administrators/)


### Request Requirements:
 - Authentication Bearer token
 - User with ADMINISTRATOR role or:
    - User with ADMINISTRATOR role and same object id
    - User stuff

## Request Body
```
{
    "last_name": "fff"
}
```

## Response
```
{
    "id": 12,
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "role": 1,
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-12-06T15:30:15.275682+02:00",
        "updated_at": "2024-12-06T15:30:15.295190+02:00"
    },
    "created_at": "2024-12-06T15:30:15.284291+02:00",
    "updated_at": "2024-12-06T15:38:05.693805+02:00",
    "first_name": "sss",
    "last_name": "fff",
    "status": 1
}
```
---
## ![текст](https://img.shields.io/badge/DELETE-%23FF0000)

#### ➡️ **URL**: [http://localhost:8181/api/v1/administrators/12/](http://localhost:8181/api/v1/administrators/)


### Request Requirements:
 - Authentication Bearer token
 - User with ADMINISTRATOR role or:
    - User with ADMINISTRATOR role and same object id
    - User stuff

## Request Body
```
None
```

## Response
```
{
    "detail": "Object deactivated successfully."
}
```
