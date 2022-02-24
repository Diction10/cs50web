# Generated by Django 3.2 on 2022-01-29 16:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_product_date_created'),
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='last_update_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='entry_date',
            field=models.DateField(),
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('transaction_date', models.DateField(default=datetime.datetime.now)),
                ('price', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amount_sold', to='sales.product')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.product')),
            ],
        ),
    ]