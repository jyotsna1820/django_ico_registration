from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .views import RegisterView, ThanksPageView, activate, HomeView, IndexView, CompatibleWalletsView, SubscriptionCreate, subscribe_activate

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('register/', RegisterView.as_view(), name="register"),
    path('thanks/', ThanksPageView.as_view(), name="thanks"),
    path('compatible_wallets/', CompatibleWalletsView.as_view(), name="compatible_wallets"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', auth_views.login,{'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    path('home/', login_required(HomeView.as_view()), name="home"),
    path('subscribe/', SubscriptionCreate.as_view(), name="subscribe"),
    path('activate/<token>/', subscribe_activate, name='subscribe_activate'),

]
