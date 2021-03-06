# Generated by Django 3.2.2 on 2021-05-31 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('num_of_shares', models.PositiveIntegerField()),
                ('stock_price', models.DecimalField(decimal_places=2, help_text='Price of each unit share', max_digits=10)),
                ('stock_name', models.CharField(choices=[('TSLA', 'TESLA'), ('BMW', 'Bayerische Motoren Werke Aktiengesellschaft')], max_length=4)),
                ('transaction_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], max_length=4)),
                ('cash_impact', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('userprofile', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='trade.userprofile')),
            ],
        ),
    ]
