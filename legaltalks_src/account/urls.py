from django.urls import path
from . import views as account_views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('signup/advocate/', account_views.advocate_signup, name='advocate-signup'),
    path('signup/advocate/verification/', account_views.code_verification, name='code-verification'),
    path('signup/advocate/join/', account_views.verification_success, name='verification-success'),
    path('signup/advocate/resend-code/', account_views.resend_code, name='resend-code'),
    path('signup/', account_views.user_signup, name='user-signup'),
    path('signup/profile-creation/', account_views.profile_signup, name='profile-creation'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('my-profile/', account_views.my_profile, name='my-profile'),
    path('my-profile/edit/', account_views.edit_profile, name='edit-profile'),
    path('view-profile/<int:user_id>/<username>/', account_views.view_profile, name='view-profile'),
]