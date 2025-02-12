from django.urls import path
from core.views import submit_form

urlpatterns = [
    path('', submit_form, name='submit-form'),
    ]