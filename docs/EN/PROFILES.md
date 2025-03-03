# Documentation for profiles functionality

### 1. [Functionality](#functionality)
### 2. [API](#api)
### 3. [CRUD](#crud)
### 4. [Admin panel](#admin-panel)
### 5. [Validation](#validation)
### 5. [Permissions](#permissions)
### 6. [Table represent profiles](#table-representation)
### 7. [Json represent profiles](#Json-body-representation)
### 8. [Other](#other)

---
### Functionality

For working with profiles we have several main objects: user, administrator, manager, owner, tourist

All profile [validation](#validation) represent automation check needed fields

---

### API

Representation of all available methods and routes

### Administrator routes
```md
----------------------------------------
| Method |             URL              |
|--------|------------------------------|
|   GET  | /api/v1/administrators/      |
|--------|------------------------------|
|   GET  | /api/v1/administrators/{id}/ |
|--------|------------------------------|
|   POST | /api/v1/administrators/      |
|--------|------------------------------|
|   PUT  | /api/v1/administrators/{id}/ |
|--------|------------------------------|
|  PATCH | /api/v1/administrators/{id}/ |
|--------|------------------------------|
| DELETE | /api/v1/administrators/{id}/ |
-----------------------------------------
```

### Manager routes
```md
-----------------------------------------
| Method |             URL              |
|--------|------------------------------|
|   GET  | /api/v1/managers/            |
|--------|------------------------------|
|   GET  | /api/v1/managers/{id}/       |
|--------|------------------------------|
|   POST | /api/v1/managers/            |
|--------|------------------------------|
|   PUT  | /api/v1/managers/{id}/       |
|--------|------------------------------|
|  PATCH | /api/v1/managers/{id}/       |
|--------|------------------------------|
| DELETE | /api/v1/managers/{id}/       |
-----------------------------------------
```

### Owner routes

```md
-------------------------------------------------------
| Method |                    URL                     |
|--------|--------------------------------------------|
|   GET  | /api/v1/glamp-owners/                      |
|--------|--------------------------------------------|
|   GET  | /api/v1/glamp-owners/{id}/                 |
|--------|--------------------------------------------|
|   POST | /api/v1/glamp-owners/register-glamp_owner/ |
|--------|--------------------------------------------|
|   PUT  | /api/v1/glamp-owners/{id}/                 |
|--------|--------------------------------------------|
|  PATCH | /api/v1/glamp-owners/{id}/                 |
|--------|--------------------------------------------|
| DELETE | /api/v1/glamp-owners/{id}/                 |
-------------------------------------------------------
```

### Tourist routes
```md
-----------------------------------------------
| Method |                URL                 |
|--------|------------------------------------|
|   GET  | /api/v1/tourists/                  |
|--------|------------------------------------|
|   GET  | /api/v1/tourists/{id}/             |
|--------|------------------------------------|
|   POST | /api/v1/tourists/register-tourist/ |
|--------|------------------------------------|
|   PUT  | /api/v1/tourists/{id}/             |
|--------|------------------------------------|
|  PATCH | /api/v1/tourists/{id}/             |
|--------|------------------------------------|
| DELETE | /api/v1/tourists/{id}/             |
-----------------------------------------------
```


All POST methods must contain user field

Example registration new administrator


```json
{
  "user": {
    "email": "example@gmail.com",
    "password": "ebb949c2",
    "confirm_password": "ebb949c2"
  },
  "first_name": "aaa",
  "last_name": "bbb"
}
```
[Back](#documentation-for-profiles-functionality)

---

### CRUD

In general, all methods working as expected, but we have some differences in body request for ![POST](https://img.shields.io/badge/POST-%23FFFF00)

For every profile working one rule while creating an object. You don't need to set STATUS and ROLE

[Available ROLES](#other)
<br>
[Available STATUSES](#other)

As you can [see](#table-representation), in User table we have ```role: int ``` field. This field will be set automatically depends on which profile you create

Example

We send a POST request on route ```/api/v1/administrators/ ``` with following data
```json
{
  "user": {
    "email": "example@gmail.com",
    "password": "ebb949c2",
    "confirm_password": "ebb949c2"
  },
  "first_name": "aaa",
  "last_name": "bbb"
}
```

Now look at response

```json
{
    "id": 12,
    "user": {
        "id": 12,
        "email": "example@gmail.com",
        "role": 1, <-- ADMIN
        "is_active": true,
        "is_staff": false,
        "created_at": "2024-12-06T15:30:15.275682+02:00",
        "updated_at": "2024-12-06T15:30:15.295190+02:00"
    },
    "created_at": "2024-12-06T15:30:15.284291+02:00",
    "updated_at": "2024-12-06T15:30:15.306452+02:00",
    "first_name": "Aaa",
    "last_name": "Bbb",
    "status": 1 <-- ACTIVATED
}
```

Same response will be for any profile with needed roles and statuses

[Back](#documentation-for-profiles-functionality)

---

### Admin panel

Working from admin panel can be a little bit different from API routes

**ALL** manipulation with profiles **MUST** be in User section. 
While filling the form, we also have some [validation](#validation) before create or update objects

[Back](#documentation-for-profiles-functionality)

---

### Validation

Existing validation functionality

1) **Validation of name**: 
    - first_name, last_name validated on capitalize first letter, working also with "-" and " ' " symbols
    - length of first_name, last_name must be more than 2 characters
    - validation of contain digits or special characters


2) **Role validation**:
   - Role must be in all list of roles


3) **Birthday validation**:
   - The date of birth cannot be in the future
   - Age must be more than 18 years old
   - Age must be not more than 125 years old


4) **Phone validation**:
   - Phone number must be entered in the format: '+999999999'
   - Up to 15 digits


5) **Vip status validation**:
   - Vip status must be in all list of vip statuses


6) **Profile validation**:
   - If the user is new (not found in the database), it creates and activates the corresponding profile.
   - If the user's role has changed, it deactivates the previous profile
   - It always ensures that the profile matching the current role is activated

[Back](#documentation-for-profiles-functionality)

---

### Permissions


| Role                          | Can Edit Own Data | Can Edit Others' Data                               | Can Create Users                             | Cannot Edit Fields |
|--------------------------------|------------------|---------------------------------------------------|----------------------------------------------|------------------|
| **Tourist**                    | ✅ Yes           | ❌ No                                            | ❌ No                                       | `is_*`, `is_active`, `is_staff`, `is_superuser`, `is_deleted`, `is_banned`, `role`, `email` |
| **Owner**                      | ✅ Yes           | ❌ No                                            | ❌ No                                       | `is_*`, `is_active`, `is_staff`, `is_superuser`, `is_deleted`, `is_banned`, `role`, `email` |
| **Manager**                    | ✅ Yes           | ✅ Tourists & Owners (except `email`)           | ✅ Tourists & Owners                        | `is_*`, `is_active`, `is_staff`, `is_superuser`, `is_deleted`, `is_banned`, `role`, `email` |
| **Admin**                      | ✅ Yes           | ✅ Tourists, Owners, Managers (except `email`)  | ✅ Tourists, Owners, Managers               | `is_*`, `is_active`, `is_staff`, `is_superuser`, `is_deleted`, `is_banned`, `role`, `email` |
| **Admin + Staff**              | ✅ Yes (including `is_*`, `is_active`, `is_staff`, `is_superuser`, `is_deleted`, `is_banned`) | ✅ All users (except `email`) | ✅ Tourists, Owners, Managers, Admins | `email` |
| **Admin + Staff + Superuser**  | ✅ Yes (full access) | ✅ All users (including Admins & Staff)         | ✅ Any role                                | `email` |

---

### Glamp Creation Rules

| Role                        | Can Create Glamps? |
|-----------------------------|--------------------|
| **Tourist**                 | ❌ No             |
| **Owner**                   | ✅ Yes            |
| **Manager**                 | ✅ Yes            |
| **Admin**                   | ✅ Yes            |
| **Admin + Staff**           | ✅ Yes            |
| **Admin + Staff + Superuser** | ✅ Yes            |
| **Staff (without Admin role)** | ❌ No          |

---

## ℹ️ Key Notes

- **Only Admin + Staff and Admin + Staff + Superuser can modify `is_staff` and `is_superuser` fields.**
- **Email cannot be changed by anyone after registration.**
- **Staff role is granted only to Admins who create new Admins.**
- **To have full API access, a user must be an Admin with Staff status.**


[Back](#documentation-for-profiles-functionality)

---

### Table representation
```
User:
    email: str (unique)
    role: int
    is_active: bool
    is_staff: bool
    is_superuser: bool
    is_deleted: bool
```

```
Administrator:
    first_name: str
    last_name: str
    user: User
    status: int
```

```
Manager:
    first_name: str
    last_name: str
    user: User
    status: int
```

```
Owner:
    first_name: str
    last_name: str
    user: User
    is_hidden: bool
    is_verified: bool
    phone: str
    vip_status: int
    status: int
```

```
Tourist:
    first_name: str
    last_name: str
    user: User
    birthday: str
    phone: str
    status: int
```

### Json body representation

```
Administrator:
    {
      "user": {
        "email": "example@gmail.com",
        "password": "ebb949c2",
        "confirm_password": "ebb949c2"
      },
      "first_name": "aaa",
      "last_name": "bbb"
    }
```

```
Manager:
    {
      "user": {
        "email": "example@gmail.com",
        "password": "ri43ydQXb",
        "confirm_password": "ri43ydQXb"
      },
      "first_name": "aaa",
      "last_name": "bbb"
    }
```

```
Owner:
    {
      "user": {
        "email": "example@gmail.com",
        "password": "eb949c2",
        "confirm_password": "ebb949c2"
      },
      "first_name": "aaa",
      "last_name": "bbb",
      "phone": "+999999999"
    }
```

```
Tourist:
    {
      "user": {
        "email": "example@gmail.com",
        "password": "ebb949c2",
        "confirm_password": "ebb949c2"
      },
      "first_name": "aaa",
      "last_name": "bbb",
      "phone": "+1234567891",
      "birthday": "2000-02-02"
    }
```

### Other

```
STATUSES:
    1: ACTIVATED
    2: SUSPENDED
    3: DELETED
    4: DEACTIVATED
    5: BANNED
```

```
ROLES:
    1: ADMIN
    2: MANAGER
    3: TOURIST
    4: OWNER
```

```
VIP_STATUSES:
    1: Silver
    2: Gold
    3: Platinum
```
[Back](#documentation-for-profiles-functionality)