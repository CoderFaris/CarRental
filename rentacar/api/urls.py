from django.urls import path
from . import views

urlpatterns = [
    # html views
    path('', views.heropage, name='heropage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('rent/', views.create_rental, name='create_rental'),
    path('rented/', views.rented_cars, name='rented'),
    path('stop-renting/', views.stop_renting, name='stop-renting'),
    path('manager-home/', views.ManagerHomeView.as_view(), name='manager-home'),
    path('manager-rentable-cars/', views.ManagerRentableCarsView.as_view(), name='manager-rentable-cars'),
    path('manager-rented-cars/', views.ManagerRentedCarsView.as_view(), name='manager-rented-cars'),
    path('manager-remove-cars/', views.ManagerRemoveCarsView.as_view(), name='manager-remove-cars'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/<str:username>', views.get_user_profile, name='profile'),
    path('profile/<str:username>/edit', views.edit_user_profile, name='edit_profile'),
    path('manager-dashboard/', views.ManagerDashboardView.as_view(), name='manager-dashboard'),
    path('ratings/', views.ratings, name='ratings'),
    

    # api views
    path('rentings/', views.RentingListCreateView.as_view(), name='renting-list-create'),
    path('rentings/<int:pk>/', views.RentingDetailView.as_view(), name='renting-detail'),
    path('cars/', views.CarListCreateView.as_view(), name='car-list-create'),
    path('cars/<int:pk>', views.CarDetailView.as_view(), name='car-detail'),
    path('check_notifications/', views.check_notifications, name='check_notifications'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.UserListCreateView.as_view(), name='users'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('is_auth/', views.is_auth, name='is-auth'),
    

    # errors
    path('access-denied/', views.access_denied, name='access_denied')
]