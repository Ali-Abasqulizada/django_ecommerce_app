# Django-Ecommerce-App
# Local Setup
1. Make sure you have python installed
2. Install dependencies: Run below command
3. pip install -r requirements
4. Change 'EMAIL_HOST_USER' in ecommerce/settings.py
5. Change 'EMAIL_HOST_PASSWORD' in ecommerce/settings.py
Note: How to get password
* Go to your google account
* Click 'Manage your Google Account'
* Go to 'Security' section
* Turn on '2-Step Verification'
* When you done search for 'App passwords'
* Create your password here
6. Change 'SECRET_KEY' in ecommerce/settings.py
7. Change 'DEBUG' in ecommerce/settings.py to True if you want to test. (Optional)
# Templates
* Folder structure
```
├───templates
│   ├───assets
│   ├───core
│   └───user
```

* Make sure you have this code
```
TEMPLATES = [
    {
	...
	'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Template files will be located here
	...
    },
]
```
# Static Files
* Folder structure
```
├───static
│   ├───assets
│   ├───core
│   ├───fonts
│   ├───img
│   └───js
```

* Make sure you have this code
```
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')  # Static files will be located here during development
]
```
# Media Files
* Make sure you have this code
```
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # This is where the media files will be stored
```
* Don't forget to add this code to ecommerce/urls.py file
```
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [...]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # You can remove this before deployment
```
