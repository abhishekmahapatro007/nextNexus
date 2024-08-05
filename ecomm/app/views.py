from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from django.views import View
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from .forms import CustomerRegistrationForm , CustomerProfileForm,StrayAnimalRescueForm
from django.db.models import Count
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import razorpay

def home(request):
    totalitem=0
    if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())
def ecommerce(request):
    return render(request,"app/ecommerce.html",locals())
def about(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())
def contact(request):
     totalitem=0
     if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
     return render(request,"app/contact.html",locals())
class StrayAnimalRescue(View):
    def get(self,request):
        form=StrayAnimalRescueForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/strayanimalrescue.html',locals())
    def post(self,request):
        form=StrayAnimalRescueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations ! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/strayanimalrescue.html',locals())


class CategoryView(View):
    def get(self,request,val):
         totalitem=0
         if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
         product=Product.objects.filter(category=val)
         title = Product.objects.filter(category = val).values('title')
         return render(request,"app/category.html",locals())
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,"app/category.html",locals())
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user) )
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render (request, "app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations ! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/customerregistration.html',locals())


class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg= Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/profile.html',locals())

def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render (request, 'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add= Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render (request, 'app/updateAddress.html',locals())

    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations ! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount=amount+ value
    totalamount=amount+40
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())

class Checkout(View):
    def get(self, request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 40  
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        order_id = payment_response['id']
        order_status = payment_response['status']

        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()   
        context = {
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount,
            'razoramount': razoramount,
            'order_id': order_id
        }
        return render(request, 'app/checkout.html', context)
    
def payment_done(request):
    order_id = request.POST.get('order_id')
    payment_id = request.POST.get('payment_id')
    signature = request.POST.get('signature')  # Add this to verify signature
    cust_id = request.POST.get('custid')
    user = request.user

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    try:
        # Verify the payment signature
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        customer = Customer.objects.get(id=cust_id)
        payment = Payment.objects.get(razorpay_order_id=order_id)
        payment.paid = True
        payment.razorpay_payment_id = payment_id
        payment.save()

        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
            c.delete()

        return redirect("orders")
    except razorpay.errors.SignatureVerificationError as e:
        return HttpResponse("Payment verification failed. Please try again.")
    
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html  ',locals())

def plus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discounted_price
            amount=amount+ value
        totalamount=amount+40
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discounted_price
            amount=amount+ value
        totalamount=amount+40
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discounted_price
            amount=amount+ value
        totalamount=amount+40
        #print(prod_id)
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod-id']
        product=product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user,product=product).save()
        data={
            'message': 'Wishlist added successfully',
        }
        return JsonResponse(data)
def mius_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod-id']
        product=product.objects.get(id=prod_id)
        user=request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message': 'Wishlist added successfully',
        }
        return JsonResponse(data)
