from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from django.shortcuts import redirect

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, NotAuthenticated) or isinstance(exc, PermissionDenied):
        return redirect('access_denied')
    
    return response
