export interface IWarehouseStock {
  id: number;
  product_id: number;
  warehouse_id: number;
  quantity: number;
  last_updated: string;
  product_name?: string;
  warehouse_location?: string;
}