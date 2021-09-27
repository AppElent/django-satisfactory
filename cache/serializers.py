from rest_framework import serializers

class CacheSerializer(serializers.Serializer):
    """  Cache """
    key = serializers.CharField()
    value = serializers.CharField()
    timeout = serializers.IntegerField(required=False)
