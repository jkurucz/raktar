import {
  Badge,
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
    // Rendelések betöltése
    api.Orders.getOrders().then((res) => {
      setOrders(res.data);
    }).catch((err) => {
      console.error("Hiba a rendelések betöltésekor:", err);
    });

    // Termékek betöltése a nevekhez
    api.Products.getProducts().then((res) => {
      setProducts(res.data);
    }).catch((err) => {
      console.error("Hiba a termékek betöltésekor:", err);
    });
  }, []);

  // ID -> név leképezés
  const productMap = Object.fromEntries(products.map(p => [p.id, p.product_name]));

  const rows = orders.map((order) => {
    const itemSummary = order.items.map(i =>
      `${productMap[i.product_id] || `#${i.product_id}`} x${i.quantity}`
    ).join(", ");

    const latestStatus = Array.isArray(order.status) && order.status.length > 0
      ? order.status[0].status
      : "Nincs státusz";

    const deliveryStatus = Array.isArray(order.status)
      ? order.status.find(s => s.status.toLowerCase().includes("kiszállítva"))
      : null;

    const deliveryDate = deliveryStatus?.status_date
      ? new Date(deliveryStatus.status_date).toLocaleString()
      : "Nincs megadva";

    return (
      <Table.Tr key={order.id}>
        <Table.Td>{order.id}</Table.Td>
        <Table.Td>{new Date(order.order_date).toLocaleString()}</Table.Td>
        <Table.Td>{itemSummary}</Table.Td>
        <Table.Td>{latestStatus}</Table.Td>
        <Table.Td>
          <Badge color={order.closed ? "green" : "red"}>
            {order.closed ? "Lezárva" : "Folyamatban"}
          </Badge>
        </Table.Td>
        <Table.Td>{deliveryDate}</Table.Td>

        {["Admin", "Warehouse", "Transport"].includes(role || "") && (
          <Table.Td>
            <Stack gap={4}>
              <Text fz="sm"><strong>Név:</strong> {order.user_name}</Text>
              <Text fz="sm"><strong>Cím:</strong> {order.user_address}</Text>
              <Text fz="sm"><strong>Telefon:</strong> {order.user_phone}</Text>
            </Stack>
          </Table.Td>
        )}

        <Table.Td>
          {role === "Admin" && (
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
          )}
        </Table.Td>
      </Table.Tr>
    );
  });

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Text fz="xl" mb="md">Megrendelések</Text>
      <Table>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>ID</Table.Th>
            <Table.Th>Dátum</Table.Th>
            <Table.Th>Termékek</Table.Th>
            <Table.Th>Státusz</Table.Th>
            <Table.Th>Állapot</Table.Th>
            <Table.Th>Szállítás ideje</Table.Th>
            {["Admin", "Warehouse", "Transport"].includes(role || "") && (
              <Table.Th>Felhasználó</Table.Th>
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
