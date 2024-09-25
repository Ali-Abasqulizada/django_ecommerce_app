from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.contrib import messages

class AdminSuperuserRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):  # This ensures it's the admin path
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)  # Redirect to login if not authenticated
            elif not request.user.is_staff:
                messages.error(request, 'You have not access')
                return redirect(settings.LOGIN_URL) 

        response = self.get_response(request)
        return response