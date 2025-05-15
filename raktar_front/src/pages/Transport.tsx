import {
  Badge,
  Button,
  Card,
  Select,
  Table,
  Text,
  TextInput,
  Stack
} from "@mantine/core";
import { useEffect, useState } from "react";
import api from "../api/api";
import { ITransportOrder } from "../interfaces/ITransportOrder";
import { ITranscomp } from "../interfaces/ITranscomp";

const TransportOrders = () => {
  const [orders, setOrders] = useState<ITransportOrder[]>([]);
  const [transcomps, setTranscomps] = useState<ITranscomp[]>([]);
  const [selectedTransportIds, setSelectedTransportIds] = useState<{ [key: number]: number }>({});
  const [selectedDates, setSelectedDates] = useState<{ [key: number]: string }>({});

  // useEffect(() => {
  //   api.TransportOrders.getAll().then(res => setOrders(res.data));
  //   api.Transcomp.getAll().then(res => setTranscomps(res.data));
  // }, []);

  useEffect(() => {
  api.TransportOrders.getAll().then((res) => {
    setOrders(res.data);  // <-- itt tömb jön vissza?
    console.log("Transport orders:", res.data);  // DEBUG
    api.Transcomp.getAll().then(res => setTranscomps(res.data));
  });
}, []);

  const assignTransport = (orderId: number) => {
    const transportId = selectedTransportIds[orderId];
    const loadDate = selectedDates[orderId];

    if (!transportId || !loadDate) return;

    api.TransportOrders.assignTransport(orderId, {
      transport_id: transportId,
      status: "in transit",
      load_date: new Date(loadDate).toISOString()
    }).then(() => {
      api.TransportOrders.getAll().then(res => setOrders(res.data));
    });
  };

  const rows = orders.map(order => {
    const items = order.items?.map(i => `${i.product_name} x${i.quantity}`).join(", ") || "Nincs adat";
    const userInfo = `${order.user_name}, ${order.user_address}`;

    return (
      <Table.Tr key={order.id}>
        <Table.Td>{order.id}</Table.Td>
        <Table.Td>{userInfo}</Table.Td>
        <Table.Td>{items}</Table.Td>
        <Table.Td>{order.transport_company || "-"} / {order.transport_truck || "-"}</Table.Td>
        <Table.Td><Badge>{order.status}</Badge></Table.Td>
        <Table.Td>
          <Stack gap="xs">
            <Select
              placeholder="Fuvarozó kiválasztása"
              data={transcomps.map(tc => ({
                value: tc.id.toString(),
                label: `${tc.company} - ${tc.truck}`
              }))}
              onChange={val => setSelectedTransportIds(prev => ({
                ...prev,
                [order.id]: Number(val)
              }))}
            />
            <TextInput
              type="date"
              value={selectedDates[order.id] || ""}
              onChange={e => setSelectedDates(prev => ({
                ...prev,
                [order.id]: e.currentTarget.value
              }))}
              placeholder="Rakodás dátuma"
            />
            <Button
              onClick={() => assignTransport(order.id)}
              disabled={!selectedTransportIds[order.id] || !selectedDates[order.id]}
            >
              Mentés
            </Button>
          </Stack>
        </Table.Td>
      </Table.Tr>
    );
  });

  return (
    <Card withBorder shadow="sm" p="lg">
      <Text fz="xl" mb="md">Fuvarfeladatok</Text>
      <Table>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>ID</Table.Th>
            <Table.Th>Megrendelő</Table.Th>
            <Table.Th>Termékek</Table.Th>
            <Table.Th>Szállító</Table.Th>
            <Table.Th>Státusz</Table.Th>
            <Table.Th>Hozzárendelés</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Card>
  );
};

export default TransportOrders;
