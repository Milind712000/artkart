from django.db import models
from django.db.models.fields.files import ImageField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .categories import category_list
from datetime import datetime

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(default='default.jpg', upload_to='art')
    
    public = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    category = models.CharField(max_length=20, choices=category_list, default=category_list[-1][0])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Purchases(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='art')
    category = models.CharField(max_length=20, choices=category_list, default=category_list[-1][0])

class CustomOrder(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_seller')

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    description_update_date = models.DateTimeField(default=datetime.now)

    phase_0 = models.BooleanField(default=False) #buyer has placed order

    phase_1 = models.BooleanField(default=False) #seller has seen the order
    rejected = models.BooleanField(default=False) #order rejected by seller

    image = models.ImageField(default='none.png', upload_to='art') #seller 
    image_update_date = models.DateTimeField(default=datetime.now)

    phase_2 = models.BooleanField(default=False) #buyer confirms
