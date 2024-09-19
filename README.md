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
# Authentication and Authorization
1. user/forms.py
* Consists of 'RegisterForm', 'LoginForm', 'PasswordResetEmailForm', 'PasswordResetEmailForm'
* RegisterForm
'RegisterForm' makes sure that 'username' and 'email' is unique with 'clean_username' and 'clean_email' functions
'password' and 'confirm' must be equal. If they are not equal 'clean' function will prevent registration
* LoginForm, PasswordResetEmailForm, SetNewResetPasswordForm will have their own behavior
2. user/tokens.py
* AccountActivationTokenGenerator will generate the hash value that we will send to the user's email
3. user/views.py
* **register_user**
* If user is authenticated (already registered) then the page will be redirected to the home page
* If user is not authenticated and 'request.method' is 'GET' method then 'form' will be invalid and the page will be redirected to register page
* If user is not authenticated and 'request.method' is 'POST' method and 'form' is valid then we will send verification mail to user's email. Notice that we set 'user.is_active' to 'False'. With help of this user will not login
* **activate**
* After the email is sent to the user's email, the user must click on the link. If everything is okey then we set 'user.is_active' to 'True'. So that user will be login. At the end we will redirect to the home page
* **login_user**
* If user is authenticated (already registered) then the page will be redirected to the home page
* If user is not authenticated and 'request.method' is 'GET' method then 'form' will be invalid and the page will be redirected to login page
* If user is not authenticated and 'request.method' is 'POST' method and 'form' is valid then we will login user
* **password_reset_email** have same logic with 'register_user' function
* **set_new_password** have same logic with 'activate' function
