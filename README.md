# Forefront HQ

## Table of Contents


- Testing
    - Bugs Discovered

## Bugs Discovered

### Bug 1 — `ModuleNotFoundError: No module named 'forefront_hq'`
**Description:** After renaming the Django config package from `webhive` to `forefront_hq`, Heroku could not find the settings module on deployment.  
**Cause:** The `DJANGO_SETTINGS_MODULE` config var on Heroku still pointed to `webhive.settings` after the rename.  
**Fix:** Updated the Heroku config var via CLI:
```
heroku config:set DJANGO_SETTINGS_MODULE=forefront_hq.settings --app forefront-hq
```

---

### Bug 2 - `Bad Request (400)` on Deployed Heroku App
**Description:** The deployed app returned a 400 error immediately after the Heroku app was renamed.  
**Cause:** `ALLOWED_HOSTS` in `settings.py` still contained the old Heroku hostname (`webhive-ca8f62799334.herokuapp.com`). Heroku also retains a random suffix in the hostname after a rename, meaning the expected clean URL `forefront-hq.herokuapp.com` was never the actual hostname.  
**Fix:** Updated `ALLOWED_HOSTS` to include the correct hostname:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'forefront-hq-cd14dedc71a3.herokuapp.com']
```

---

### Bug 3 — `Not Found (404)` After Fixing ALLOWED_HOSTS
**Description:** App returned a 404 on all routes after the 400 was resolved.  
**Cause:** `ROOT_URLCONF` was defined twice in `settings.py` — the first instance (`webhive.urls`) was conflicting with the correct one (`forefront_hq.urls`). The `accounts/urls.py` file also did not exist yet.  
**Fix:** Removed the duplicate `ROOT_URLCONF` entry and created `accounts/urls.py` with the required URL patterns.
 
---

### Bug 4 — `ModuleNotFoundError: No module named 'accounts.urls'`
**Description:** Internal server error (500) on all routes after the 404 was resolved.  
**Cause:** `forefront_hq/urls.py` included `accounts.urls` but the file did not exist.  
**Fix:** Created `accounts/urls.py` with a basic home route.
 
---
 
### Bug 5 — `ImproperlyConfigured: allauth.account.middleware.AccountMiddleware`
**Description:** Server failed to start after installing `django-allauth`.  
**Cause:** The allauth middleware was not added to `MIDDLEWARE` in `settings.py`.  
**Fix:** Added `allauth.account.middleware.AccountMiddleware` to the bottom of the `MIDDLEWARE` list:
```python
'allauth.account.middleware.AccountMiddleware',
```
 
---
 
### Bug 6 — `ModuleNotFoundError: No module named 'requests'`
**Description:** Server failed to start after adding allauth social account providers.  
**Cause:** The `requests` package was not installed in the virtual environment.  
**Fix:** Ran the following and updated `requirements.txt`:
```
pip install requests
```
 
---
 
### Bug 7 — `ModuleNotFoundError: No module named 'jwt'`
**Description:** Server failed to start after installing `requests`.  
**Cause:** The `PyJWT` package required by allauth's Google provider was not installed.  
**Fix:** Ran the following and updated `requirements.txt`:
```
pip install PyJWT
```
 
---
 
### Bug 8 — `ModuleNotFoundError: No module named 'cryptography'`
**Description:** Server failed to start after installing `PyJWT`.  
**Cause:** The `cryptography` package required by allauth was not installed.  
**Fix:** Ran the following and updated `requirements.txt`:
```
pip install cryptography
```
 
---
 
### Bug 9 — Static Files Not Loading on Heroku
**Description:** CSS, images and JS were not being served on the deployed app.  
**Cause:** `whitenoise` was not installed, `STATIC_ROOT` was not set, and `DISABLE_COLLECTSTATIC` was not configured in Heroku config vars.  
**Fix:**
 
* Installed `whitenoise` and added it to `MIDDLEWARE`
* Added `STATIC_ROOT = BASE_DIR / 'staticfiles'` to `settings.py`
* Set `DISABLE_COLLECTSTATIC = 0` in Heroku config vars
---
 
### Bug 10 — Admin Login Failing With Correct Credentials
**Description:** Could not log in to the Django admin panel despite using the correct superuser credentials.  
**Cause:** The superuser was created before `django-allauth` was installed. Allauth changes the authentication backend which caused a mismatch with the existing superuser.  
**Fix:** Reset the superuser password via CLI:
```
python manage.py changepassword AshRoberts
```
 
---

