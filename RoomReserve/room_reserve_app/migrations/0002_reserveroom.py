# Generated by Django 4.1.7 on 2023-02-25 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.CharField(max_length=255, null=True)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_reserve_app.room')),
            ],
            options={
                'unique_together': {('room_id', 'date')},
            },
        ),
    ]
