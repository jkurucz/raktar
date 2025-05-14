import axiosInstance from "./axios.config.ts";
import { IProducts } from "../interfaces/IProducts.ts";
import { ICreateProduct } from "../interfaces/ICreateProduct.ts";
import { Order,  } from "../interfaces/IOrders.ts";



const Auth = {
  login: (email: string, password: string)  => axiosInstance.post<{token: string}>('/user/users/login', {email, password})
}

const Registrate = {
  registrate: (
    email: string,
    name: string,
    password: string,
    phone: string,
    address: {
      city: string;
      country: string;
      postalcode: string;
      street: string;
    }
  ) =>
    axiosInstance.post("/user/users/register", {
      email,
      name,
      password,
      phone,
      address,
    }),
};

const Products = {
  getProducts: ()=> axiosInstance.get<IProducts[]>('/product/'),
  getProduct: (id: string ) => axiosInstance.get<IProducts>(`/product/${id}`),
  updateProduct: (id: string, obj: ICreateProduct) => axiosInstance.put(`/product/${id}/`, obj),
  createProduct: (obj: ICreateProduct) => axiosInstance.post('/product/', obj),
  deleteProduct: (id: string) => axiosInstance.delete(`/product/${id}`)
 
}

const Orders = {
  getOrders: () => axiosInstance.get<Order[]>('/order/'), // saját vagy összes
  getAllOrders: () => axiosInstance.get<Order[]>('/orders/all'),
  getOrderById: (id: number) => axiosInstance.get<Order>(`/orders/${id}`),
  createOrder: (orderData: { items: { product_id: number; quantity: number }[] }) =>
    axiosInstance.post("/order/", orderData)
};


const api = {Products, Auth, Registrate, Orders};
export default api;
