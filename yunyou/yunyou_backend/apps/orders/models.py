"""Order models"""
from django.db import models
from django.conf import settings


class Order(models.Model):
    """Order model"""
    
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
        ('completed', '已完成'),
    ]
    
    ORDER_TYPE_CHOICES = [
        ('ticket', '门票'),
        ('product', '商品'),
        ('package', '套餐'),
    ]
    
    order_no = models.CharField('订单号', max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField('订单类型', max_length=20, choices=ORDER_TYPE_CHOICES)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField('总金额', max_digits=10, decimal_places=2)
    points_used = models.IntegerField('使用积分', default=0)
    points_discount = models.DecimalField('积分抵扣', max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField('实付金额', max_digits=10, decimal_places=2)
    payment_method = models.CharField('支付方式', max_length=20, blank=True)
    payment_time = models.DateTimeField('支付时间', null=True, blank=True)
    contact_name = models.CharField('联系人', max_length=50)
    contact_phone = models.CharField('联系电话', max_length=20)
    note = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order_no}"


class OrderItem(models.Model):
    """Order item model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField('商品类型', max_length=20)
    item_id = models.IntegerField('商品ID')
    item_name = models.CharField('商品名称', max_length=200)
    quantity = models.IntegerField('数量', default=1)
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('小计', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        db_table = 'order_items'
