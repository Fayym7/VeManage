from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(primary_key=True, max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.IntegerField(primary_key=True, unique=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    items = models.CharField(max_length= 1000, null=False, blank=False)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=status_choices, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.po_number} - {self.vendor.name}"

class HistoricalPerformance(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name='performance')
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.vendor} - {self.date}"
     
    