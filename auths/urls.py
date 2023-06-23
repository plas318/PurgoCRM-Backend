'''
Basic router url provides these endpoints:

GET /users/: Retrieve a list of all users
POST /users/: Create a new user
GET /users/{pk}/: Retrieve a single user by primary key
PUT /users/{pk}/: Update a single user by primary key
PATCH /users/{pk}/: Partially update a single user by primary key
DELETE /users/{pk}/: Delete a single user by primary key

'''

from rest_framework import routers
from django.urls import path
from .views import UserViewSet, DepartmentViewSet, LoginView, RegisterView, LogoutView

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
