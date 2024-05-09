from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

# class HistoricalPerformanceSerializer(serializers.ModelSerializer):
#     vendor = VendorSerializer(data= validated_data.get("vendor"))
#     class Meta:
#         model = HistoricalPerformance
#         fields = (
#             'vendor', 'date', 'on_time_delivery_rate',
#     'quality_rating_avg',
#     'average_response_time' ,
#     'fulfillment_rate'
#         )
    
    # def create(self, validated_data):
    #     vendor_data = validated_data.get("vendor")
    #     performance = HistoricalPerformance.objects.create(**validated_data)
    #     Vendor.objects.create(artist=artist, vendor=vendor_data)
    #     return performance
    
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()  # Use VendorSerializer for vendor field

    class Meta:
        model = HistoricalPerformance
        fields = (
            'vendor', 'date', 'on_time_delivery_rate',
            'quality_rating_avg', 'average_response_time', 'fulfillment_rate'
        )
    
    def create(self, validated_data):
        vendor_data = validated_data.pop("vendor")
        # Assuming you are passing vendor_data as a dictionary
        vendor_serializer = VendorSerializer(data=vendor_data)
        if vendor_serializer.is_valid():
            vendor_instance = vendor_serializer.save()
            historical_performance = HistoricalPerformance.objects.create(vendor=vendor_instance, **validated_data)
            return historical_performance
        else:
            # Handle serializer validation errors here
            raise serializers.ValidationError("Vendor data is invalid.")
# class HistoricalPerformanceSerializer(serializers.ModelSerializer):
#     # Instead of using VendorSerializer directly, specify vendor_code field
#     vendor_code = serializers.CharField(source='vendor.vendor_code', read_only=True)

#     class Meta:
#         model = HistoricalPerformance
#         fields = (
#             'vendor_code',  # Use vendor_code instead of vendor
#             'date', 'on_time_delivery_rate',
#             'quality_rating_avg',
#             'average_response_time',
#             'fulfillment_rate'
#         )

#     def create(self, validated_data):
#         vendor_data = validated_data.pop("vendor")
#         # Create HistoricalPerformance instance
#         performance = HistoricalPerformance.objects.create(**validated_data)
#         # Assuming vendor_data is a vendor_code, fetch Vendor instance using vendor_code
#         vendor_instance = Vendor.objects.get(vendor_code=vendor_data)
#         performance.vendor = vendor_instance  # Assign vendor to HistoricalPerformance
#         performance.save()
#         return performance