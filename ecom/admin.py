from django.contrib import admin

from ecom.models import Cart, OrderItem,Product,Order, CustomUser, Shipping_address

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','availability']
    list_filter=("name","price")
    prepopulated_fields={"slug":("name",)}

# class CartAdmin(admin.ModelAdmin):
#     list_display=['id']

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','status']

# class DeliveryAddressAdmin(admin.ModelAdmin):
#     list_display=['id','user','first_name','last_name','address','phone_number','city','postal_code']

class Shipping_addressAdmin(admin.ModelAdmin):
    list_display=['order','shipping_address']

admin.site.register(Product,ProductAdmin)
admin.site.register(CustomUser)
#admin.site.register(DeliveryAddress,DeliveryAddressAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Shipping_address,Shipping_addressAdmin)
admin.site.register(OrderItem)