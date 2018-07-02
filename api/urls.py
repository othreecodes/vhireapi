from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework.authtoken import views as rviews

router = routers.DefaultRouter()
router.register(r'users', views.UserViewset)
router.register(r'bookings', views.BookingViewset)
router.register(r'jobs', views.JobViewset)
router.register(r'types', views.JobTypeViewset)
router.register(r'categories', views.JobCategoryViewset)
router.register(r'identifications', views.UserIdViewset)
router.register(r'invoices', views.InvoiceViewset)
router.register(r'applicants', views.JobApplicationViewset)
router.register(r'services', views.ServiceViewSet)
router.register(r'sessions', views.SessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', rviews.obtain_auth_token),
]
