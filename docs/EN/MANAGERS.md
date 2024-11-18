# MANAGERS


### Available methods


- ![текст](https://img.shields.io/badge/GET-%2390EE90)
- ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)
- ![текст](https://img.shields.io/badge/POST-%23FFFF00)
- ![текст](https://img.shields.io/badge/PUT-%230000FF)
- ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)
- ![текст](https://img.shields.io/badge/DELETE-%23FF0000)

---
## ![GET](https://img.shields.io/badge/GET-%2390EE90)

#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/](http://localhost:8181/api/v1/managers/)

### Request Requirements:
 - Authentication Bearer token
 - User with ADMIN role or:
    - User with MANAGER role
    - User stuff


#### Output

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
                "role": 2,
                "is_active": true,
                "is_staff": false,
                "created_at": "2024-11-18T10:45:57.571374+02:00",
                "updated_at": "2024-11-18T10:45:57.580688+02:00"
            },
            "first_name": "avs",
            "last_name": "vgs",
            "status": 1
        }
    ]
}
```
---
## ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)

#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/12/](http://localhost:8181/api/v1/managers/12/)


### Request Requirements:
 - Authentication Bearer token
 - User with ADMIN role:
    - User with MANAGER role and same object id
    - User stuff

#### Response
```
{
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "role": 2,
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-11-18T10:45:57.571374+02:00",
        "updated_at": "2024-11-18T10:45:57.580688+02:00"
    },
    "first_name": "avs",
    "last_name": "vgs",
    "status": 1
}
```
---
![текст](https://img.shields.io/badge/POST-%23FFFF00)

#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/](http://localhost:8181/api/v1/managers/)

### Request Requirements:
 - Authentication Bearer token
 - User with ADMIN role or:
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
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "role": 2
        "is_active": true,
        "is_staff": false,
    },
    "first_name": "aaa",
    "last_name": "bbb"
    "status": 1,
}
```
---
## ![текст](https://img.shields.io/badge/PUT-%230000FF)

#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/12/](http://localhost:8181/api/v1/managers/)
### Request Requirements:
 - Authentication Bearer token
 - User with ADMIN role or:
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
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "role": 2,
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-11-12T15:10:12.433051+02:00",
        "updated_at": "2024-11-12T15:10:12.442579+02:00"
    },
    "first_name": "aaa",
    "last_name": "sss",
    "status": 1,
}
```
---
## ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)
#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/12/](http://localhost:8181/api/v1/managers/)
### Request Requirements:
 - Authentication Bearer token
 - User with ADMIN role or:
    - User with MANAGER role and same object id
    - User stuff

## Request Body
```
{
    "first_name": "qwer",
    "last_name": "rewq"
}
```

## Response
```
{
    "user": {
        "id": 12,
        "email": "a@gmail.com",
        "role": 2,
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-11-12T15:10:12.433051+02:00",
        "updated_at": "2024-11-12T15:10:12.442579+02:00"
    },
    "first_name": "qwer",
    "last_name": "rewq",
    "status": 1,
}
```
---
## ![текст](https://img.shields.io/badge/DELETE-%23FF0000)
#### ➡️ **URL**: [http://localhost:8181/api/v1/managers/12/](http://localhost:8181/api/v1/managers/)
### Request Requirements:
 - Authentication Bearer token
 - User with ADMIN role or:
    - User with MANAGER role and same object id
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
