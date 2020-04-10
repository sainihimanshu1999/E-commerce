# Generated by Django 3.0.2 on 2020-04-10 17:30

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_order_billing_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='countries',
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='country',
            field=django_countries.fields.CountryField(default='India', max_length=2),
            preserve_default=False,
        ),
    ]
