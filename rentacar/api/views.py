from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Avg
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomUserChangeForm, RentingForm, CarForm, RatingForm
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .permissions import CustomIsAuthenticated, IsManagerOrAdmin
from .models import Renting, Cars, Notification, UserInfo, Rating
from .serializers import RentingSerializer, CarSerializer, UserInfoSerializer, RatingSerializer
from datetime import datetime

from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

# API VIEWS
class RentingListCreateView(generics.ListCreateAPIView):
    queryset = Renting.objects.all()
    serializer_class = RentingSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RentingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Renting.objects.all()
    serializer_class = RentingSerializer
    permission_classes = [permissions.IsAdminUser]

class CarListCreateView(generics.ListCreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAdminUser]

class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAdminUser]

class UserListCreateView(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAdminUser]



# HTML VIEWS
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            print(form.errors)
            return HttpResponse('no, you are not normal')
    else:
        form = CustomUserCreationForm()  #just a blank form
    
    return render(request, 'registration/register.html', {'form' : form})
            

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm() # blank
    return render(request, 'registration/login.html', {'form' : form})

def logout_view(request):
    logout(request)
    return redirect('login')

@api_view(['GET'])
@permission_classes([CustomIsAuthenticated])
def home(request):
    return render(request, 'pages/home.html', {'username' : request.user.username})

def access_denied(request):
    return render(request, 'errors/accessdenied.html')

@login_required(redirect_field_name="{% url 'login' %}")
def create_rental(request):

    rented_cars = Renting.objects.values_list('car_model_id', flat=True)

    cars = Cars.objects.all()
    serialized_cars = CarSerializer(cars, many=True)

    car_costs = {car.id : car.cost for car in cars}

    if request.method == 'POST':
        form = RentingForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            rental.save()
            return redirect('home')
    else:
        form = RentingForm()
    
    car_model_field = form.fields['car_model']
    choices = [(car.id, car.car_model) for car in cars]
    updated_choices = [(car_id, car_model, car_id in rented_cars) for car_id, car_model in choices]
    
    car_model_field.choices = [(car_id, car_model) for car_id, car_model, is_disabled in updated_choices]
    car_model_field.widget.choices = updated_choices

    return render(request, 'pages/rentacar.html', {'form' : form, 'cars' : serialized_cars.data, 'car_costs': car_costs})

@login_required(redirect_field_name="{% url 'login' %}")
def rented_cars(request):
    if request.method == 'GET':
        rented_cars = Renting.objects.filter(user=request.user)
        cars_with_diff_and_cost = []

        for rented_car in rented_cars:
            pick_up_date = rented_car.pick_up_date
            return_date = rented_car.return_date
            diff = abs((return_date - pick_up_date).days)

            # Access the related Cars object via the foreign key
            car = rented_car.car_model
            total_cost_per_day = car.cost
            total_cost = diff * total_cost_per_day

            rented_car.total_cost = total_cost
            rented_car.save()

            serialized_rented_car = RentingSerializer(rented_car).data
            serialized_rented_car['diff'] = diff
            serialized_rented_car['total_cost'] = total_cost

            cars_with_diff_and_cost.append(serialized_rented_car)

    return render(request, 'pages/rentedcars.html', {
        'username': request.user.username, 
        'cars': cars_with_diff_and_cost
    })

@login_required(redirect_field_name="{% url 'login' %}")
def stop_renting(request):
    if request.method == 'GET':
        cars = Renting.objects.filter(user=request.user)
        serialized_cars = RentingSerializer(cars, many=True)
        
    return render(request, 'pages/stoprenting.html', {'username' : request.user.username, 'cars' : serialized_cars.data})



class ManagerHomeView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get(self, request, format=None):
        return render(request, 'pages/managerhome.html', {'username' : request.user.username})

class ManagerRentableCarsView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get(self, request):
        cars = Cars.objects.all()
        serialized_cars = CarSerializer(cars, many=True)
        form = CarForm()  
        return render(request, 'pages/managerrentable.html', {'cars': serialized_cars.data, 'form': form})

    def post(self, request):
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            return redirect('manager-rentable-cars')
        else:
            cars = Cars.objects.all()
            serialized_cars = CarSerializer(cars, many=True)
            return render(request, 'pages/managerrentable.html', {'cars': serialized_cars.data, 'form': form})

class ManagerRentedCarsView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get(self, request):
        renting = Renting.objects.all()
        serialized_rentings = RentingSerializer(renting, many=True)
        return render(request, 'pages/managerrentedcars.html', {'rentings' : serialized_rentings.data})

class ManagerRemoveCarsView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    
    def get(self, request):
        cars = Cars.objects.all()
        serialized_cars = CarSerializer(cars, many=True)
        return render(request, 'pages/managerremovecars.html', {'cars' : serialized_cars.data})
    
class ManagerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get(self, request):
        cars = Cars.objects.all()
        rentings = Renting.objects.all()
        users = UserInfo.objects.all()

        serialized_cars = CarSerializer(cars, many=True)
        serialized_rentings = RentingSerializer(rentings, many=True)
        serialized_users = UserInfoSerializer(users, many=True)

        # amount of x
        cars_length = len(serialized_cars.data)
        rentings_length = len(serialized_rentings.data)
        users_length = len(serialized_users.data)
        

        return render(request, 'pages/managerdashboard.html', {
        'c_length' : cars_length, 'r_length' : rentings_length, 
        'u_length' : users_length, 'username' : request.user.username
        })
        
@login_required
def get_user_profile(request, username):
    user = get_object_or_404(UserInfo, username=username)
    return render(request, 'pages/profile.html', {'user' : user})


@login_required
def edit_user_profile(request, username):
    user = get_object_or_404(UserInfo, username=username)
    if request.user.username != username:
        return HttpResponseForbidden("You are not allowed")
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
        else:
            print(form.errors)
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'pages/edit_profile.html', {'form': form, 'user': user})


@login_required
def notifications(request):
    if request.method == 'GET':
        return render(request, 'pages/notifications.html')

@login_required
def check_notifications(request):
    today = timezone.now().date()
    user = request.user
    due_rentals = Renting.objects.filter(Q(return_date__lte=today) & Q(user=user))

    notifications = []
    for rental in due_rentals:
        message = f"Rental for {rental.car_model} has expired"
        notification, created = Notification.objects.get_or_create(user=user, message=message)
        notifications.append({'message' : message, 'created_at' : notification.created_at.isoformat()})

    return JsonResponse(notifications, safe=False)

def ratings(request):
    cars = Cars.objects.all()
    ratings = Rating.objects.all()
    serialized_cars = CarSerializer(cars, many=True)
    serialized_ratings = RatingSerializer(ratings, many=True)
    
    
    car_ratings = {
    car.id: round(ratings.filter(car_model=car).aggregate(average_score=Avg('score'))['average_score'] or 0, 1)
    for car in cars
    }

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ratings')
        else:
            print(form.errors)
    else:
        form = RatingForm()

    return render(request, 'pages/ratings.html', {
        'cars': serialized_cars.data,
        'ratings': serialized_ratings.data,
        'form': form,
        'car_ratings': car_ratings
    })

def heropage(request):
    return render(request, 'pages/heropage.html')

def is_auth(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')


        

            


    
    



