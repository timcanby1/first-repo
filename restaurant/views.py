from django.shortcuts import render
from .forms import BookingForm
from .models import Booking, Menu
from django.core import serializers
from datetime import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item})


@csrf_exempt
def bookings(request):
    @csrf_exempt
    def bookings(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            data['reservation_date'] = datetime.strptime(data['reservation_date'],'%Y-%m-%d').date()
        exist = Booking.objects.filter(reservation_date=data['reservation_date'],
                                       reservation_slot=data['reservation_slot']).exists()
        if not exist:
            booking = Booking(**data)
            booking.save()
            return HttpResponse(serializers.serialize('json', [booking]), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"error": "Slot already booked"}), status=400,
                                content_type='application/json')

    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    return HttpResponse(serializers.serialize('json', bookings), content_type='application/json')