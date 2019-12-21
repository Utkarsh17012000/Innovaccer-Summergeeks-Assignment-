from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('<int:account_id>/delete/',views.delete_account,name="delete"),
    path('<int:visitor_id>/meeting/',views.meeting,name="meeting"),
    path('<int:relogin_id>/welcome/',views.relogin,name="relogin"),
]