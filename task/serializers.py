from rest_framework import serializers


class SendDateTimeSerializer(serializers.Serializer):

    datetime = serializers.DateTimeField(default_timezone='Asia/Yerevan')