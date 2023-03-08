from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('buying/', views.buying, name='buying'),
    path('selling/', views.selling, name='selling'),
    path('profile/<username>', views.profile, name='profile'),
    path('dashboard/<username>', views.dashboard, name='dashboard'),
]