from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'trade/home.html')

def transaction(request):
    return render(request, 'trade/transaction.html')