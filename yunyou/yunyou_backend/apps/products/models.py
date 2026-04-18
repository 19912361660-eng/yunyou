"""Product models"""
from django.db import models
from django.conf import settings


class Category(models.Model):
    """Product category"""
    name = models.CharField('分类名称', max_length=50)
    icon = models.CharField('图标', max_length=50, blank=True)
    description = models.TextField('描述', blank=True)
    order = models.IntegerField('排序', default=0)
    
    class Meta:
        db_table = 'product_categories'
        ordering = ['order']


class Product(models.Model):
    """Exchange product model"""
    
    STATUS_CHOICES = [
        ('active', '上架'),
        ('inactive', '下架'),
        ('sold_out', '售罄'),
    ]
    
    name = models.CharField('商品名称', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField('描述')
    image = models.ImageField('主图', upload_to='products/')
    images = models.JSONField('图片列表', default=list, blank=True)
    points = models.IntegerField('所需积分')
    price = models.DecimalField('市场价', max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField('库存', default=0)
    sold_count = models.IntegerField('已兑换', default=0)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField('精选', default=False)
    is_new = models.BooleanField('新品', default=False)
    exchange_rules = models.TextField('兑换规则', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'products'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name


class ExchangeRecord(models.Model):
    """Points exchange record"""
    
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    record_no = models.CharField('兑换单号', max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exchanges')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    points_spent = models.IntegerField('消耗积分')
    quantity = models.IntegerField('数量', default=1)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    address = models.TextField('收货地址')
    contact_name = models.CharField('联系人', max_length=50)
    contact_phone = models.CharField('联系电话', max_length=20)
    tracking_no = models.CharField('快递单号', max_length=50, blank=True)
    shipped_at = models.DateTimeField('发货时间', null=True, blank=True)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'exchange_records'
        ordering = ['-created_at']
