import Login from "../pages/Login.tsx";
import ForgotPassword from "../pages/ForgotPassword.tsx";
import Dashboard from "../pages/Dashboard.tsx";
import Products from "../pages/Products.tsx";
import ProductForm from "../pages/ProductForm.tsx";
import Registrate from "../pages/Registrate.tsx";
import Orders from "../pages/Orders.tsx";
import Users from "../pages/Users.tsx";
import UserForm from "../pages/UserForm.tsx";
import Transcomp from "../pages/Transcomp.tsx";
import Transport from "../pages/Transport.tsx";

export const routes = [
    {
        path: "login",
        component: <Login/>,
        isPrivate: false
    },
    {
        path: "forgot",
        component: <ForgotPassword/>,
        isPrivate: false
    },
    {
        path: "registrate",
        component: <Registrate/>,
        isPrivate: false
    },
    {
        path: "dashboard",
        component: <Dashboard/>,
        isPrivate: true
    },
    {
        path: "product",
        component: <Products/>,
        isPrivate: true
    },
    {
        path: "orders",
        component: <Orders/>,
        isPrivate: true
    },
    {
        path: "users",
        component: <Users/>,
        isPrivate: true
    },
      {
        path: "users/:id",
        component: <UserForm />,
        isPrivate: true
    },
    {
        path: "product/add",
        component: <ProductForm isCreate={true}/>,
        isPrivate: true
    },
    {
        path: "product/:id",
        component: <ProductForm isCreate={false}/>,
        isPrivate: true
    },
    {
        path: "transcomp",
        component: <Transcomp />,
        isPrivate: true
    },
    {
        path: "transport",
        component: <Transport />,
        isPrivate: true
    },
]