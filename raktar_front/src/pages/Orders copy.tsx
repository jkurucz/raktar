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
import { useNavigate } from "react-router-dom";
import { roleKeyName } from "../constants/constants";

const Orders = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const navigate = useNavigate();
  const role = localStorage.getItem(roleKeyName);

  useEffect(() => {
    api.Orders.getOrders().then((res) => {
      setOrders(res.data);
    }).catch((err) => {
      console.error("Hiba a rendelések betöltésekor:", err);
    });
  }, []);

  const rows = orders.map((order) => {
    const itemSummary = order.items.map(i => `#${i.product_id} x${i.quantity}`).join(", ");
    const latestStatus = Array.isArray(order.status) && order.status.length > 0
  ? order.status[0].status
  : "Nincs státusz";

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
