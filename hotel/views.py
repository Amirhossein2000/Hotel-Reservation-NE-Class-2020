from django.shortcuts import render


def home(request):
    return render(request, 'eng_panel/Home.html')

def login(request):
    return render(request, 'login.html')