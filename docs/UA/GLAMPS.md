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

#### Приклад відповіді на ```Url``` - http://localhost:8181/api/v1/glamps/25/

```
{
    "id": 25,
    "category": {
        "id": 21,
        "name": "test87hf fdx1",
        "slug": "test87hf-fdx1",
    },
    "owner": {
        "id": 12,
        "email": "root@gmail.com",
    },
    ...
}
```
<details> <summary>Показати повну відповідь</summary>

```
{
    "id": 25,
    "category": {
        "id": 21,
        "name": "test87hf fdx1",
        "slug": "test87hf-fdx1",
        "created_at": "2024-12-06T13:02:50.139091+02:00",
        "updated_at": "2024-12-06T20:37:07.667645+02:00",
        "title": "ttests",
        "description": "tt",
        "is_active": true,
        "is_hidden": false
    },
    "owner": {
        "id": 12,
        "email": "root@gmail.com",
        "role": 1,
        "is_active": true,
        "is_staff": true,
        "created_at": "2024-12-06T12:57:17.031703+02:00",
        "updated_at": "2024-12-06T12:57:39.843435+02:00"
    },
    "created_at": "2024-12-06T13:03:00.714550+02:00",
    "updated_at": "2024-12-06T20:36:36.285592+02:00",
    "glamp_type": 5,
    "name": "testyyugkj",
    "slug": "25-test",
    "description": "tesd",
    "capacity": 1,
    "price": "0.00",
    "status": 3,
    "street": "tests123dddtreet",
    "building_number": null,
    "apartment": null,
    "city": "Tokiooo56",
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
    "jacuzzi": false,
    "vat": false,
    "sauna": false,
    "fireplace": false,
    "gazebo": false,
    "terrace": false,
    "barbecue_area": false,
    "hammocks": false,
    "garden_furniture": false,
    "pets_farm": false,
    "riding": false,
    "hiking_walking": false,
    "fishing": false,
    "swimming": false,
    "boating": false,
    "alpine_skiing": false,
    "meditation_yoga": false,
    "sports_area": false,
    "game_area": false,
    "events_excursions": false,
    "national_park": false,
    "sea": false,
    "lake": false,
    "stream": false,
    "waterfall": false,
    "thermal_springs": false,
    "mountains": false,
    "salt_caves": false,
    "beautiful_views": false,
    "number_of_bedrooms": 65,
    "number_of_beds": 4445,
    "cot_for_babies": false,
    "number_of_bathrooms": 555,
    "bathroom_in_room": false,
    "kitchen_in_room": false,
    "dining_area": false,
    "microwave": false,
    "plate": false,
    "refrigerator": false,
    "kitchen_on_territory": false,
    "no_kitchen": false,
    "breakfast_included": false,
    "lunch_included": false,
    "dinner_included": false,
    "all_inclusive": false,
    "room_service": false,
    "bar": false,
    "restaurant": false,
    "instant_booking": false,
    "reception_24": false,
    "free_cancellation": false,
    "allowed_with_animals": false,
    "suitable_for_children": false,
    "suitable_for_groups": false,
    "can_order_transfer": false,
    "car_charging_station": false,
    "place_for_car": false,
    "projector_and_screen": false,
    "area_for_events": false,
    "territory_under_protection": false,
    "cloakroom": false,
    "without_thresholds": false,
    "no_ladder": false,
    "bath_with_handrails": false,
    "toilet_with_handrails": false,
    "shower_chair": false,
    "suitable_for_guests_in_wheelchairs": false,
    "room_on_first_flor": false
}
```
</details>

## Створення глемпу

```Url``` - http://localhost:8181/api/v1/glamps/

### Запит POST

Для створення глемпу в системі вже повинна бути створена та категорія яка буде використана при створенні глемпу.
Щоб створити глемп потрібно вказати саме id категорії.

Також всі поля нижче є обов'язковими: 

```
{
    "category_id": 21,
    "city": "Tokiooo",
    "glamp_type": 3,
    "name": "test",
    "capacity": 1,
    "status": 3,
    "description": "tesdddd123td",
    "street": "tests123dddtreet",
    "number_of_bedrooms": 65,
    "number_of_beds": 4445,
    "number_of_bathrooms": 555
}
```

***glamp_type та status покищо мають вже задані параметри і можна прописувати лише ті що є в системі. Подивитись доступні можна тут: glamp-backend\src\glamps\constants.py***

#### Приклад відповіді

```
{
    "id": 25,
    "category": {
        "id": 21,
        "name": "test1",
        "slug": "test1",
    },
    "owner": {
        "id": 12,
        "email": "root@gmail.com",
    },
    ...
}
```

<details> <summary>Показати повну відповідь</summary>

```
{
    "id": 25,
    "category": {
        "id": 21,
        "name": "test1",
        "slug": "test1",
        "created_at": "2024-12-06T13:02:50.139091+02:00",
        "updated_at": "2024-12-06T13:02:50.139134+02:00",
        "title": "ttests",
        "description": "tt",
        "is_active": true,
        "is_hidden": false
    },
    "owner": {
        "id": 12,
        "email": "root@gmail.com",
        "role": 1,
        "is_active": true,
        "is_staff": true,
        "created_at": "2024-12-06T12:57:17.031703+02:00",
        "updated_at": "2024-12-06T12:57:39.843435+02:00"
    },
    "created_at": "2024-12-06T13:03:00.714550+02:00",
    "updated_at": "2024-12-06T13:03:00.763252+02:00",
    "glamp_type": 3,
    "name": "test",
    "slug": "25-test",
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
    "heating_system": false,
    "cooling_system": false,
    "internet": false,
    "laundry_services": false,
    "tv": false,
    "iron": false,
    "workplace": false,
    "pool": false,
    "spa": false,
    "jacuzzi": false,
    "vat": false,
    "sauna": false,
    "fireplace": false,
    "gazebo": false,
    "terrace": false,
    "barbecue_area": false,
    "hammocks": false,
    "garden_furniture": false,
    "pets_farm": false,
    "riding": false,
    "hiking_walking": false,
    "fishing": false,
    "swimming": false,
    "boating": false,
    "alpine_skiing": false,
    "meditation_yoga": false,
    "sports_area": false,
    "game_area": false,
    "events_excursions": false,
    "national_park": false,
    "sea": false,
    "lake": false,
    "stream": false,
    "waterfall": false,
    "thermal_springs": false,
    "mountains": false,
    "salt_caves": false,
    "beautiful_views": false,
    "number_of_bedrooms": 65,
    "number_of_beds": 4445,
    "cot_for_babies": false,
    "number_of_bathrooms": 555,
    "bathroom_in_room": false,
    "kitchen_in_room": false,
    "dining_area": false,
    "microwave": false,
    "plate": false,
    "refrigerator": false,
    "kitchen_on_territory": false,
    "no_kitchen": false,
    "breakfast_included": false,
    "lunch_included": false,
    "dinner_included": false,
    "all_inclusive": false,
    "room_service": false,
    "bar": false,
    "restaurant": false,
    "instant_booking": false,
    "reception_24": false,
    "free_cancellation": false,
    "allowed_with_animals": false,
    "suitable_for_children": false,
    "suitable_for_groups": false,
    "can_order_transfer": false,
    "car_charging_station": false,
    "place_for_car": false,
    "projector_and_screen": false,
    "area_for_events": false,
    "territory_under_protection": false,
    "cloakroom": false,
    "without_thresholds": false,
    "no_ladder": false,
    "bath_with_handrails": false,
    "toilet_with_handrails": false,
    "shower_chair": false,
    "suitable_for_guests_in_wheelchairs": false,
    "room_on_first_flor": false
}
```
</details>

## Оновлення глемпу

```Url``` - http://localhost:8181/api/v1/glamps/{glamp_id}

### Запит PUT або PATCH

#### Приклад відповіді на ```Url``` - http://localhost:8181/api/v1/glamps/25/


```
{
  "id": 25,
  "category": {
    "id": 21,
    "name": "test1",
    "slug": "test1"
  },
  "owner": {
    "id": 12,
    "email": "root@gmail.com"
  },
  ...
}
```
<details> <summary>Показати повну відповідь</summary>

```
{
    "id": 25,
    "category": {
        "id": 21,
        "name": "test1",
        "slug": "test1",
        "created_at": "2024-12-06T13:02:50.139091+02:00",
        "updated_at": "2024-12-06T13:02:50.139134+02:00",
        "title": "ttests",
        "description": "tt",
        "is_active": true,
        "is_hidden": false
    },
    "owner": {
        "id": 12,
        "email": "root@gmail.com",
        "role": 1,
        "is_active": true,
        "is_staff": true,
        "created_at": "2024-12-06T12:57:17.031703+02:00",
        "updated_at": "2024-12-06T12:57:39.843435+02:00"
    },
    "created_at": "2024-12-06T13:03:00.714550+02:00",
    "updated_at": "2024-12-06T13:03:00.763252+02:00",
    "glamp_type": 3,
    "name": "test",
    "slug": "25-test",
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
    "heating_system": false,
    "cooling_system": false,
    "internet": false,
    "laundry_services": false,
    "tv": false,
    "iron": false,
    "workplace": false,
    "pool": false,
    "spa": false,
    "jacuzzi": false,
    "vat": false,
    "sauna": false,
    "fireplace": false,
    "gazebo": false,
    "terrace": false,
    "barbecue_area": false,
    "hammocks": false,
    "garden_furniture": false,
    "pets_farm": false,
    "riding": false,
    "hiking_walking": false,
    "fishing": false,
    "swimming": false,
    "boating": false,
    "alpine_skiing": false,
    "meditation_yoga": false,
    "sports_area": false,
    "game_area": false,
    "events_excursions": false,
    "national_park": false,
    "sea": false,
    "lake": false,
    "stream": false,
    "waterfall": false,
    "thermal_springs": false,
    "mountains": false,
    "salt_caves": false,
    "beautiful_views": false,
    "number_of_bedrooms": 65,
    "number_of_beds": 4445,
    "cot_for_babies": false,
    "number_of_bathrooms": 555,
    "bathroom_in_room": false,
    "kitchen_in_room": false,
    "dining_area": false,
    "microwave": false,
    "plate": false,
    "refrigerator": false,
    "kitchen_on_territory": false,
    "no_kitchen": false,
    "breakfast_included": false,
    "lunch_included": false,
    "dinner_included": false,
    "all_inclusive": false,
    "room_service": false,
    "bar": false,
    "restaurant": false,
    "instant_booking": false,
    "reception_24": false,
    "free_cancellation": false,
    "allowed_with_animals": false,
    "suitable_for_children": false,
    "suitable_for_groups": false,
    "can_order_transfer": false,
    "car_charging_station": false,
    "place_for_car": false,
    "projector_and_screen": false,
    "area_for_events": false,
    "territory_under_protection": false,
    "cloakroom": false,
    "without_thresholds": false,
    "no_ladder": false,
    "bath_with_handrails": false,
    "toilet_with_handrails": false,
    "shower_chair": false,
    "suitable_for_guests_in_wheelchairs": false,
    "room_on_first_flor": false
}
```
</details> 

# GLAMPS BY CATEGORY

# Отримання списку всіх глемпів пов'язаних з категорією 

```Url``` - http://localhost:8181/api/v1/categories/{catrgory_id}/glamps/

### Запит GET

#### Приклад відповіді на ```Url``` - http://localhost:8181/api/v1/categories/21/glamps/


```
{
    "count": 2,
    "next": null,
    "previous": null,
    "page": 1,
    "pageSize": 10,
    "results": [
        {
            "id": 25,
            "category": {
                "id": 21,
                "name": "test1",
                "slug": "test1",
            },
            "owner": {
                "id": 12,
                "email": "root@gmail.com",
            },
            ...
        },
        ...
    ]
}
```
<details> <summary>Показати повну відповідь</summary>

```
{
    "count": 2,
    "next": null,
    "previous": null,
    "page": 1,
    "pageSize": 10,
    "results": [
        {
            "id": 25,
            "category": {
                "id": 21,
                "name": "test1",
                "slug": "test1",
                "created_at": "2024-12-06T13:02:50.139091+02:00",
                "updated_at": "2024-12-06T13:02:50.139134+02:00",
                "title": "ttests",
                "description": "tt",
                "is_active": true,
                "is_hidden": false
            },
            "owner": {
                "id": 12,
                "email": "root@gmail.com",
                "role": 1,
                "is_active": true,
                "is_staff": true,
                "created_at": "2024-12-06T12:57:17.031703+02:00",
                "updated_at": "2024-12-06T12:57:39.843435+02:00"
            },
            "created_at": "2024-12-06T13:03:00.714550+02:00",
            "updated_at": "2024-12-06T13:03:00.763252+02:00",
            "glamp_type": 3,
            "name": "test",
            "slug": "25-test",
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
            "heating_system": false,
            "cooling_system": false,
            "internet": false,
            "laundry_services": false,
            "tv": false,
            "iron": false,
            "workplace": false,
            "pool": false,
            "spa": false,
            "jacuzzi": false,
            "vat": false,
            "sauna": false,
            "fireplace": false,
            "gazebo": false,
            "terrace": false,
            "barbecue_area": false,
            "hammocks": false,
            "garden_furniture": false,
            "pets_farm": false,
            "riding": false,
            "hiking_walking": false,
            "fishing": false,
            "swimming": false,
            "boating": false,
            "alpine_skiing": false,
            "meditation_yoga": false,
            "sports_area": false,
            "game_area": false,
            "events_excursions": false,
            "national_park": false,
            "sea": false,
            "lake": false,
            "stream": false,
            "waterfall": false,
            "thermal_springs": false,
            "mountains": false,
            "salt_caves": false,
            "beautiful_views": false,
            "number_of_bedrooms": 65,
            "number_of_beds": 4445,
            "cot_for_babies": false,
            "number_of_bathrooms": 555,
            "bathroom_in_room": false,
            "kitchen_in_room": false,
            "dining_area": false,
            "microwave": false,
            "plate": false,
            "refrigerator": false,
            "kitchen_on_territory": false,
            "no_kitchen": false,
            "breakfast_included": false,
            "lunch_included": false,
            "dinner_included": false,
            "all_inclusive": false,
            "room_service": false,
            "bar": false,
            "restaurant": false,
            "instant_booking": false,
            "reception_24": false,
            "free_cancellation": false,
            "allowed_with_animals": false,
            "suitable_for_children": false,
            "suitable_for_groups": false,
            "can_order_transfer": false,
            "car_charging_station": false,
            "place_for_car": false,
            "projector_and_screen": false,
            "area_for_events": false,
            "territory_under_protection": false,
            "cloakroom": false,
            "without_thresholds": false,
            "no_ladder": false,
            "bath_with_handrails": false,
            "toilet_with_handrails": false,
            "shower_chair": false,
            "suitable_for_guests_in_wheelchairs": false,
            "room_on_first_flor": false
        },
        {
            "id": 26,
            "category": {
                "id": 21,
                "name": "test1",
                "slug": "test1",
                "created_at": "2024-12-06T13:02:50.139091+02:00",
                "updated_at": "2024-12-06T13:02:50.139134+02:00",
                "title": "ttests",
                "description": "tt",
                "is_active": true,
                "is_hidden": false
            },
            "owner": {
                "id": 12,
                "email": "root@gmail.com",
                "role": 1,
                "is_active": true,
                "is_staff": true,
                "created_at": "2024-12-06T12:57:17.031703+02:00",
                "updated_at": "2024-12-06T12:57:39.843435+02:00"
            },
            "created_at": "2024-12-06T16:21:35.672505+02:00",
            "updated_at": "2024-12-06T16:21:35.700858+02:00",
            "glamp_type": 3,
            "name": "test2",
            "slug": "26-test2",
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
            "heating_system": false,
            "cooling_system": false,
            "internet": false,
            "laundry_services": false,
            "tv": false,
            "iron": false,
            "workplace": false,
            "pool": false,
            "spa": false,
            "jacuzzi": false,
            "vat": false,
            "sauna": false,
            "fireplace": false,
            "gazebo": false,
            "terrace": false,
            "barbecue_area": false,
            "hammocks": false,
            "garden_furniture": false,
            "pets_farm": false,
            "riding": false,
            "hiking_walking": false,
            "fishing": false,
            "swimming": false,
            "boating": false,
            "alpine_skiing": false,
            "meditation_yoga": false,
            "sports_area": false,
            "game_area": false,
            "events_excursions": false,
            "national_park": false,
            "sea": false,
            "lake": false,
            "stream": false,
            "waterfall": false,
            "thermal_springs": false,
            "mountains": false,
            "salt_caves": false,
            "beautiful_views": false,
            "number_of_bedrooms": 65,
            "number_of_beds": 4445,
            "cot_for_babies": false,
            "number_of_bathrooms": 555,
            "bathroom_in_room": false,
            "kitchen_in_room": false,
            "dining_area": false,
            "microwave": false,
            "plate": false,
            "refrigerator": false,
            "kitchen_on_territory": false,
            "no_kitchen": false,
            "breakfast_included": false,
            "lunch_included": false,
            "dinner_included": false,
            "all_inclusive": false,
            "room_service": false,
            "bar": false,
            "restaurant": false,
            "instant_booking": false,
            "reception_24": false,
            "free_cancellation": false,
            "allowed_with_animals": false,
            "suitable_for_children": false,
            "suitable_for_groups": false,
            "can_order_transfer": false,
            "car_charging_station": false,
            "place_for_car": false,
            "projector_and_screen": false,
            "area_for_events": false,
            "territory_under_protection": false,
            "cloakroom": false,
            "without_thresholds": false,
            "no_ladder": false,
            "bath_with_handrails": false,
            "toilet_with_handrails": false,
            "shower_chair": false,
            "suitable_for_guests_in_wheelchairs": false,
            "room_on_first_flor": false
        }
    ]
}
```
</details>

# Отримання конкретного глемпу який пов'язаний з категорією 

```Url``` - http://localhost:8181/api/v1/categories/{catrgory_id}/glamps/{glamp_id}/

### Запит GET

#### Приклад відповіді на ```Url``` - http://localhost:8181/api/v1/categories/21/glamps/25/


```
{
    "id": 25,
    "category": {
        "id": 21,
        "name": "test1",
        "slug": "test1",
    },
    "owner": {
        "id": 12,
        "email": "root@gmail.com",
    },
    ...
}
```
<details> <summary>Показати повну відповідь</summary>

```
{
    "id": 25,
    "category": {
        "id": 21,
        "name": "test1",
        "slug": "test1",
        "created_at": "2024-12-06T13:02:50.139091+02:00",
        "updated_at": "2024-12-06T13:02:50.139134+02:00",
        "title": "ttests",
        "description": "tt",
        "is_active": true,
        "is_hidden": false
    },
    "owner": {
        "id": 12,
        "email": "root@gmail.com",
        "role": 1,
        "is_active": true,
        "is_staff": true,
        "created_at": "2024-12-06T12:57:17.031703+02:00",
        "updated_at": "2024-12-06T12:57:39.843435+02:00"
    },
    "created_at": "2024-12-06T13:03:00.714550+02:00",
    "updated_at": "2024-12-06T13:03:00.763252+02:00",
    "glamp_type": 3,
    "name": "test",
    "slug": "25-test",
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
    "heating_system": false,
    "cooling_system": false,
    "internet": false,
    "laundry_services": false,
    "tv": false,
    "iron": false,
    "workplace": false,
    "pool": false,
    "spa": false,
    "jacuzzi": false,
    "vat": false,
    "sauna": false,
    "fireplace": false,
    "gazebo": false,
    "terrace": false,
    "barbecue_area": false,
    "hammocks": false,
    "garden_furniture": false,
    "pets_farm": false,
    "riding": false,
    "hiking_walking": false,
    "fishing": false,
    "swimming": false,
    "boating": false,
    "alpine_skiing": false,
    "meditation_yoga": false,
    "sports_area": false,
    "game_area": false,
    "events_excursions": false,
    "national_park": false,
    "sea": false,
    "lake": false,
    "stream": false,
    "waterfall": false,
    "thermal_springs": false,
    "mountains": false,
    "salt_caves": false,
    "beautiful_views": false,
    "number_of_bedrooms": 65,
    "number_of_beds": 4445,
    "cot_for_babies": false,
    "number_of_bathrooms": 555,
    "bathroom_in_room": false,
    "kitchen_in_room": false,
    "dining_area": false,
    "microwave": false,
    "plate": false,
    "refrigerator": false,
    "kitchen_on_territory": false,
    "no_kitchen": false,
    "breakfast_included": false,
    "lunch_included": false,
    "dinner_included": false,
    "all_inclusive": false,
    "room_service": false,
    "bar": false,
    "restaurant": false,
    "instant_booking": false,
    "reception_24": false,
    "free_cancellation": false,
    "allowed_with_animals": false,
    "suitable_for_children": false,
    "suitable_for_groups": false,
    "can_order_transfer": false,
    "car_charging_station": false,
    "place_for_car": false,
    "projector_and_screen": false,
    "area_for_events": false,
    "territory_under_protection": false,
    "cloakroom": false,
    "without_thresholds": false,
    "no_ladder": false,
    "bath_with_handrails": false,
    "toilet_with_handrails": false,
    "shower_chair": false,
    "suitable_for_guests_in_wheelchairs": false,
    "room_on_first_flor": false
}
```
</details>

## Створення глемпу для конкретної категорії 

```Url``` - http://localhost:8181/api/v1/categories/{catrgory_id}/glamps/

### Запит POST

Тут сенс в тому що для цього урла не потрібно вказувати id категорії, він буде автоматично підставлятись з того id що вказаний в урлі.

Всі поля нижче є обов'язковими: 

```
{
    "city": "Tokiooo56",
    "glamp_type": 5,
    "name": "test45",
    "capacity": 1,
    "status": 3,
    "description": "tesd",
    "street": "tests123dddtreet",
    "number_of_bedrooms": 65,
    "number_of_beds": 4445,
    "number_of_bathrooms": 555
}
```

#### Приклад відповіді

```
{
    "id": 27,
    "category": {
        "id": 21,
        "name": "test87hf fdx1",
        "slug": "test87hf-fdx1",
    },
    "owner": {
        "id": 12,
        "email": "root@gmail.com",
    },
    ...
}
```
<details> <summary>Показати повну відповідь</summary>

```
{
    "id": 27,
    "category": {
        "id": 21,
        "name": "test87hf fdx1",
        "slug": "test87hf-fdx1",
        "created_at": "2024-12-06T13:02:50.139091+02:00",
        "updated_at": "2024-12-06T20:37:07.667645+02:00",
        "title": "ttests",
        "description": "tt",
        "is_active": true,
        "is_hidden": false
    },
    "owner": {
        "id": 12,
        "email": "root@gmail.com",
        "role": 1,
        "is_active": true,
        "is_staff": true,
        "created_at": "2024-12-06T12:57:17.031703+02:00",
        "updated_at": "2024-12-06T12:57:39.843435+02:00"
    },
    "created_at": "2024-12-06T20:42:56.713246+02:00",
    "updated_at": "2024-12-06T20:42:56.736277+02:00",
    "glamp_type": 5,
    "name": "test45",
    "slug": "27-test45",
    "description": "tesd",
    "capacity": 1,
    "price": "0.00",
    "status": 3,
    "street": "tests123dddtreet",
    "building_number": null,
    "apartment": null,
    "city": "Tokiooo56",
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
    "jacuzzi": false,
    "vat": false,
    "sauna": false,
    "fireplace": false,
    "gazebo": false,
    "terrace": false,
    "barbecue_area": false,
    "hammocks": false,
    "garden_furniture": false,
    "pets_farm": false,
    "riding": false,
    "hiking_walking": false,
    "fishing": false,
    "swimming": false,
    "boating": false,
    "alpine_skiing": false,
    "meditation_yoga": false,
    "sports_area": false,
    "game_area": false,
    "events_excursions": false,
    "national_park": false,
    "sea": false,
    "lake": false,
    "stream": false,
    "waterfall": false,
    "thermal_springs": false,
    "mountains": false,
    "salt_caves": false,
    "beautiful_views": false,
    "number_of_bedrooms": 65,
    "number_of_beds": 4445,
    "cot_for_babies": false,
    "number_of_bathrooms": 555,
    "bathroom_in_room": false,
    "kitchen_in_room": false,
    "dining_area": false,
    "microwave": false,
    "plate": false,
    "refrigerator": false,
    "kitchen_on_territory": false,
    "no_kitchen": false,
    "breakfast_included": false,
    "lunch_included": false,
    "dinner_included": false,
    "all_inclusive": false,
    "room_service": false,
    "bar": false,
    "restaurant": false,
    "instant_booking": false,
    "reception_24": false,
    "free_cancellation": false,
    "allowed_with_animals": false,
    "suitable_for_children": false,
    "suitable_for_groups": false,
    "can_order_transfer": false,
    "car_charging_station": false,
    "place_for_car": false,
    "projector_and_screen": false,
    "area_for_events": false,
    "territory_under_protection": false,
    "cloakroom": false,
    "without_thresholds": false,
    "no_ladder": false,
    "bath_with_handrails": false,
    "toilet_with_handrails": false,
    "shower_chair": false,
    "suitable_for_guests_in_wheelchairs": false,
    "room_on_first_flor": false
}
```
</details>