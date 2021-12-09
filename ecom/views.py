
from django.contrib.messages.api import success
from django.http.response import JsonResponse
from django.views import View
from django.views.generic import ListView,CreateView
from ecom.models import Cart, Order, OrderItem, Product,CartItem
from django.db.models import Q
from django.shortcuts import  render, redirect
from .forms import  NewUserForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView 
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from copy import deepcopy
from django.forms.models import model_to_dict
# Create your views here.


class StartingPageView(ListView):
    template_name="ecom/home_page.html"
    model=Product
    context_object_name="product"


class SearchView(View):
	def get(self,request):
		query=self.request.GET.get('query')
		if query:
			product=Product.objects.filter(name__icontains=query)

			return render(request,"ecom/search-result.html",{'products':product})
		else:
			
			return render(request,"ecom/search-result.html")


class FilterView(ListView):
	template_name="ecom/filter.html"
	model=Product
	context_object_name="products"

	def get_queryset(self):
		data= self.kwargs['data']
		return self.model.objects.all().order_by(data)
	


#product detail view
class SignleItemView(View):
	def get(self,request,slug):
		product=Product.objects.get(slug=slug)
		item_already_in_cart=False
		if request.user.is_authenticated:
			item_already_in_cart=CartItem.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
		context={
			'product':product,
			'item_already_in_cart':item_already_in_cart
		}
		return render(request,'ecom/item-detail.html',context)
		

class UserSignUpView(CreateView):
	form_class=NewUserForm
	success_url=reverse_lazy('login')
	template_name="ecom/register.html"


class UserLoginView(LoginView):
	template_name="ecom/login.html"


class Logout(View):
	def get(self,request):
		logout(request)
		messages.info(request, "You have successfully logged out.") 
		return redirect("/") 


class AddToCart(ListView):
	def get(self,request,*args, **kwargs):
		user=self.request.user
		product_id=self.request.GET.get('prod_id')
		product=Product.objects.get(id=product_id)	
		cart_item,created=CartItem.objects.get_or_create(user=user,product=product,ordered=False)
		cart_item.save()
		return redirect('/cart')

	
class CartItemView(View):
	def get(self,request):
		if request.user.is_authenticated:
			user=self.request.user
			cart=CartItem.objects.filter(user=user)
			amount=0.0
			shipping_amount=70.0
			total_amount=0.0
			cart_product=[p for p in CartItem.objects.all() if p.user==user]

			if cart_product:
				for p in cart_product:
					tempamount=(p.quantity*p.product.price)
					amount+=tempamount
					total_amount=amount+shipping_amount
					
				return render(request,"ecom/cart.html",{'carts':cart,'amount':amount,
				'tempamount':tempamount,'totalamount':total_amount})
			else:
				return render(self.request,"ecom/emptycart.html")


class PlusCartItem(View):
	def get(self,*args, **kwargs):
		prod_id=self.request.GET['prod_id']
		c=CartItem.objects.get(Q(product=prod_id)& Q(user=self.request.user))
		avialable=c.product.availability

		if c.quantity<avialable:
			c.quantity+=1
			c.save()
			amount=0.0
			shipping_amount=70.0
			cart_product=[p for p in CartItem.objects.all() if p.user==self.request.user]

		for p in cart_product:
			tempamount=(p.quantity*p.product.price)
			amount+=tempamount
			

		data={
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)


class MinusCartItem(View):
	def get(self,*args, **kwargs):
		prod_id=self.request.GET['prod_id']
		c=CartItem.objects.get(Q(product=prod_id)& Q(user=self.request.user))
		c.quantity-=1
		c.save()
		
		if c.quantity<=0:
			c.delete()
		amount=0.0
		shipping_amount=70.0
		cart_product=[p for p in CartItem.objects.all() if p.user==self.request.user]

		for p in cart_product:
			tempamount=(p.quantity*p.product.price)
			amount+=tempamount

		data={
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)


class DeleteCartItem(View):
	def get(self,*args, **kwargs):
		prod_id=self.request.GET['prod_id']
		c=CartItem.objects.get(Q(product=prod_id)& Q(user=self.request.user))
		c.delete()
		amount=0.0
		shipping_amount=70.0
		cart_product=[p for p in CartItem.objects.all() if p.user==self.request.user]

		for p in cart_product:
			tempamount=(p.quantity*p.product.price)
			amount+=tempamount

		data={
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)


class CheckoutView(View):
	def get(self,*args, **kwargs):
		user=self.request.user
		cart_items=CartItem.objects.filter(user=user)
		amount=0.0
		shiping_amount=70.0
		totalamount=0.0
		cart_product=[p for p in CartItem.objects.all() if p.user==self.request.user]
		if cart_product:
			for p in cart_product:
				tempamount=(p.quantity*p.product.price)
				amount+=tempamount
			totalamount=amount+shiping_amount
		return render(self.request,"ecom/checkout.html",{'totalamount':totalamount,
		'cart_items':cart_items,'user':user})



class PlacedOrderView(View):
	def get(self,*args, **kwargs):
		user=self.request.user
		cart_item=CartItem.objects.filter(user=user,ordered=False)
		order=Order.objects.create(user=user)

		for item in cart_item:
			order_item=OrderItem()
			order_item.product=item.product
			order_item.quantity=item.quantity
			order_item.user=item.user
			order_item.ordered=True
			order_item.total_cost=item.product.price*item.quantity
			order_item.save()

			order.items.add(order_item)
			product=order_item.product
			product.availability=product.availability-order_item.quantity
			product.save()
		
		order.ordered=True
		order.save()
		cart_item.delete()
		
		return render(self.request,"ecom/final.html",{'order':order})


		

class ProfileView(View):
	template_name="ecom/order.html"
	model=OrderItem

	def get(self, request):
		orderitems=[]
		user=request.user
		orders=Order.objects.all().filter(user=user,ordered=True)
		print(orders)
		for order in orders:
			for item in order.items.all():
				orderdict={}
				orderdict['order']={
					'id':order.id,
					'status':item.order.status,
					'date':item.order.ordered_date
				}
				orderdict['product']={
					'name':item.product.name,
					'price':item.product.price,
					#'quantity':item.product.quantity,
					'image':item.product.image.url
				}
				orderdict['quantity']=item.quantity
				orderdict['total_cost']=item.quantity*item.product.price
				orderitems.append(orderdict)	
		context={
			'items':orderitems
		}

		return render(request,self.template_name,context)

		
	


