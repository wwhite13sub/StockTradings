from django.urls import path
from .views import (HomePageView, ResetPageView, PortfolioPageView, SignUpView,TransactionsView)


urlpatterns = [
path('portfolio/', PortfolioPageView.as_view(), name='portfolio'),
path('reset/', ResetPageView.as_view(), name='reset'),
path('', HomePageView.as_view(), name='home'),
path('signup/', SignUpView.as_view(), name='signup'),
path("transactions/", TransactionsView.as_view(), name="transactions"),
]