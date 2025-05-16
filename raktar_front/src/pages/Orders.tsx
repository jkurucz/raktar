import {
  Button,
  Card,
  Stack,
  Table,
  Text
} from "@mantine/core";
import { useEffect, useState } from "react";
import api from "../api/api";
import { Order } from "../interfaces/IOrders.ts";
import { IProducts } from "../interfaces/IProducts.ts";
import { useNavigate } from "react-router-dom";
import { roleKeyName } from "../constants/constants";

const Orders = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [products, setProducts] = useState<IProducts[]>([]);
  const navigate = useNavigate();
  const role = localStorage.getItem(roleKeyName);

  useEffect(() => {
    if (role === "User") {
      api.Orders.getOrders()
        .then((res) => {
          setOrders(res.data);
        })
        .catch((err) => {
          console.error("Hiba a rendelések betöltésekor:", err);
        });
    } else {
      api.Orders.getAllOrders()
        .then((res) => {
          setOrders(res.data);
        })
        .catch((err) => {
          console.error("Hiba a rendelések betöltésekor:", err);
        });
    }

    // Termékek betöltése a nevekhez
    api.Products.getProducts()
      .then((res) => {
        setProducts(res.data);
      })
      .catch((err) => {
        console.error("Hiba a termékek betöltésekor:", err);
      });
  }, [role]);

  // Termék ID -> Név
  const productMap = Object.fromEntries(products.map(p => [p.id, p.product_name]));

  // Rendelések sorainak előállítása (egy order = több sor: annyi, ahány termék van benne)
  const rows = orders.flatMap((order) => {
    return order.items.map((item, idx) => (
      <Table.Tr key={`${order.id}_${item.product_id}`}>
        {/* Első sorban jelenik meg a rendelés azonosítója, dátuma, ügyfél, fuvar (ha admin/warehouse/transport) */}
        {idx === 0 ? (
          <>
            <Table.Td rowSpan={order.items.length}>{order.id}</Table.Td>
            <Table.Td rowSpan={order.items.length}>
              {new Date(order.order_date).toLocaleDateString()}
            </Table.Td>
          </>
        ) : null}
        {/* Terméknév és darabszám külön oszlopban */}
        <Table.Td>{item.quantity}</Table.Td>
        <Table.Td>{productMap[item.product_id] || `#${item.product_id}`}</Table.Td>
        {/* Ügyfél adatok csak admin/warehouse/transport role-nál, és csak az első sorban */}
        {["Admin", "Warehouse", "Transport"].includes(role || "") && idx === 0 && (
          <Table.Td rowSpan={order.items.length}>
            <Stack gap={4}>
              <Text fz="sm"><strong>Név:</strong> {order.user_name || '-'}</Text>
              <Text fz="sm"><strong>Cím:</strong> {order.user_address || '-'}</Text>
              <Text fz="sm"><strong>Telefon:</strong> {order.user_phone || '-'}</Text>
            </Stack>
          </Table.Td>
        )}
        {/* ÚJ: Fuvarozó (cég, rendszám, dátum) - csak első sorban */}
        {["Admin", "Warehouse", "Transport", "User"].includes(role || "") && idx === 0 && (
          <Table.Td rowSpan={order.items.length}>
            <Stack gap={4}>
              <Text fz="sm"><strong>Cég:</strong> {order.transport_company || '-'}</Text>
              <Text fz="sm"><strong>Rendszám:</strong> {order.transport_truck || '-'}</Text>
              <Text fz="sm"><strong>Szállítás: </strong> 
                {order.load_date
                  ? new Date(order.load_date).toLocaleDateString()
                  : '-'}
              </Text>
            </Stack>
          </Table.Td>
        )}
        {/* Műveletek csak az első sorban */}
        {idx === 0 ? (
          <Table.Td rowSpan={order.items.length}>
            {/* {role === "Admin" && (
              <Button onClick={() => navigate(`/orders/${order.id}`)} size="xs" color="blue">
                Módosítás
              </Button>
            )}
            {role === "Transport" && (
              <Button onClick={() => navigate(`/orders/${order.id}/delivery`)} size="xs" color="orange">
                Fuvar hozzáadása
              </Button>
            )}
            {role === "Warehouse" && (
              <Button onClick={() => navigate(`/orders/${order.id}/location`)} size="xs" color="gray">
                Raktárhely
              </Button>
            )} */}
            {role === "User" && (
              <Button onClick={() => navigate(`${order.id}/complaint`)} size="xs" color="red">
                Panasz
              </Button>
            )}
          </Table.Td>
        ) : null}
      </Table.Tr>
    ));
  });

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Text fz="xl" mb="md">Megrendelések</Text>
      <Table>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>ID</Table.Th>
            <Table.Th>Dátum</Table.Th>
            <Table.Th>db</Table.Th>
            <Table.Th>Termék</Table.Th>
            {["Admin", "Warehouse", "Transport"].includes(role || "") && (
              <Table.Th>Ügyfél</Table.Th>
            )}
            {["Admin", "Warehouse", "Transport", "User"].includes(role || "") && (
              <Table.Th>Fuvar (cég, rendszám, dátum)</Table.Th>
            )}
            <Table.Th>Műveletek</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Card>
  );
};

export default Orders;
