# Generated by Django 5.0.4 on 2024-07-06 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_blog_content_alter_blog_summary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(choices=[('cancer', 'cancer'), ('diarrhoea', 'Diarrhoea'), ('typhoid', 'Typhoid'), ('malaria', 'Malaria')], max_length=15),
        ),
    ]
