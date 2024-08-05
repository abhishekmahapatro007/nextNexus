from django.contrib import admin
from .models import Product,Customer,Animal,Cart,Payment,OrderPlaced,Wishlist

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'discounted_price', 'category', 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'locality', 'city', 'state','zipcode']

@admin.register(Animal)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'location', 'animal_type', 'mobile_number','email_address','animal_health_description','injury_description']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin) :
    list_display = ['id', 'user','product','quantity']



@admin.register(Payment)
class PaymentModelAdmin (admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'customer', 'product', 'quantity', 'ordered_date','status','payment']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product']