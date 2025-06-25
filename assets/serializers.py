from rest_framework import serializers
from .models import Asset, Notification, Violation

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'asset', 'asset_name', 'message', 'created_at', 'type']

class ViolationSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    class Meta:
        model = Violation
        fields = ['id', 'asset', 'asset_name', 'message', 'created_at', 'type'] 