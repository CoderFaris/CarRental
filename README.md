# Car Rental Website

## Overview

This Car Rental Website is a full-stack project designed to facilitate the process of renting cars online. The system includes user registration and login, car rental functionalities, and an administrative dashboard for managers. The project also provides API endpoints for administrative tasks using Django Rest Framework (DRF).

## Features

### User Features
1. **User Registration and Login**
   - Users can create an account and log in to the system.

2. **Car Rental System**
   - Users can browse available cars and rent them.
   - Users can view their rented cars.
   - Users can stop renting a car.

3. **Profile Management**
   - Users can edit their profile information.

### Manager Features
1. **Manager Dashboard**
   - View statistics such as the number of users, rentals, and cars.

2. **Car Management**
   - Add new cars to the inventory.
   - View all cars in the inventory.
   - Remove cars from the inventory.

3. **Rental Management**
   - View details of who has rented which cars.

### API Endpoints (Admin Only)
- View and manage users.
- View and manage cars.
- View and manage rentals.


## Installation

### Prerequisites (step by step)
- Python 3.x
- pip install -r requirements.txt
- cd to manage.py
- python manage.py migrate
- python manage.py runserver


## URL PATHS
- register/
- login/
- home/
- rent/
- rented/
- stop-renting/
- manager-home/
- manager-rentable-cars/
- manager-rented-cars/
- manager-remove-cars/
- notifications/
- profile/username
- profile/username/edit
- manager-dashboard/
- ratings/

## API ENDPOINTS
- cars/
- cars/{carID}
- users/
- users/{userID}
- rentings/
- rentings/{rentingID}

## Contributions
1. Fork the repository
2. Create a new branch
3. Make your changes and commit them
4. Push your branch and submit a pull request







