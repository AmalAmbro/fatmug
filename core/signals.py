from django.utils import timezone

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import F, Avg, ExpressionWrapper, fields, Sum, Q

from core.models import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def vendor_metrics(sender, instance, created, **kwargs):
    # handling vendor's on_time_delivery_rate
    if instance.status == 'completed' and instance.completed_date == None:
        # saving completed date
        instance.completed_date = timezone.now()
        instance.save()

        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        on_time_completed_pos = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed', completed_date__lte=F('delivery_date'),
        ).count()

        delivery_rate = 0
        if completed_pos > 0:
            delivery_rate = on_time_completed_pos / completed_pos

        vendor.on_time_delivery_rate = delivery_rate * 100
        vendor.save()

    # handling vendor's quality_rating_avg
    if instance.status == 'completed' and instance.quality_rating:
        quality_ratings = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed') \
        .exclude(quality_rating__isnull=True) \
        .aggregate(avg_rating=Avg('quality_rating'))

        if quality_ratings['avg_rating'] is not None:
            instance.vendor.quality_rating_avg = quality_ratings['avg_rating']
            instance.vendor.save()

    # handling vendor's average response time
    if instance.acknowledgment_date is not None:
        pos = PurchaseOrder.objects.filter(vendor=instance.vendor) \
        .filter(~Q(issue_date=None) and ~Q(acknowledgment_date=None))

        avg_responses = pos.annotate(
            response_time = ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())
        )

        if avg_responses:
            response_time = avg_responses.aggregate(sum_response_time=Avg('response_time'))
            total_seconds = response_time['sum_response_time'].total_seconds()
            # converted to minutes
            instance.vendor.average_response_time = (total_seconds or timezone.timedelta()) / 60
            instance.vendor.save()

    
@receiver(pre_save, sender=PurchaseOrder)
def handle_fulfillment_rate(sender, instance, **kwargs):
    if instance.pk is None:
        return

    old_instance = PurchaseOrder.objects.get(pk=instance.pk)

    if old_instance.status != instance.status:
        vendor = instance.vendor

        successful_fulfillments = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            quality_rating__isnull=False  # Assuming quality_rating is provided for successfully fulfilled POs
        ).count()

        if old_instance.status == 'completed':
            successful_fulfillments -= 1

        if instance.status == 'completed':
            successful_fulfillments += 1

        total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()

        fulfillment_rate = 0
        if total_pos > 0:
            fulfillment_rate = successful_fulfillments / total_pos

        vendor.fulfillment_rate = fulfillment_rate * 100
        vendor.save()

