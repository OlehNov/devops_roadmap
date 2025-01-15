# CHANGELOG

---
## 27.10.2024 03:16. Wash the Cat. Part 3

1. Addons added.
2. All features that are used in more than one app have been moved to addons.
3. Categories api endpoints added.
4. Washed the Cat))).
5. CHANGELOG.md added.
6. Eventlog fixed.
---
## 27.10.2024 13:16. Administrator by id fixed.
1. GET Administrator by id request fixed.
---
## 27.10.2024 23:03. Users fixed.
1. User permissions fixed.
---
## 28.10.2024 09:13. Create manager app.
1. Create model for manager profile
---
## 29.10.2024 01:00. Categories fixed.
1. Categories permissions fixed.
---
## 29.10.2024 09:57. Fixed wrong database writing for Eventlogs
1. Changed dockerfile - added command for eventlogs migrations
2. created manager for EventLog model
---
## 29.10.2024 19:50. Settings fixed.
1. DEBUG settings fixed.
---
## 30.10.20024 15:28. Users fixed.
1. Password field visible and able to write.
---
## 30.10.2024 15:40. Role check fixed.
1. Refactored user role_check decorator.
---
## 30.10.2024 18:27. Add slug.
1. Add slug for glamps.
2. Add slug for categories.
---
## 30.10.2024 19:19. Bug fixed.
1. user.signals deleted.
---
## 01.11.2024 14:43. Slug field fixed.
1. Model glamp default value equals None for slug field added.
2. Dockerfile fixed.
---
## 01.11.2024 15:15. Admin changes.
1. user id field displayed in admin.
---
## 06.11.2024 11:35. managers app.
1. Create CRUD for managers app.
---
## 09.11.2024 22:10. create glamp.
1. Commited picture in glamps.
2. Replaced uuid with id.
---
## 16.11.2024 14:16. User fixed.
1. Fields first_name and last_name in models added.
2. Defaults values for first_name and last_name added.
---
## 16.11.2024 15:24. User fixed.
1. Fields first_name and last_name in models and admin commented.
---
## 16.11.2024 16:36. Endpoint format fixed.
1. {glamp_id} instead {id}
2. {category_id} instead {id}
---
## 18.11.2024 16:36. Generate category slug.
1. The user can enter a slug for their category manually or the slug will be automatically generated based on the category name.
---
## 24.11.2024 23:09. Filters refactored.
1. QueryParamFilter refactored.
2. SortingFilter added.
## 25.11.2024 20:31. Adapting dump.json.
1. Adapting dump.json to slug in categories and glamps.
---
## 25.11.2024 11:17. Fix managers viewset.
1. Fixing CRUD managers viewset
---
## 26.11.2024 20:43. Permissions fixed.
1. Permissions for manager view fixed
---
## 26.11.2024 20:43. Categories name fixed.
1. Name in Categories fixed
---
## 27.11.2024 13:14. Administrator admin panel.
1. Refactor ADministrator profile admin panel
---
## 28.11.2024 15:44. Change save logic.
1. Change save logic for managers and administrators admin panel
---
## 28.11.2024 23:52. Categories name validation.
1. Name in Categories validation
---
## 01.12.2024 16:08. Toutists endpoints permission classes fixed.
1. Tourists endpoints views permission classes fixed.
2. Tourists views serializer added.
---
## 03.12.2024 12:03. Create CRUD for tourist profile.
1. Create full CRUD functionality for tourist profile.
---
## 06.12.2024 12:45. Moved endpoint categories and added a new one.
1. Moved categories to http://localhost:8181/api/v1/categories/.
2. Added a new endponit http://localhost:8181/api/v1/categories/{category_id}/glamps/{glamp_id}/.
---
## 14.12.2024 13:35. Fixed bugs in glamps.
1. Fixed transliteration name glamp.
2. Fixed 500 errors in glamps urls.
---
## 23.12.2024 11:17. Adapted event_log to serializers.
1. Adapted event_log to serializers.
2. Add new OperationType in event_log.
---
## 27.12.2024 15:40. Create validator for glamp price.
1. Add validator for glamp price.
2. Fix validators for glamp status and type.
---
## 07.01.2025 15:40. Connection log event.
1. Connection log event to other urls.
---
## 10.01.2025 16:35. Permissions fixed.
1. Permissions in addons/permissions module fixed.
2. addons/handlers/auth_handler.py added.
---
## 10.01.2025 16:37. LogOut Endpoint fixed.
1. UserLogoutSerializer added.
---
## 14.01.2025 15:29. Refactor ActivateUserView.
1. Refactor ActivateUserView.
2. Change activate-user endpoint
3. Change send_activation_email func for activation
---
## 16.01.2025 19:34. Add new fields in glamp model.
1. Add new fields.
2. Create new endpoints for new fields. 
---
## 19.01.2025 15:31. Fix 500 create glamp through category.
1. Fix 500 exception in create glamp through category.
2. Create new endpoints for new fields for glamp by category.
---