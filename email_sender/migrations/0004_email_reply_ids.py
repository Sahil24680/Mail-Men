# Generated by Django 5.0.3 on 2024-07-03 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_sender', '0003_remove_email_reply_ids'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='reply_ids',
            field=models.ManyToManyField(blank=True, related_name='replies', to='email_sender.email'),
        ),
    ]
