# Generated by Django 5.0.3 on 2024-07-02 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_sender', '0002_email_reply_ids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='reply_ids',
        ),
    ]
