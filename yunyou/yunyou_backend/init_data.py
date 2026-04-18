"""Initialize database with sample data"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.attractions.models import Attraction
from apps.products.models import Category, Product
from apps.users.models import UserTask

User = get_user_model()

def create_admin():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin',
            phone='13800138000'
        )
        print('✓ 管理员账号已创建: admin / admin123')

def create_sample_attractions():
    attractions = [
        {
            'name': '故宫博物院',
            'location': '北京',
            'province': '北京市',
            'city': '北京市',
            'description': '中国明清两代的皇家宫殿，旧称紫禁城。',
            'detailed_description': '故宫是世界上现存规模最大、保存最为完整的木质结构古建筑之一，是国家AAAAA级旅游景区。',
            'rating': 4.9,
            'rating_count': 10000,
            'tags': ['历史', '文化', '建筑', '世界遗产'],
            'category': '历史文化',
            'price': 60,
            'opening_hours': '08:30-17:00',
            'address': '北京市东城区景山前街4号',
            'latitude': 39.9163,
            'longitude': 116.3972,
            'is_recommended': True,
            'is_hot': True,
            'visit_duration': 240,
            'facilities': ['停车场', '卫生间', '餐饮', '讲解器'],
            'traffic_info': '地铁1号线天安门东站下车',
        },
        {
            'name': '长城',
            'location': '北京',
            'province': '北京市',
            'city': '北京市',
            'description': '世界文化遗产，中国古代军事防御工程。',
            'detailed_description': '长城是中国古代的军事防御工程，是世界文化遗产。',
            'rating': 4.8,
            'rating_count': 15000,
            'tags': ['历史', '文化', '壮丽', '世界遗产'],
            'category': '自然景观',
            'price': 45,
            'opening_hours': '07:00-18:00',
            'address': '北京市延庆区八达岭镇',
            'latitude': 40.3580,
            'longitude': 116.5704,
            'is_recommended': True,
            'is_hot': True,
            'visit_duration': 180,
            'facilities': ['停车场', '索道', '餐饮', '纪念品店'],
            'traffic_info': '公交877路直达',
        },
        {
            'name': '东方明珠',
            'location': '上海',
            'province': '上海市',
            'city': '上海市',
            'description': '上海标志性建筑，电视塔。',
            'detailed_description': '东方明珠广播电视塔是上海的标志性文化景观之一。',
            'rating': 4.7,
            'rating_count': 8000,
            'tags': ['地标', '景观', '现代', '夜景'],
            'category': '城市观光',
            'price': 180,
            'opening_hours': '09:00-21:00',
            'address': '上海市浦东新区世纪大道1号',
            'latitude': 31.2397,
            'longitude': 121.4998,
            'is_recommended': True,
            'is_hot': True,
            'visit_duration': 120,
            'facilities': ['电梯', '观光厅', '旋转餐厅', '纪念品店'],
            'traffic_info': '地铁2号线陆家嘴站下车',
        },
        {
            'name': '西湖',
            'location': '杭州',
            'province': '浙江省',
            'city': '杭州市',
            'description': '中国著名的风景游览胜地。',
            'detailed_description': '西湖是中国大陆首批国家重点风景名胜区。',
            'rating': 4.9,
            'rating_count': 20000,
            'tags': ['自然', '湖泊', '文化', '世界遗产'],
            'category': '自然景观',
            'price': 0,
            'opening_hours': '全天开放',
            'address': '浙江省杭州市西湖区西湖风景名胜区',
            'latitude': 30.2465,
            'longitude': 120.1488,
            'is_recommended': True,
            'is_hot': True,
            'visit_duration': 360,
            'facilities': ['游船', '自行车', '餐饮'],
            'traffic_info': '地铁1号线龙翔桥站',
        },
        {
            'name': '张家界',
            'location': '张家界',
            'province': '湖南省',
            'city': '张家界市',
            'description': '世界地质公园，独特的石英砂岩峰林地貌。',
            'detailed_description': '张家界国家森林公园是中国第一个国家森林公园。',
            'rating': 4.8,
            'rating_count': 12000,
            'tags': ['自然', '山地', '世界遗产', '奇观'],
            'category': '自然景观',
            'price': 225,
            'opening_hours': '08:00-18:00',
            'address': '湖南省张家界市武陵源区',
            'latitude': 29.1171,
            'longitude': 110.4474,
            'is_recommended': True,
            'is_hot': True,
            'visit_duration': 480,
            'facilities': ['索道', '电梯', '环保车', '餐饮'],
            'traffic_info': '张家界荷花机场转大巴',
        },
    ]
    
    for data in attractions:
        Attraction.objects.get_or_create(name=data['name'], defaults=data)
    print(f'✓ 已创建 {len(attractions)} 个景点')

def create_sample_categories():
    categories = [
        {'name': '文创产品', 'icon': 'palette', 'order': 1},
        {'name': '生活用品', 'icon': 'home', 'order': 2},
        {'name': '数码配件', 'icon': 'smartphone', 'order': 3},
        {'name': '户外装备', 'icon': 'compass', 'order': 4},
    ]
    
    for data in categories:
        Category.objects.get_or_create(name=data['name'], defaults=data)
    print(f'✓ 已创建 {len(categories)} 个商品分类')

def create_sample_products():
    products = [
        {
            'name': '故宫文创书签',
            'description': '定制版故宫书签一套，精美包装。',
            'points': 200,
            'price': 29.9,
            'stock': 100,
            'is_new': True,
            'is_featured': True,
        },
        {
            'name': '旅行帆布包',
            'description': '简约大方，容量充足，适合旅行使用。',
            'points': 500,
            'price': 89.9,
            'stock': 50,
            'is_featured': True,
        },
        {
            'name': '便携旅行洗漱包',
            'description': '多功能收纳，方便携带。',
            'points': 300,
            'price': 59.9,
            'stock': 80,
            'is_new': True,
        },
        {
            'name': '移动电源20000mAh',
            'description': '大容量快充，旅途不断电。',
            'points': 800,
            'price': 159.9,
            'stock': 30,
        },
        {
            'name': '城市旅行地图册',
            'description': '精美手绘风格，收录热门旅游城市。',
            'points': 150,
            'price': 39.9,
            'stock': 120,
            'is_featured': True,
        },
    ]
    
    category = Category.objects.first()
    for data in products:
        data['category'] = category
        Product.objects.get_or_create(name=data['name'], defaults=data)
    print(f'✓ 已创建 {len(products)} 个商品')

def create_sample_tasks():
    tasks = [
        {
            'title': '每日签到',
            'description': '每天签到获得积分奖励',
            'task_type': 'daily',
            'points_reward': 10,
        },
        {
            'title': '发布游记',
            'description': '发布一篇旅游分享帖子',
            'task_type': 'daily',
            'points_reward': 50,
        },
        {
            'title': '景点打卡',
            'description': '完成一个景点的参观并评分',
            'task_type': 'daily',
            'points_reward': 30,
        },
        {
            'title': '旅行达人',
            'description': '访问10个不同的景点',
            'task_type': 'achievement',
            'points_reward': 500,
        },
        {
            'title': '社交达人',
            'description': '发布20篇帖子',
            'task_type': 'achievement',
            'points_reward': 1000,
        },
    ]
    
    admin = User.objects.filter(role='admin').first()
    if admin:
        for data in tasks:
            UserTask.objects.get_or_create(
                user=admin, 
                title=data['title'], 
                defaults=data
            )
    print(f'✓ 已创建 {len(tasks)} 个任务')

if __name__ == '__main__':
    print('开始初始化数据...')
    create_admin()
    create_sample_attractions()
    create_sample_categories()
    create_sample_products()
    create_sample_tasks()
    print('数据初始化完成!')
