from django.http import HttpResponse
from .models import User

def activate_account(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()
        return HttpResponse('Your account has been activated. You can now log in.')
    else:
        return HttpResponse('Invalid activation link.')