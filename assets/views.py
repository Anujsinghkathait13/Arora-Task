from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from .models import Asset, Notification, Violation
from .serializers import AssetSerializer, NotificationSerializer, ViolationSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

@api_view(['GET'])
def run_checks(request):
    now = timezone.now()
    fifteen_minutes = timedelta(minutes=15)

    assets = Asset.objects.all()

    for asset in assets:
        # Reminder for service_time
        if 0 <= (asset.service_time - now).total_seconds() <= 900:
            Notification.objects.get_or_create(
                asset=asset,
                message=f"Service due for asset: {asset.name}"
            )
        # Reminder for expiration_time
        if 0 <= (asset.expiration_time - now).total_seconds() <= 900:
            Notification.objects.get_or_create(
                asset=asset,
                message=f"Asset {asset.name} is about to expire."
            )

        # Check for violations
        if now > asset.service_time and not asset.is_serviced:
            Violation.objects.get_or_create(
                asset=asset,
                reason=f"Asset {asset.name} missed service time."
            )
        if now > asset.expiration_time:
            Violation.objects.get_or_create(
                asset=asset,
                reason=f"Asset {asset.name} is expired."
            )

    return Response({"message": "Checks completed."})


# Create your views here.
