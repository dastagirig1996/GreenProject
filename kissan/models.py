from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.core.validators import MaxValueValidator,MinValueValidator 

STATE_CHOICES = (('KA', 'Karnataka'),
('AP', 'Andhra Pradesh'),
('KL', 'Kerala'),
('TN', 'Tamil Nadu'),
('MH', 'Maharashtra'),
('UP', 'Uttar Pradesh'),
('GA', 'Goa'),
('GJ', 'Gujarat'),
('RJ', 'Rajasthan'),
('HP', 'Himachal Pradesh'),
('TG', 'Telangana'),
('AR', 'Arunachal Pradesh'),
('AS', 'Assam'), ('BR', 'Bihar'),
('CT', 'Chhattisgarh'),
('HR', 'Haryana'),
('JH', 'Jharkhand'),
('MP', 'Madhya Pradesh'),
('MN', 'Manipur'),
('ML', 'Meghalaya'),
('MZ', 'Mizoram'),
('NL', 'Nagaland'),
('OR', 'Odisha'),
('PB', 'Punjab'),
('SK', 'Sikkim'),
('TR', 'Tripura'),
('UT', 'Uttarakhand'),
('WB', 'West Bengal'),
('AN', 'Andaman and Nicobar Islands'),
('CH', 'Chandigarh'),
('DH', 'Dadra and Nagar Haveli and Daman and Diu'),
('DL', 'Delhi'),
('JK', 'Jammu and Kashmir'),
('LD', 'Lakshadweep'),
('LA', 'Ladakh'),
('PY', 'Puducherry'))

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    locality=models.CharField(max_length=100)
    city=models.CharField(max_length=20)
    pincode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.user)

CATEGORY_CHOICES=(
    ('V','Vegitable'),
    ('F','Fruits'),
    ('M','Milk'),
    ('Fi','Fish')
)

class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discountd_price=models.FloatField()
    description=models.TextField()
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    quantity = models.IntegerField()
    Product_Added_date = models.DateTimeField(auto_now_add=True)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.title)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantiry=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delevered'),
    ('Cancle','Cancle')
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantiry=models.PositiveIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    
