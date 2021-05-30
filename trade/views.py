from django.shortcuts import render
import yfinance as yf
from django.utils import timezone
from django.views import generic 
from trade import models as trade_models 
from django.views.generic import TemplateView
from django.urls import reverse_lazy 

from trade import models as trade_models


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

# def profile(request):
#     return render(request, 'trade/profile.html')


class ProfilePageView(TemplateView):
    template_name = 'profile.html'

# def transaction(request):
#     return render(request, 'trade/transaction.html')
class TransactionsView(TemplateView):
    template_name = 'transactions.html'