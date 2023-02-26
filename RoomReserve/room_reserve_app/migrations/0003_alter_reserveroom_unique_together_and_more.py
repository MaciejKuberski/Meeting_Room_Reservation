# Generated by Django 4.1.7 on 2023-02-26 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve_app', '0002_reserveroom'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reserveroom',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='reserveroom',
            constraint=models.UniqueConstraint(fields=('room_id', 'date'), name='unique_booking'),
        ),
    ]
