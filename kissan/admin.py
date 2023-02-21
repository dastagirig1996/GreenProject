from django.contrib import admin
from . models import Customer,Product,Cart,OrderPlaced

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','pincode','state']

@admin.register(Product)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discountd_price','description','category','Product_Added_date','product_image']

@admin.register(Cart)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantiry']

@admin.register(OrderPlaced)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantiry','order_date','status']