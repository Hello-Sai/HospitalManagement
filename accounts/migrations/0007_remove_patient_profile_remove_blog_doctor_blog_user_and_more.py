# Generated by Django 4.1 on 2024-07-06 10:28

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_blog_is_drafted"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patient",
            name="profile",
        ),
        migrations.RemoveField(
            model_name="blog",
            name="doctor",
        ),
        migrations.AddField(
            model_name="blog",
            name="user",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blogs",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="is_doctor",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="blog",
            name="category",
            field=models.CharField(
                choices=[
                    ("hypocrispy", "Covid19"),
                    ("phobia", "Immunization"),
                    ("mental_health", "Mental Health"),
                    ("heart_disease", "Heart Disease"),
                ],
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="blog",
            name="image",
            field=models.ImageField(upload_to=accounts.models.user_path),
        ),
        migrations.DeleteModel(
            name="Doctor",
        ),
        migrations.DeleteModel(
            name="Patient",
        ),
    ]
