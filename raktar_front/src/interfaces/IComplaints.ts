export interface IComplaint {
  id: number;
  order_id: number;
  user_id: number;
  message: string;
  created_at: string;
  user_name?: string;
  order_items?: { product_name: string; quantity: number }[];
}