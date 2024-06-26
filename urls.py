"""
URL configuration for GameCollectionAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from GameCollectionAPI.views import register_user, login_user, Users, GameViewSet, CollectionViewSet, RatingViewSet, PlatformViewSet, AllCollectionsViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', Users, basename='user')
router.register(r'game', GameViewSet, basename='game')
router.register(r'collection', CollectionViewSet, basename='collection')
router.register(r'rating', RatingViewSet, basename='rating')
router.register(r'platforms', PlatformViewSet, basename='platform')
router.register(r'all-collections', AllCollectionsViewSet, basename='all-collections')

urlpatterns = [
    path("", include(router.urls)),
    path("register/", register_user, name='register'),
    path('login/', login_user, name='login'),
    path("api-token-auth/", obtain_auth_token, name='api_token_auth'),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]