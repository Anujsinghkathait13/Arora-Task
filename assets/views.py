from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Asset, Notification, Violation
from .serializers import AssetSerializer, NotificationSerializer, ViolationSerializer
from datetime import timedelta


# Create your views here.

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer

class ViolationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Violation.objects.all().order_by('-created_at')
    serializer_class = ViolationSerializer

def home_view(request):
    return JsonResponse({
        "message": "Welcome to the Asset Management API",
        "endpoints": ["/api/assets/", "/api/run-checks/", "/swagger/"]
    })
    
@api_view(['POST'])
def run_checks(request):
    now = timezone.now()
    soon = now + timedelta(minutes=15)
    notifications_created = 0
    violations_created = 0

    # Reminders for service_time and expiration_time within 15 minutes
    assets = Asset.objects.filter(
        Q(service_time__gt=now, service_time__lte=soon, serviced=False) |
        Q(expiration_time__gt=now, expiration_time__lte=soon)
    )
    for asset in assets:
        if asset.service_time > now and asset.service_time <= soon and not asset.serviced:
            if not Notification.objects.filter(asset=asset, type='service', message__icontains='Service due').exists():
                Notification.objects.create(
                    asset=asset,
                    message=f'Service due for asset {asset.name} at {asset.service_time}',
                    type='service'
                )
                notifications_created += 1
        if asset.expiration_time > now and asset.expiration_time <= soon:
            if not Notification.objects.filter(asset=asset, type='expiration', message__icontains='Expiration due').exists():
                Notification.objects.create(
                    asset=asset,
                    message=f'Expiration due for asset {asset.name} at {asset.expiration_time}',
                    type='expiration'
                )
                notifications_created += 1

    # Violations for overdue service or expired assets
    overdue_assets = Asset.objects.filter(
        Q(service_time__lt=now, serviced=False) |
        Q(expiration_time__lt=now)
    )
    for asset in overdue_assets:
        if asset.service_time < now and not asset.serviced:
            if not Violation.objects.filter(asset=asset, type='service', message__icontains='Service overdue').exists():
                Violation.objects.create(
                    asset=asset,
                    message=f'Service overdue for asset {asset.name} since {asset.service_time}',
                    type='service'
                )
                violations_created += 1
        if asset.expiration_time < now:
            if not Violation.objects.filter(asset=asset, type='expiration', message__icontains='Asset expired').exists():
                Violation.objects.create(
                    asset=asset,
                    message=f'Asset {asset.name} expired at {asset.expiration_time}',
                    type='expiration'
                )
                violations_created += 1

    return Response({
        'notifications_created': notifications_created,
        'violations_created': violations_created
    }, status=status.HTTP_200_OK)
