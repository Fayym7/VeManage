from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from datetime import date



def calculate_average(values):
    total = sum(values)
    count = len(values)
    return total / count if count != 0 else 0.0

@receiver(post_save, sender=PurchaseOrder) 
def ontime_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        rate = vendor.performance.on_time_delivery_rate
        temp = rate*(completed_orders-1)
        if instance.delivery_date <= date.today():
            temp+=1
        if completed_orders != 0:
            on_time_delivery_rate = temp / completed_orders
            vendor.performance.on_time_delivery_rate = on_time_delivery_rate
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.performance.save()
            vendor.save()
        
  
@receiver(post_save, sender=PurchaseOrder) 
def quality_rating_average(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        quality_ratings = completed_orders.values_list('quality_rating', flat=True)
        if quality_ratings:
            quality_rating_avg = calculate_average(quality_ratings)
            vendor.performance.quality_rating_avg = quality_rating_avg
            vendor.quality_rating_avg = quality_rating_avg
            vendor.performance.save()
            vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def average_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = [(order.acknowledgment_date - order.issue_date).total_seconds() / 3600
                          for order in completed_orders]
        if response_times:
            avg_response_time = calculate_average(response_times)
            vendor.performance.average_response_time = avg_response_time
            vendor.average_response_time = avg_response_time
            vendor.performance.save()
            vendor.save()


@receiver(pre_save, sender=PurchaseOrder)
def fulfilment_rate(sender, instance, **kwargs):
    if instance.pk and instance.status =='completed':  # If the instance is being updated and 
        old_instance = PurchaseOrder.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            vendor = instance.vendor
            total_orders = PurchaseOrder.objects.filter(vendor=vendor)
            completed_orders = total_orders.filter(status='completed').count()+1
            total_orders = total_orders.count()
            if total_orders != 0:
                fulfillment_rate = completed_orders/total_orders
                vendor.performance.fulfillment_rate = fulfillment_rate
                vendor.fulfillment_rate = fulfillment_rate
                vendor.performance.save()
                vendor.save()
