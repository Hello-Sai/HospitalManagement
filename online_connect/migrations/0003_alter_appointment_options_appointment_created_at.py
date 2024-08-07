# Generated by Django 4.1 on 2024-07-10 06:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("online_connect", "0002_alter_appointment_patient"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="appointment",
            options={"ordering": ("date",)},
        ),
        migrations.AddField(
            model_name="appointment",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
