from django.shortcuts import render
import yfinance as yf

from django.utils import timezone
from django.views import generic 
from trade import models as trade_models 
from django.views.generic import TemplateView
from django.urls import reverse_lazy 
from collections import namedtuple

from trade import models as trade_models

StockData = namedtuple("StockData", ["open", "high", "low", "close", "adj_close"])
MonthlyStockData = namedtuple("MonthlyStockData", ["date", "open", "high", "low", "close"])
StockQuantityPrice = namedtuple("StockQuantityPrice", ["name", "quantity", "price", "value"])

VALID_STOCK_NAMES = [stock[0] for stock in trade_models.Transaction.STOCK_NAMES]

def get_historical_data_html_div(ticker_name, days=90):
    now = timezone.now()
    days_ago = now - timezone.timedelta(days=days)

    try:
        stock = yf.Ticker(ticker_name)
        df = stock.history(start=days_ago.strftime("%Y-%m-%d"), end=now.strftime("%Y-%m-%d"))
    except Exception as e:
        print(repr(e))
        return "Could not load yahoo financal data at this time"

    df = df.reset_index()

    fig = plotly_express.line(df, x="Date", y="Open", title=f"90 days stock price for {ticker_name}")

    html_div = plotly.offline.plot(fig, output_type="div")
    return html_div
    
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


class ProfilePageView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock_name = self.request.GET.get("stock_name", VALID_STOCK_NAMES[0])
        context["stock_name"]  = stock_name

        stock_share_quantity_value = []

        stock_data = get_current_stock_data(stock_name)
        context["stock_data"] = stock_data

        historical_data_div = get_historical_data_html_div(stock_name)
        context["historical_data_div"] = historical_data_div

        context["valid_stock_names"] = VALID_STOCK_NAMES

        transaction_form = TransactionForm()
        context["transaction_form"] = transaction_form

        current_shares = self.request.user.userprofile.get_share_count(stock_name)
        context["current_shares"] = current_shares
        current_value = round(current_shares * float(stock_data.open), 2)
        context["current_value"] = current_value

        stock_share_quantity_value.append(
            StockQuantityPrice(name=stock_name, quantity=current_shares, price=stock_data.open, value=current_value)
        )
    #to create total value for user profile value and stock value
        rest_stock_names = [stock for stock in VALID_STOCK_NAMES if stock != stock_name]
        rest_current_value = 0
        for _stock_name in rest_stock_names:
            _stock_data = get_current_stock_data(_stock_name)
            _stock_open = _stock_data.open
            _current_shares = self.request.user.userprofile.get_share_count(_stock_name)
            _current_value = round(_current_shares * float(_stock_open), 2)
            rest_current_value += _current_value

            stock_share_quantity_value.append(
                StockQuantityPrice(name=_stock_name, quantity=_current_shares, price=_stock_open, value=_current_value)
            )

        context["stock_share_quantity_value"] = stock_share_quantity_value
    
        total_portfolio_value = round(current_value + rest_current_value + float(self.request.user.userprofile.balance), 2)

        context["total_portfolio_value"] = total_portfolio_value

        monthly_stock_data = get_monthly_stock_data(stock_name)
        context["monthly_stock_data"] = monthly_stock_data

        return context

    def post(self, *args, **kwargs):

        current_user = self.request.user
        user_profile = current_user.userprofile

        form = TransactionForm(self.request.POST, user=current_user)
        if not form.is_valid():
            context = self.get_context_data()
            context["transaction_form"] = form

            return render(self.request, self.template_name, context)  

        transaction = form.save(commit=False)

        cleaned_data = form.cleaned_data 

        num_of_shares = cleaned_data["num_of_shares"]         
        stock_price = cleaned_data["stock_price"]
        transaction_type = cleaned_data["transaction_type"]

        total_price = stock_price * num_of_shares
        transaction.cash_impact = total_price

        if transaction_type == "BUY":
            user_profile.balance -= total_price
        else:
            user_profile.balance += total_price

        user_profile.save()

        transaction.userprofile = user_profile
        transaction.save()

        context = self.get_context_data()
        return render(self.request, self.template_name, context)


# def transaction(request):
#     return render(request, 'trade/transaction.html')
class TransactionsView(TemplateView):
    template_name = 'transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        current_user = self.request.user
        all_transactions = trade_models.Transaction.objects.filter(userprofile=current_user.userprofile).order_by("-pk")
        context["transactions"] = all_transactions

        hourly_graph_divs = [get_hourly_div(stock_name) for stock_name in VALID_STOCK_NAMES]
        context["hourly_graph_divs"] = hourly_graph_divs
        return context