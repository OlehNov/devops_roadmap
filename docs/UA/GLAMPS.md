# GLAMPS

## Отримання списку всіх глемпів 

```Url``` - http://localhost:8181/api/v1/glamps/

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
            "category": "openok",
            "owner": {
                "id": 1,
                "email": "root@gmail.com",
                "first_name": "f",
                "last_name": "f",
                "is_active": true,
                "is_staff": true,
                "role": 1,
                "created_at": "2024-11-15T13:45:14.092696+02:00",
                "updated_at": "2024-11-15T13:47:03.970060+02:00"
            },
            "created_at": "2024-11-15T13:57:06.197881+02:00",
            "updated_at": "2024-11-15T14:02:21.995124+02:00",
            "glamp_type": 3,
            "name": "teseet",
            "slug": "2-test",
            "description": "tes123td",
            "capacity": 1,
            "price": "0.00",
            "status": 3,
            "street": "tests123treet",
            "building_number": null,
            "apartment": null,
            "city": "Tokiooo",
            "region": null,
            "latitude": 0.0,
            "longitude": 0.0,
            "heating_system": false,
            ...
        },
        ...
    ]
}
```

## Отримання конкретного глемпу (за id)

```Url``` - http://localhost:8181/api/v1/glamps/{glamp_id}/ замість glamp_id вставляєм id того глемпу що хочем отримати.

### Запит GET

#### Приклад відповіді на ```Url``` - http://localhost:8181/api/v1/glamps/2/

```
{
    "id": 2,
    "category": "openok",
    "owner": {
        "id": 1,
        "email": "root@gmail.com",
        "first_name": "f",
        "last_name": "f",
        "is_active": true,
        "is_staff": true,
        "role": 1,
        "created_at": "2024-11-15T13:45:14.092696+02:00",
        "updated_at": "2024-11-15T13:47:03.970060+02:00"
    },
    "created_at": "2024-11-15T13:57:06.197881+02:00",
    "updated_at": "2024-11-15T14:02:21.995124+02:00",
    "glamp_type": 3,
    "name": "teseet",
    "slug": "2-test",
    "description": "tes123td",
    "capacity": 1,
    "price": "0.00",
    "status": 3,
    "street": "tests123treet",
    "building_number": null,
    "apartment": null,
    "city": "Tokiooo",
    "region": null,
    "latitude": 0.0,
    "longitude": 0.0,
    "heating_system": false,
    "cooling_system": false,
    "internet": false,
    "laundry_services": false,
    "tv": false,
    "iron": false,
    "workplace": false,
    "pool": false,
    "spa": false,
    ...
}
```

## Створення глемпу

```Url``` - http://localhost:8181/api/v1/glamps/

### Запит POST

Для створення глемпу в системі вже повинна бути створена та категорія яка буде використана при створенні глемпу. Також всі поля нижче є обов'язковими: 

```
{
    "category": "test_cat",
    "city": "test_city",
    "glamp_type": 3,
    "name": "test_name",
    "capacity": 1,
    "status": 3,
    "description": "test",
    "street": "test_street",
    "number_of_bedrooms": 65,
    "number_of_beds": 445,
    "number_of_bathrooms": 555
}
```

***glamp_type та status покищо мають вже задані параметри і можна прописувати лише ті що є в системі. Подивитись доступні можна тут: glamp-backend\src\glamps\constants.py***

#### Приклад відповіді

```
{
    "id": 3,
    "category": "openok",
    "owner": {
        "id": 1,
        "email": "root@gmail.com",
        "first_name": "f",
        "last_name": "f",
        "is_active": true,
        "is_staff": true,
        "role": 1,
        "created_at": "2024-11-15T13:45:14.092696+02:00",
        "updated_at": "2024-11-15T13:47:03.970060+02:00"
    },
    "created_at": "2024-11-15T14:30:00.138370+02:00",
    "updated_at": "2024-11-15T14:30:00.170571+02:00",
    "glamp_type": 3,
    "name": "teseet",
    "slug": "3-teseet",
    "description": "tes123td",
    "capacity": 1,
    "price": "0.00",
    "status": 3,
    "street": "tests123treet",
    "building_number": null,
    "apartment": null,
    "city": "Tokiooo",
    "region": null,
    "latitude": 0.0,
    "longitude": 0.0,
    "heating_system": false,
    "cooling_system": false,
    "internet": false,
    ...
}
```

## Оновлення глемпу

```Url``` - http://localhost:8181/api/v1/glamps/{glamp_id}

### Запит PUT або PATCH

#### Приклад відповіді на ```Url``` - http://localhost:8181/api/v1/glamps/3/

```
{
    "id": 3,
    "category": "openok",
    "owner": {
        "id": 1,
        "email": "root@gmail.com",
        "first_name": "f",
        "last_name": "f",
        "is_active": true,
        "is_staff": true,
        "role": 1,
        "created_at": "2024-11-15T13:45:14.092696+02:00",
        "updated_at": "2024-11-15T13:47:03.970060+02:00"
    },
    "created_at": "2024-11-15T14:30:00.138370+02:00",
    "updated_at": "2024-11-15T14:33:38.659901+02:00",
    "glamp_type": 3,
    "name": "yyyyyy",
    "slug": "3-teseet",
    "description": "tesdddd123td",
    "capacity": 1,
    "price": "0.00",
    "status": 3,
    "street": "tests123dddtreet",
    "building_number": null,
    "apartment": null,
    "city": "Tokiooo",
    "region": null,
    "latitude": 0.0,
    "longitude": 0.0,
    ...
}
```

