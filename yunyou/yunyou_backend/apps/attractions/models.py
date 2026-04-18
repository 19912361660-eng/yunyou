"""Attraction models for 云游智行"""
from django.db import models
from django.conf import settings


class Attraction(models.Model):
    """Tourist attraction model"""
    
    name = models.CharField('景点名称', max_length=200)
    location = models.CharField('位置', max_length=200)
    province = models.CharField('省份', max_length=50, blank=True)
    city = models.CharField('城市', max_length=50, blank=True)
    description = models.TextField('描述')
    detailed_description = models.TextField('详细介绍', blank=True)
    image = models.ImageField('主图', upload_to='attractions/', blank=True, null=True)
    images = models.JSONField('图片列表', default=list, blank=True)
    rating = models.DecimalField('评分', max_digits=2, decimal_places=1, default=0)
    rating_count = models.IntegerField('评分人数', default=0)
    tags = models.JSONField('标签', default=list)
    category = models.CharField('类别', max_length=50, blank=True)
    price = models.DecimalField('门票价格', max_digits=10, decimal_places=2, default=0)
    opening_hours = models.CharField('开放时间', max_length=100, blank=True)
    address = models.CharField('地址', max_length=500, blank=True)
    latitude = models.DecimalField('纬度', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('经度', max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField('联系电话', max_length=50, blank=True)
    website = models.URLField('官网', blank=True)
    is_recommended = models.BooleanField('推荐景点', default=False)
    is_hot = models.BooleanField('热门景点', default=False)
    visit_duration = models.IntegerField('建议游览时长(分钟)', default=120)
    facilities = models.JSONField('设施', default=list, blank=True)
    traffic_info = models.TextField('交通信息', blank=True)
    view_count = models.IntegerField('浏览次数', default=0)
    like_count = models.IntegerField('点赞数', default=0)
    status = models.CharField('状态', max_length=20, choices=[
        ('active', '开放'), ('closed', '关闭'), ('maintenance', '维护中')
    ], default='active')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'attractions'
        verbose_name = '景点'
        verbose_name_plural = '景点管理'
        ordering = ['-rating', '-view_count']
    
    def __str__(self):
        return self.name
    
    def update_rating(self):
        from django.db.models import Avg
        from apps.users.models import VisitedAttraction
        
        result = VisitedAttraction.objects.filter(attraction=self).aggregate(Avg('rating'))
        avg = result['rating__avg'] or 0
        self.rating = round(avg, 1)
        self.rating_count = VisitedAttraction.objects.filter(attraction=self).count()
        self.save()


class AttractionImage(models.Model):
    """Additional attraction images"""
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField('图片', upload_to='attractions/gallery/')
    caption = models.CharField('图片说明', max_length=200, blank=True)
    order = models.IntegerField('排序', default=0)
    
    class Meta:
        db_table = 'attraction_images'
        ordering = ['order']


class Route(models.Model):
    """Travel route planning"""
    
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('shared', '已分享'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='routes')
    title = models.CharField('路线名称', max_length=200)
    description = models.TextField('路线描述', blank=True)
    start_date = models.DateField('开始日期', null=True, blank=True)
    end_date = models.DateField('结束日期', null=True, blank=True)
    total_days = models.IntegerField('总天数', default=1)
    estimated_cost = models.DecimalField('预估费用', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    is_public = models.BooleanField('公开路线', default=False)
    like_count = models.IntegerField('点赞数', default=0)
    share_count = models.IntegerField('分享次数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'routes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}的路线: {self.title}"


class RouteDay(models.Model):
    """Route day itinerary"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField('第几天')
    date = models.DateField('日期', null=True, blank=True)
    title = models.CharField('标题', max_length=200, blank=True)
    notes = models.TextField('备注', blank=True)
    
    class Meta:
        db_table = 'route_days'
        ordering = ['day_number']


class RouteAttraction(models.Model):
    """Attractions in a route"""
    route_day = models.ForeignKey(RouteDay, on_delete=models.CASCADE, related_name='attractions')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    order = models.IntegerField('顺序')
    arrival_time = models.TimeField('到达时间', null=True, blank=True)
    departure_time = models.TimeField('离开时间', null=True, blank=True)
    visit_duration = models.IntegerField('游览时长(分钟)', default=120)
    notes = models.TextField('备注', blank=True)
    transportation = models.CharField('交通方式', max_length=100, blank=True)
    
    class Meta:
        db_table = 'route_attractions'
        ordering = ['order']


class AttractionLike(models.Model):
    """User likes for attractions"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    created_at = models.DateTimeField('时间', auto_now_add=True)
    
    class Meta:
        db_table = 'attraction_likes'
        unique_together = ['user', 'attraction']
