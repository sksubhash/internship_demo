# Generated by Django 3.1 on 2020-08-11 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nurseryapp', '0011_tblorder_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblorder',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='nurseryapp.tblplants'),
        ),
    ]
