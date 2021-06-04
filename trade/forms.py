from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Transactions


class TransactionsForm(ModelForm):

    # user = forms.
    # TransactionForm(user, 100, 10,  foo=10, bar=100)
    def __init__(self, *args, user=None, **kwargs):
        # args = (100, 10)
        # kwargs = {"foo": 10, "bar": 100}

        super().__init__(*args, **kwargs)
        self.current_user = user

    def clean(self):

        cleaned_data = super().clean()

        # Num of shares
        num_of_shares = cleaned_data["num_of_shares"]
        if num_of_shares < 1:
            raise ValidationError({
                "num_of_shares": ["Num of shares must be 1 or more"]
            })
        # import pdb; pdb.set_trace()
        transaction_type = cleaned_data["transaction_type"]
        stock_name = cleaned_data["stock_name"]
        stock_price = cleaned_data["stock_price"]
        user_profile = self.current_user.userprofile
        if transaction_type == "SELL":

            current_shares_count = user_profile.get_share_count(
                cleaned_data["stock_name"])
            if current_shares_count < int(cleaned_data["num_of_shares"]):
                raise ValidationError({
                    "num_of_shares": [
                        f"You don't have {num_of_shares} shares for {stock_name}, "
                        f"you have {current_shares_count}."
                    ]
                })
        else:
            total_share_price = float(stock_price) * int(num_of_shares)
            if total_share_price > user_profile.balance:
                raise ValidationError({
                    "num_of_shares": [
                        f"You don't have enough balance to buy these shares"
                    ]
                })

        return cleaned_data

    class Meta:
        model = Transactions
        exclude = ["date_time", "userprofile", "cash_impact"] # table to not include values of