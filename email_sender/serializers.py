from rest_framework import serializers
from .models import Email,Inbox
from django.utils.timesince import timesince



class Emailserializer(serializers.ModelSerializer):
    sender = serializers.EmailField(source='sender.email', read_only=True)
    timestamp = serializers.SerializerMethodField()
    username = serializers.CharField(source='sender.username', read_only=True)  # Username field
    reply_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Email
        fields = ['id','sender','To','username','subject','body','timestamp','is_read','reply_ids']


    def get_timestamp(self, obj):
        formatted_date = obj.timestamp.strftime("%b %d, %Y, %I:%M %p")
        time_ago = timesince(obj.timestamp) + " ago"
        return f"{formatted_date} ({time_ago})"


class InboxSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Inbox
        fields = ['num_inbox','archived_inbox','starred_inbox']