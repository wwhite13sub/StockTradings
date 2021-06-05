from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone


import plotly 
from plotly import express as plotly_express

from collections import namedtuple
from trade import models as trade_models

from .forms import TransactionsForm
import pandas as pd
import numpy as np
import csv
import yfinance as yf

                                    #date_time
StockData = namedtuple("StockData", ["open", "high", "low", "close", "adj_close"])
MonthlyStockData = namedtuple("MonthlyStockData", ["date", "open", "high", "low", "close"])
StockQuantityPrice = namedtuple("StockQuantityPrice", ["name", "quantity", "price", "value"])

VALID_STOCK_NAMES = [stock[0] for stock in trade_models.Transactions.STOCK_NAMES]

def get_historical_data_html_div(ticker_name, days=90):
    now = timezone.now()
    days_ago = now - timezone.timedelta(days=days)

    try:
        stock = yf.Ticker(ticker_name)
        df = stock.history(start=days_ago.strftime("%Y-%m-%d"), end=now.strftime("%Y-%m-%d"))
    except Exception as e:
        print(repr(e))
        return "Could not load yahoo financial data at this time"

    df = df.reset_index()

    fig = plotly_express.line(df, x="Date", y="Close", title=f"90 days stock price for {ticker_name}")

    html_div = plotly.offline.plot(fig, output_type="div")
    return html_div

def get_monthly_stock_data(ticker_name):

    today = timezone.now()
    first_day_of_current_month = today.replace(day=1)

    current_month = first_day_of_current_month.month

    if current_month == 1:
        final_month = 11
    elif current_month == 2:
        final_month = 12
    else:
        final_month = current_month - 2

    first_day_of_third_month = first_day_of_current_month.replace(month=final_month)

    df = yf.download(
        ticker_name, 
        start=first_day_of_third_month.strftime("%Y-%m-%d"), 
        end=(first_day_of_current_month + timezone.timedelta(days=1)).strftime("%Y-%m-%d"),
        period="3mo",
        interval="1mo",
    )
    df = df.reset_index()
    df = df.dropna() #pandas

    final_data = []

    for index, row in df.iterrows():
        open = round(float(row.Open), 2)
        high = round(float(row.High),2)
        low = round(float(row.Low),2)
        close = round(float(row.Close),2)
        
        date = row.Date.strftime("%Y-%m-%d")

        stock_data = MonthlyStockData(date=date, open=open, high=high, low=low, close=close, )

        final_data.append(stock_data)

    return final_data

    # graph side by side 
def get_hourly_stock_html_div(ticker_names):
    try:
        df = yf.download(ticker_names, period="1d", interval="60m")
    except Exception as e:
        print(repr(e))
        return "Could not load yahoo financial data "
    open_df = df.Open
    open_df = open_df.reset_index()
    #[0]date/time index slice [1: take every other values]
    # fig = plotly_express.line(open_df, x=open_df.columns[0], y=open_df.columns[1:], title="Hourly Stock Price")
    fig = plotly_express.line(open_df, x=open_df.columns[0], y=open_df.columns[2], title="Hourly Stock Price")
     
    html_div = plotly.offline.plot(fig, output_type="div") #html div means (html tag )
    return html_div

def get_hourly_div(ticker_name):
    try:
        df= yf.download(ticker_name, period="1d", interval="60m")
        # raise Exception
    except Exception as e:
        print(repr(e))
        return "Could not retrieve data at this moment"
    #open_df = df.Open
    #import pdb; pdb.set_trace()
    df = df.reset_index()
    fig = plotly_express.line(df, x=df.columns[0], y=df.columns[1], title=f"Hourly Stock {ticker_name}")

    div = plotly.offline.plot(fig, output_type="div") 
    return div


    
def get_current_stock_data(ticker_name):
    df = yf.download(ticker_name, timezone.now().strftime("%Y-%m-%d"), period="1m", interval="1m")

    while df.empty:
        df = yf.download(ticker_name, (timezone.now() - timezone.timedelta(days=1)).strftime("%Y-%m-%d"), period="1m", interval="1m")

    df = df.tail(1)
    df = df.reset_index()
    #import pdb; pdb.set_trace()

    # date_time = (df["Date Time"])
    open = round(float(df.Open), 2)
    high = round(float(df.High),2)
    low = round(float(df.Low),2)
    close = round(float(df.Close),2)
    adj_close = round(float(df["Adj Close"]),2)

        #date_time
    stock_data = StockData( open=open, high=high, low=low, close=close, adj_close=adj_close)

    return stock_data
    



# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


class ResetPageView(LoginRequiredMixin, TemplateView):
    template_name = 'reset.html'

    def post(self, *args, **kwargs):

        userprofile = self.request.user.userprofile

        userprofile.transactions.all().delete()

        userprofile.reset_account()

        return redirect("transactions")


class PortfolioPageView(LoginRequiredMixin, TemplateView):
    template_name = 'portfolio.html'

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

        transactions_form = TransactionsForm()
        context["transactions_form"] = transactions_form

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

        form = TransactionsForm(self.request.POST, user=current_user)
        if not form.is_valid():
            context = self.get_context_data()
            context["transactions_form"] = form

            return render(self.request, self.template_name, context)  

        transactions = form.save(commit=False)

        cleaned_data = form.cleaned_data 

        num_of_shares = cleaned_data["num_of_shares"]         
        stock_price = cleaned_data["stock_price"]
        transaction_type = cleaned_data["transaction_type"]

        total_price = stock_price * num_of_shares
        transactions.cash_impact = total_price

        if transaction_type == "BUY":
            user_profile.balance -= total_price
        else:
            user_profile.balance += total_price

        user_profile.save()

        transactions.userprofile = user_profile
        transactions.save()

        context = self.get_context_data()
        return render(self.request, self.template_name, context)

    


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        response = super().form_valid(form)
        profile = trade_models.UserProfile(user=self.object)
        profile.reset_account()
        profile.save()
        return response





class TransactionsView(LoginRequiredMixin, generic.TemplateView):

    
    template_name = "transactions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        current_user = self.request.user
        all_transactions = trade_models.Transactions.objects.filter(userprofile=current_user.userprofile).order_by("-pk")
        context["transactions"] = all_transactions

        hourly_graph_divs = [get_hourly_div(stock_name) for stock_name in VALID_STOCK_NAMES]
        context["hourly_graph_divs"] = hourly_graph_divs
        return context

    
        