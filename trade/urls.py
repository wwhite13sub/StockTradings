from django.urls import path
from .views import (ProfilePageView, HomePageView, TransactionsView)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('transactions/', TransactionsView.as_view(), name='transactions')

]