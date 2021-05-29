from django.shortcuts import render
import yfinance as yf
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'trade/base.html')

def profile(request):
    return render(request, 'trade/profile.html')

def transaction(request):
    return render(request, 'trade/transaction.html')