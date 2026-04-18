import { Attraction, Product, User } from './types';

export const ATTRACTIONS_DATA: Attraction[] = [
  {
    id: '1',
    name: '故宫博物院',
    location: '北京',
    description: '中国明清两代的皇家宫殿，旧称紫禁城。',
    image: 'https://picsum.photos/seed/forbidden/800/600',
    rating: 4.9,
    tags: ['历史', '文化', '建筑'],
  },
  {
    id: '2',
    name: '长城',
    location: '北京',
    description: '世界文化遗产，中国古代军事防御工程。',
    image: 'https://picsum.photos/seed/greatwall/800/600',
    rating: 4.8,
    tags: ['历史', '文化', '壮丽'],
  },
  {
    id: '3',
    name: '东方明珠',
    location: '上海',
    description: '上海标志性建筑，电视塔。',
    image: 'https://picsum.photos/seed/shanghai/800/600',
    rating: 4.7,
    tags: ['地标', '景观', '现代'],
  },
];

export const PRODUCTS_DATA: Product[] = [
  {
    id: 'p1',
    name: '故宫文创书签',
    points: 200,
    description: '定制版故宫书签一套，精美包装。',
    image: 'https://picsum.photos/seed/bookmark/400/300',
  },
  {
    id: 'p2',
    name: '旅行帆布包',
    points: 500,
    description: '简约大方，容量充足。',
    image: 'https://picsum.photos/seed/bag/400/300',
  },
];

export const USERS_DATA: User[] = [
  { id: 'u1', name: '张三', email: 'zhangsan@example.com', role: '用户', status: '活跃' },
  { id: 'u2', name: '李四', email: 'lisi@example.com', role: '管理员', status: '活跃' },
  { id: 'u3', name: '王五', email: 'wangwu@example.com', role: '用户', status: '禁用' },
];
