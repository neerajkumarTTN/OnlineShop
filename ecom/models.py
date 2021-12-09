
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, User
# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email,password,username,mobile,address,**extrafields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            mobile=mobile,
            address=address,
            **extrafields
        )

        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_user(self,email,password,username,mobile,address,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,username,mobile,address,**extra_fields)

    def create_superuser(self,email,password,username,mobile,address,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email,password,username,mobile,address,**extra_fields)



class CustomUser(AbstractBaseUser,PermissionsMixin):
   email=models.EmailField(db_index=True,unique=True,max_length=254)
   username=models.CharField(max_length=250,null=True)
   mobile=models.CharField(max_length=50,null=True)
   address=models.CharField(max_length=250,null=True)

   is_staff=models.BooleanField(default=True)
   is_active=models.BooleanField(default=True)
   is_superuser=models.BooleanField(default=False)

   objects=CustomUserManager()

   USERNAME_FIELD='email'
   REQUIRED_FIELDS=['username','mobile','address']
    
  

   class Meta:
       verbose_name='User'
       verbose_name_plural='Users'

class Shipping_address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    shipping_address=models.CharField(max_length=250)

    def __str__(self):
        # print(self.order.id)
        return str(self.shipping_address)
    
class Product(models.Model):
    name=models.CharField(max_length=150)
    content=models.TextField(null=True)
    image=models.ImageField(upload_to="items",null=True)
    price=models.FloatField(null=False,blank=False,default=0,)
    availability=models.PositiveIntegerField(default=1)
    slug=models.SlugField(unique=True,db_index=True,)

    def __str__(self) -> str:
        return f"{self.name}"
   

STATUS_CHOICES=(  
    ('Pending','Pending'),
    ('Delivered','Delivered'),
    ('Accepted','Accepted'),
    ('Cancel','Cancel')
    )


class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    #product=models.ForeignKey(OrderItem,on_delete=models.CASCADE,null=True)
    address=models.ForeignKey(Shipping_address,on_delete=models.SET_NULL,blank=True,null=True)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=30,choices=STATUS_CHOICES,default='pending')
    ordered = models.BooleanField(default=False)

    @property
    def total_cast(self):
        return self.quantity*self.product.price

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True,related_name="items")

    total_cost=models.IntegerField(default=0)
    

class Cart(models.Model):

    cart_id = models.CharField(max_length=250, blank=True)
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True,related_name='items')
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
 
    @property
    def total_cost(self):
        return self.quantity * self.product.price