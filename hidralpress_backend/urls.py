"""hidralpress_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from imagens.views import OSViewSet, SectorViewSet, StepViewSet, ImageViewSet, StepOsViewSet, ValidateOSView
from django.contrib import admin

router = DefaultRouter()
router.register(r'os', OSViewSet, basename='os')
router.register(r'sectors', SectorViewSet, basename='sector')
router.register(r'steps', StepViewSet, basename='step')
router.register(r'steps-os', StepOsViewSet, basename='step-os')
router.register(r'images', ImageViewSet, basename='image')
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path('validate-os/', ValidateOSView.as_view())
]
