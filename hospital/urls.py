from django.urls import path, include
from rest_framework import routers
from .views import HospitalViewSet, DoctorViewSet, \
                   MajorViewSet, SchoolViewSet, \
                   DashboardView, \
                   SalesHistoryListView, SalesHistoryDetailsView, \
                   SalesHistoryRecentView, ProductView, ProductDetailsView
                   
                   
router = routers.DefaultRouter()

router.register(r'hospitals', HospitalViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'majors', MajorViewSet)
router.register(r'schools', SchoolViewSet)

urlpatterns =[
    path('', include(router.urls)),
    path('saleshistory/', SalesHistoryListView.as_view(), name='sales-history'),
    path('saleshistory/<int:pk>/', SalesHistoryDetailsView.as_view(), name='sales-history-detail'),
    path('saleshistory/myhistory/', SalesHistoryRecentView.as_view(), name='sales-history-self'),
    path('dashboard/', DashboardView.as_view(), name='dash-board'),
    path('products/', ProductView.as_view(), name='product'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-details')
]

