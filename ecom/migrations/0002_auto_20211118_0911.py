# Generated by Django 3.2.8 on 2021-11-18 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='cart',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecom.order'),
        ),
    ]
