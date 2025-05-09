# Generated by Django 5.0.3 on 2024-07-07 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_sender', '0005_email_archived_email_starred'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='archived_inbox',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inbox',
            name='starred_inbox',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
