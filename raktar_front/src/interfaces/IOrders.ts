export interface OrderItem {
  product_id: number;
  quantity: number;
}

export interface OrderStatus {
  status: string;
  status_date: string;
}

export interface Order {
  id: number;
  closed: boolean;
  order_date: string;
  items: OrderItem[];
  status: OrderStatus[];

  // csak ha admin/warehouse/transport vagy:
  user_name?: string;
  user_phone?: string;
  user_address?: string;
  

  //PRÓBA
  transport_company?: string;
  transport_truck?: string;
  load_date?: string;
}
