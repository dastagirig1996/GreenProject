from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views import View
from . models import Customer, Product, Cart, OrderPlaced, User
from .forms import CustomerRegistrationForm, CustomerProfileForm, FarmerRegistrationForm, ProductForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse


class ProductView(View):
  def get(self,request):
    totalitem=0
    Vegitable=Product.objects.filter(category='V')
    Fruits=Product.objects.filter(category='F')
    Fish=Product.objects.filter(category='Fi')
    if request.user.is_authenticated:
      totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'app/home.html',{'Vegitable':Vegitable,'Fruits':Fruits,'Fish':Fish,'totalitem':totalitem})

class ProductDetailView(View):
  def get(self,request,pk):
    product=Product.objects.get(pk=pk)
    item_already_in_cart=False
    if request.user.is_authenticated:
      item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
  user=request.user
  product_id=request.GET.get('prod-id')
  product=Product.objects.get(id=product_id)
  Cart(user=user,product=product).save()
  return redirect('/cart')

@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user=request.user
    cart=Cart.objects.filter(user=user)
    #print(cart)
    amount=0.0
    shipping_amount=40
    # total_amount=0.0
    cart_product= [p for p in Cart.objects.all() if p.user==user]
  if cart_product:
    for p in cart_product:
      tempamount=(p.quantiry * p.product.discountd_price)
      amount+=tempamount
      totalamount=amount+shipping_amount
    return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
  else:
    return render(request,'app/emptycart.html')
  
def plus_cart(request):
  if request.method=='GET':
    prod_id=request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantiry+=1
    c.save()
    amount=0.0
    shipping_amount=40
    cart_product= [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
        tempamount=(p.quantiry * p.product.discountd_price)
        amount+=tempamount

    data = {
      'quantiry':c.quantiry,
      'amount':amount,
      'totalamount':amount+shipping_amount
      }
    return JsonResponse(data)
 

def minus_cart(request):
  if request.method=='GET':
    prod_id=request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantiry-=1
    c.save()
    amount=0.0
    shipping_amount=40
    cart_product= [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
      tempamount=(p.quantiry * p.product.discountd_price)
      amount+=tempamount

    data = {
      'quantiry':c.quantiry,
      'amount':amount,
      'totalamount':amount+shipping_amount
      }
    return JsonResponse(data)
  
def remove_cart(request):
  if request.method=='GET':
   prod_id=request.GET['prod_id']
   c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.delete()
   amount=0.0
   shipping_amount=40
   cart_product= [p for p in Cart.objects.all() if p.user==request.user]
   for p in cart_product:
      tempamount=(p.quantiry * p.product.discountd_price)
      amount+=tempamount
      

   data = {
      'amount':amount,
      'totalamount':amount+shipping_amount
      }
   return JsonResponse(data)

@login_required
def buy_now(request):
  return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')
@login_required
def address(request):
  add=Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html',{'add':add})


@login_required
def orders(request):
  op=OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html',{'order_placed':op})


def fish(request):
  return render(request, 'app/Fish.html')


class CustomerRegistrationView(View):
  def get(self,request):
    form=CustomerRegistrationForm()
    return render(request,'app/customerregistration.html',{'form':form})
  def post(self,request):
    form=CustomerRegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request,'Registation Successfull')
      form.save()
    return render(request,'app/customerregistration.html',{'form':form})
  
@login_required
def checkout(request):
  user=request.user
  add=Customer.objects.filter(user=user)
  cart_items=Cart.objects.filter(user=user)
  amount=0.0
  shipping_amount=40
  totalamount=0.0
  shipping_amount=40
  cart_product= [p for p in Cart.objects.all() if p.user==request.user]
  if cart_product:
    for p in cart_product:
      tempamount=(p.quantiry * p.product.discountd_price)
      amount+=tempamount
    totalamount=amount+shipping_amount
  return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})


@login_required
def payment_done(request):
  user=request.user
  custid=request.GET.get('custid')
  customer=Customer.objects.get(id=custid)
  cart=Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,product=c.product,quantiry=c.quantiry).save()
    c.delete()
  return redirect('orders')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  def get(self,request):
    form=CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form})
 
  def post(self,request):
    form=CustomerProfileForm(request.POST)
    if form.is_valid():
      usr=request.user
      name=form.cleaned_data['name']
      locality=form.cleaned_data['locality']
      city=form.cleaned_data['city']
      state=form.cleaned_data['state']
      pincode=form.cleaned_data['pincode']
      reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,pincode=pincode)
      reg.save()
      messages.success(request,'Profile updated successfully')
    return render(request,'app/profile.html',{'form':form})


# Farmer module

#-------------------------------------------------------------------------------------------------------------------------------------
def farmerRegistration(request):
    if request.method == 'POST':
        frm = FarmerRegistrationForm(request.POST)
        if frm.is_valid():
            messages.info(request, 'info : Registered successfully')
            frm.save()
    else:
        frm = FarmerRegistrationForm()
    return render(request, 'farmer/signup.html', {'form': frm})


def farmerlogin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                passw = form.cleaned_data['password']
                user = authenticate(username=name, password=passw)
                # if user is not None:
                login(request, user)
                messages.success(request, ' logged in successfully')
                
                return redirect('farmerhome')
        else:
            form = AuthenticationForm()
        return render(request, 'farmer/login.html', {'fm': form})
    else:
        return redirect('farmerhome')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/flogin/')

def sellerHome(request):
  return render(request,'farmer/sellerHome.html')

def farmerhome(request):
    if not request.user.is_authenticated:
      form = AuthenticationForm()
      return render(request, 'farmer/login.html', {'fm': form})
    else:
      usr = request.user
      data = Product.objects.filter(user=usr)
      return render(request, 'farmer/home.html', {'data': data})

def addproducts(request):
    if not request.user.is_authenticated:
      form = AuthenticationForm()
      return render(request, 'farmer/login.html', {'fm': form})
    else:
      usr = request.user
      print(usr)
      if request.method == 'POST':
          form = ProductForm(request.POST, request.FILES)
          if form.is_valid():
              form.save()
              print('created')
              return redirect('farmerhome')
          else:
              print(form.errors)
              return render(request, 'farmer/addproducts.html', {"form": form.errors})
      else:
          form = ProductForm()
      return render(request, 'farmer/addproducts.html', {"form": form})
    
def orderdproducts(request):
    if not request.user.is_authenticated:
      form = AuthenticationForm()
      return render(request, 'farmer/login.html', {'fm': form})
    else:
        usr = request.user
        products = OrderPlaced.objects.filter(user = usr, status = 'Accepted')
        return render(request,'farmer/orders.html', {'products':products})