# CATEGORIES

## Get a list of all categories

```Url``` - http://localhost:8181/api/v1/glamps/categories/

### Request GET

#### An example of a response

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

## Getting a specific category (by slug)

```Url``` - http://localhost:8181/api/v1/glamps/categories/{slug} instead of slug, insert the slug of the category you want to get.

### Request GET

#### An example of a response to ```Url``` - http://localhost:8181/api/v1/glamps/categories/bobr-kurwa

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

## Create a category 

```Url``` - http://localhost:8181/api/v1/glamps/categories/

### Request POST

To create a category, you need to specify the following fields: 

```
{
    "name": "testname",
    "slug": "testslug",
    "title": "testtitle",
    "description": "testdescription"
}
```

***Slug explanation is a field that is used to search for a specific category (see above). The slug must be unique and meet certain requirements. It can only consist of Latin characters, numbers, hyphens, and underscores.***

*Another point, if you create a category through the admin panel, the slug will be automatically generated in real time, but you can change it (it's just a convenience). However, if you create through Postman, as I showed earlier, the slug field must be written with handles.*

#### An example of a response

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