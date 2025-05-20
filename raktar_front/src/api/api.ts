import axiosInstance from "./axios.config.ts";
import { IProducts } from "../interfaces/IProducts.ts";
import { ICreateProduct } from "../interfaces/ICreateProduct.ts";
import { Order } from "../interfaces/IOrders.ts";
import { User } from "../interfaces/IUsers.ts";
import { SafeUpdateUserRequest } from "../interfaces/IUsers.ts";
import { ITransportOrder } from "../interfaces/ITransportOrder.ts";
import { IComplaint } from "../interfaces/IComplaints.ts";
import { IWarehouseStock } from "../interfaces/IWarehouseStock";
import { IWarehouse } from "../interfaces/IWarehouse";

const Auth = {
  login: (email: string, password: string)  => axiosInstance.post<{token: string}>('/user/users/login', {email, password})
}

const Registrate = {
  registrate: (email: string, name: string, password: string, phone: string, address: {
    city: string; country: string; postalcode: string; street: string;}) =>
    axiosInstance.post("/user/users/register", {email, name, password, phone, address,}),
};

const Products = {
  getProducts: ()=> axiosInstance.get<IProducts[]>('/product/'),
  getProduct: (id: string ) => axiosInstance.get<IProducts>(`/product/${id}`),
  updateProduct: (id: string, obj: ICreateProduct) => axiosInstance.put(`/product/${id}/`, obj),
  createProduct: (obj: ICreateProduct) => axiosInstance.post('/product/', obj),
  deleteProduct: (id: string) => axiosInstance.delete(`/product/${id}`)
};

const Orders = {
  getOrders: () => axiosInstance.get<Order[]>('/order/'), 
  getAllOrders: () => axiosInstance.get<Order[]>('/order/all'),
  getOrderById: (id: number) => axiosInstance.get<Order>(`/orders/${id}`),
  createOrder: (orderData: { items: { product_id: number; quantity: number }[] }) =>
    axiosInstance.post("/order/", orderData),
  getUnassignedOrders: () => axiosInstance.get<Order[]>('/order/unassigned')
};

const Users = {
  getAllUsers: () => axiosInstance.get<User[]>('/user/'),
  getUserById: (id: string) => axiosInstance.get<User>(`/user/users/${id}`),
  updateUser: (id: string, data: any) => axiosInstance.put(`/user/users/${id}`, data),
  getRoles: () => axiosInstance.get<{ name: string }[]>('/user/roles'),
  safeUpdateUser: (id: string, data: SafeUpdateUserRequest) => 
    axiosInstance.put<User>(`/user/users/${id}/safe-update`, data),
  getMyProfile: () => axiosInstance.get<User>('/user/users/me'),
  updateMyProfile: (data: Partial<User>) => axiosInstance.put<User>('/user/users/me', data)
};

const Transcomp = {
  getAll: () => axiosInstance.get('/transcomp/'),
  create: (data: { truck: string; company: string }) => axiosInstance.post('/transcomp/', data),
  delete: (id: number) => axiosInstance.delete(`/transcomp/${id}`)
};

const TransportOrders = {
  getAll: () => axiosInstance.get<ITransportOrder[]>('/transport/'),
  getById: (id: number) => axiosInstance.get<ITransportOrder>(`/transport/${id}`),
  updateStatus: (id: number, data: { status: string; load_date?: string | null }) =>
  axiosInstance.patch(`/transport/${id}`, data),
  assignTransport: (id: number, data: { transport_id: number; status: string; load_date: string }) => 
    axiosInstance.put(`/transport/${id}/assign`, data),
  create: (data: {order_id: number; transport_id: number; load_date: string; direction?: string;}) => 
    axiosInstance.post("/transport/", data),
};

const Complaints = {
  getAllComplaints: () => axiosInstance.get<IComplaint[]>('/complaint/complaints'),       
  getOrderComplaints: (orderId: number) => axiosInstance.get<IComplaint[]>(`/complaint/orders/${orderId}/complaints`), 
  createComplaint: (orderId: number, message: string) =>
    axiosInstance.post<IComplaint>(`/complaint/orders/${orderId}/complaints`, { message }),
};

const Warehouse = {
  getStock: (warehouseId: number) =>
    axiosInstance.get<IWarehouseStock[]>(`/warehouse/warehouse-stocks/${warehouseId}`),
  updateStock: (product_id: number, warehouse_id: number, quantity: number) =>
    axiosInstance.post<IWarehouseStock>(`/warehouse/warehouse-stocks`, { product_id, warehouse_id, quantity }),
  getWarehouses: () => axiosInstance.get<IWarehouse[]>(`/warehouse/warehouses`)
};

const api = {Products, Auth, Registrate, Orders, Users, Transcomp, TransportOrders, Complaints, Warehouse};
export default api;
