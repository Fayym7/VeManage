from django.shortcuts import render
from rest_framework import generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer 
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class VendorMixinView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'vendor_code'
    # authentication_classes = []
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get("vendor_code")
        if pk is not None:
            if str(pk) not in list(Vendor.objects.values_list('vendor_code', flat=True)):
        
                return Response({'Detail':'No Vendor based on the Code found'}, status=404)
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.data['vendor_code']

        if str(pk) in list(Vendor.objects.values_list('vendor_code', flat=True)):
       
            return Response({'Detail':'Vendor ID is already in use, Try a different one'}, status=409)
        return self.create(request, *args, **kwargs)

    def delete(self,request, *args, **kwargs):
        pk = kwargs.get("vendor_code")
   
        if str(pk) not in list(Vendor.objects.values_list('vendor_code', flat=True)):
            return Response({'Detail':'No Vendor based on the Code found'}, status=404)
        return self.destroy(request, *args, **kwargs)
    
    def put(self,request, *args , **kwargs):
        pk = int(kwargs.get('vendor_code'))
        if str(pk) not in list(Vendor.objects.values_list('vendor_code', flat=True)):

            return Response({'Detail':'No Vendor based on the Code found'}, status=404)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
  
    def perform_create(self, serializer):
        vendor_instance = serializer.save()
        HistoricalPerformance.objects.create(vendor=vendor_instance)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        pk = str(kwargs.get('vendor_code'))
        mutable_data = request.data.copy()
        inst = Vendor.objects.get(pk= pk)
        for key, value in mutable_data.items():
            if not value:
                mutable_data[key] = getattr(inst, key)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=mutable_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
 


class PurchaseOrderMixinView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_number'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get('po_number')
        if pk is not None:
            if int(pk) not in list(PurchaseOrder.objects.values_list('po_number', flat=True)):
                return Response({'Detail':'No Purchase Order Found'}, status=404)
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
         
    def post(self, request, *args, **kwargs):
        if 'acknowledgment' in self.request.path:
            pk = int(kwargs.get("po_number"))
            if pk not in list(PurchaseOrder.objects.values_list('po_number', flat=True)):
                return Response({'Detail':'No Purchase Order Found'}, status=404)
            po_number = kwargs.get("po_number")
            instance = PurchaseOrder.objects.get(po_number= po_number)
            current_datetime = datetime.utcnow()
            formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            instance.acknowledgment_date = formatted_datetime
            instance.save()
            return Response({'Detail':f'Acknowlegemnt date has been set at {formatted_datetime}'}, status = 200)
        return self.create(request, *args, **kwargs)

    def delete(self,request, *args , **kwargs):
        pk = kwargs.get('po_number')
     
        if int(pk) not in list(PurchaseOrder.objects.values_list('po_number', flat=True)):
           
            return Response({'Detail':'No Purchase Order Found'}, status=404)
        return self.destroy(request, *args, **kwargs)
    
    def put(self,request, *args , **kwargs):
        pk = kwargs.get('po_number')
       
        if int(pk) not in list(PurchaseOrder.objects.values_list('po_number', flat=True)):
          
            return Response({'Detail':'No Purchase Order Found'}, status=404)
        kwargs['partial']= True
        return self.update(request, *args, **kwargs)

    

    def create(self, request, *args, **kwargs):
        vendor_name = request.data.get('vendor', None)
    
        vendor = Vendor.objects.filter(name= vendor_name).first()
      
        if not vendor:
            return Response({'Detail':'Vendor Not Found, Enter a valid Vendor Name'}, status=status.HTTP_404_NOT_FOUND)
        mutable_data = request.data.copy()
        mutable_data['vendor'] = vendor.pk
     
        serializer = self.get_serializer(data=mutable_data)
      
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            errors = e.detail
            print(errors)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
   
        vendor = Vendor.objects.filter(name= request.data['vendor']).first()
        if not vendor:
            return Response({'Detail':'Vendor Not Found, Enter a valid Vendor Name'}, status=status.HTTP_404_NOT_FOUND)
        pk = int(kwargs.get('po_number'))
        mutable_data = request.data.copy()
     
        inst = PurchaseOrder.objects.get(pk= pk)
 
        mutable_data['vendor'] = vendor.pk
 
        for key, value in mutable_data.items():
            if not value:
                mutable_data[key] = getattr(inst, key)
     
        instance = self.get_object()
       
        serializer = self.get_serializer(instance, data=mutable_data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            errors = e.detail
            print(errors)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()) 
        # Group purchase orders based on vendor's name
        grouped_purchase_orders = {}
        for purchase_order in queryset:
            vendor_name = purchase_order.vendor.name
            if vendor_name not in grouped_purchase_orders:
                grouped_purchase_orders[vendor_name] = []
            grouped_purchase_orders[vendor_name].append(self.get_serializer(purchase_order).data)
        return Response(grouped_purchase_orders)

