from django.urls import path
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

# router.register(r'order', ecommerce_views.OrderViewSet, basename='order')



app_name = 'account'

router = routers.DefaultRouter()
router.register(r'profiles', views.ProfileView, basename='profiles')
# router.register(r'buying', views.OrderViewSet, basename='buying')

urlpatterns = router.urls

urlpatterns += [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_pwd/', views.reset_pwd, name='reset_pwd'),
    path('buying/', views.buying, name='buying'),
    path('selling/', views.selling, name='selling'),
    path('profile/<username>', views.profile, name='profile'),
    # path('profiles/', views.ProfileView.as_view(), name='profiles'),
    path('dashboard/<username>', views.dashboard, name='dashboard'),
]
