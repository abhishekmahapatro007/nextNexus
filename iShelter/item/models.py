from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
            ordering = ('name',)
            verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_adopt = models.BooleanField(default=False)
    fostered_by = models.ForeignKey(User, related_name='items',null=True, on_delete=models.CASCADE)
    fostered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
            ordering = ('name',)
            verbose_name_plural = 'Items'
    
    def __str__(self):
        return self.name