from django.contrib import admin
from .models import Post, Purchases, CustomOrder

admin.site.register(Post)
admin.site.register(Purchases)
admin.site.register(CustomOrder)
