from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.datetime_safe import date
from django.views import generic
from hotel.models import Room, Reservation, Service
from django.http import HttpResponse


def Signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def ShowReserves(request):
    if request.method == 'GET':
        room_number = request.GET.get("room_number")
        reserves = Reservation.objects.filter(room_id=room_number)
        services = Service.objects.all()

        return render(request, 'showreserves.html',
                      {'reserves': reserves, 'room_number': room_number, 'services': services})

    if request.method == 'POST':
        room_number = request.GET.get("room_number")
        form = request.POST

        st = form['start_time']
        et = form['end_time']
        msg = "Hotel is Reserved in range ", st, " between ", et
        bad_days = Reservation.objects.filter(start_time__range=(st, et)).all()
        if len(bad_days) > 0:
            return HttpResponse(msg)

        bad_days = Reservation.objects.filter(end_time__range=(st, et)).all()
        if len(bad_days) > 0:
            return HttpResponse(msg)

        amount = Room.objects.filter(room_number=room_number).values('amount')
        new_reserve = Reservation(room_id=room_number, user=request.user,
                                  start_time=st,
                                  end_time=et, amount=amount)
        new_reserve.save()

        services = form['services']
        for s in services:
            new_reserve.services.add(s)
        new_reserve.save()

        return HttpResponse("reserved successfully!")


def HomeView(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            rooms = Room.objects.all()
            context = {
                "rooms": rooms
            }
            return render(request, 'home.html', context=context)
    else:
        if request.method == 'GET':
            return redirect('login')


class Login(generic.View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password is not correct')
            return redirect('login')

    def get(self, request):
        if not request.user.is_authenticated:

            return render(request, 'login.html')
        else:
            return redirect('home')


def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
