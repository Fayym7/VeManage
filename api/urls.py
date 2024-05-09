from django.urls import path
from . import views


urlpatterns = [
    path('vendors/', views.VendorMixinView.as_view(), name='vendor_list'),
    path('vendors/<int:vendor_code>/', views.VendorMixinView.as_view(), name='vendors_operate'),
    path('vendors/<int:vendor_code>/performance/', views.VendorMixinView.as_view(), name='vendor_performance'),
    path('purchase_orders/', views.PurchaseOrderMixinView.as_view(), name='purchase_orders'),
    path('purchase_orders/<int:po_number>/', views.PurchaseOrderMixinView.as_view(), name='purchase_orders_operate'),
    path('purchase_orders/<int:po_number>/acknowledgment', views.PurchaseOrderMixinView.as_view(), name='purchase_order_acknowledge')
    ]

