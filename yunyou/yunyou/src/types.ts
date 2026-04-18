export enum Screen {
  HOME_WEB = 'HOME_WEB',
  ADMIN_DASHBOARD = 'ADMIN_DASHBOARD',
  ADMIN_USERS = 'ADMIN_USERS',
  ADMIN_ATTRACTIONS = 'ADMIN_ATTRACTIONS',
  ADMIN_SHOP = 'ADMIN_SHOP',
  WEB_ATTRACTIONS_LIST = 'WEB_ATTRACTIONS_LIST',
  WEB_ROUTE_PLANNING = 'WEB_ROUTE_PLANNING',
  WEB_MALL = 'WEB_MALL',
  WEB_COMMUNITY = 'WEB_COMMUNITY',
  WEB_ATTRACTION_DETAIL = 'WEB_ATTRACTION_DETAIL',
  ADMIN_ORDERS = 'ADMIN_ORDERS',
  ADMIN_DATA_CENTER = 'ADMIN_DATA_CENTER',
  WEB_PERSONAL = 'WEB_PERSONAL',
  WEB_TASKS = 'WEB_TASKS',
  ADMIN_ADD_USER = 'ADMIN_ADD_USER',
  ADMIN_SETTINGS = 'ADMIN_SETTINGS',
  WEB_AI_ASSISTANT = 'WEB_AI_ASSISTANT',
  ADMIN_ADD_ATTRACTION = 'ADMIN_ADD_ATTRACTION',
  ADMIN_ADD_PRODUCT = 'ADMIN_ADD_PRODUCT',
}

export interface Attraction {
  id: string;
  name: string;
  location: string;
  description: string;
  image: string;
  rating: number;
  tags: string[];
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  status: string;
}

export interface Product {
  id: string;
  name: string;
  points: number;
  description: string;
  image: string;
}
