
from django.urls import path
from .views import edit_profile, generate_cv_pdf, change_password, moderator_request_view
urlpatterns = [
     path('profile_edit/', edit_profile, name="profile_edit"),
     path('change-password',change_password, name="change_password"),
     path('cv-form/', generate_cv_pdf, name='form_pdf'),
     path('moderator-request/', moderator_request_view, name='moderator_request'),

]


