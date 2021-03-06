# Generated by Django 3.1 on 2020-08-11 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nurseryapp', '0006_auto_20200811_0038'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('quantity', models.SmallIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nurseryapp.tblplants')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tblorder',
            },
        ),
    ]
