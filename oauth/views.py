from django.shortcuts import render


def google_auth(request):
    return render(request, 'oauth/google_login.html')