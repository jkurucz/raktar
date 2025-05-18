export interface ITransportOrder {
  id: number;
  order_id: number;
  carrier_id: number;
  transport_id: number | null;
  status: string;
  updated_at: string;
  load_date: string;
  user_name: string;
  user_address: string;
  items: { product_name: string; quantity: number }[];
  transport_company?: string;
  transport_truck?: string;
}