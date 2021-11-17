from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .categories import category_list

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    preview_image = models.ImageField(default='default.jpg', upload_to='art')
    full_image = models.ImageField(default='default.jpg', upload_to='art')
    
    public = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    category = models.CharField(max_length=20, choices=category_list, default=category_list[-1][0])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

# class corder(models.Model):
#     # init
#     buyer_id = models.ForeignKey(User)
#     seller_id = models.ForeignKey(User)

#     # buyer
#     price = models.DecimalField(max_digits=7, decimal_places=2)
#     description = models.TextField()
#     step1 = models.BooleanField(default=False)

#     # seller
#     preview_img = models.ImageField(default='none.jpg', upload_to='order_imgs')
#     final_img = models.ImageField(default='none.jpg', upload_to='order_imgs')

#     # buyer
#     step2 = models.BooleanField(default=False)