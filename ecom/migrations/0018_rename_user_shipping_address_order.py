# Generated by Django 3.2.9 on 2021-11-23 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0017_auto_20211123_0429'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipping_address',
            old_name='user',
            new_name='order',
        ),
    ]
