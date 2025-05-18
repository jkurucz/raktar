import {
  Button,
  Card,
  Table,
  Text,
  Group
} from "@mantine/core";
import { useEffect, useState } from "react";
import api from "../api/api";
import { ITransportOrder } from "../interfaces/ITransportOrder";
import { useNavigate } from "react-router-dom";
import { roleKeyName } from "../constants/constants.ts";

const TransportOrders = () => {
  const [orders, setOrders] = useState<ITransportOrder[]>([]);

  // Ideiglenesen forgalomból kivonva!
  //const [statusUpdates, setStatusUpdates] = useState<{ [key: number]: string }>({});
  const navigate = useNavigate();

  useEffect(() => {
    api.TransportOrders.getAll().then((res) => {
      setOrders(res.data);
      console.log("Transport orders:", res.data);
    });
  }, []);

  const role = localStorage.getItem(roleKeyName);

  // Ideiglenesen forgalomból kivonva!
  // const handleStatusChange = (orderId: number, newStatus: string | null) => {
  //   if (!newStatus) return;
  //   setStatusUpdates(prev => ({ ...prev, [orderId]: newStatus }));

  //   const order = orders.find(o => o.id === orderId);
  //   const loadDate = order?.load_date || null;

  //   api.TransportOrders.updateStatus(orderId, {
  //     status: newStatus,
  //     load_date: loadDate
  //   }).then(() => {
  //     api.TransportOrders.getAll().then(res => setOrders(res.data));
  //   });
  // };

  const rows = orders.map(order => (
    <Table.Tr key={order.id}>
      <Table.Td>{order.id}</Table.Td>
      <Table.Td>
        <Text fw={700} ta="left">{order.user_name}</Text>
        <Text size="sm" ta="left">{order.user_address}</Text>
      </Table.Td>
      {order.items && order.items.length > 0 ? (
        <>
          <Table.Td>
            {order.items.map((item, idx) => (
              <Text key={idx} ta="left">{item.product_name}</Text>
            ))}
          </Table.Td>
          <Table.Td>
            {order.items.map((item, idx) => (
              <Text key={idx} ta="left">{item.quantity}</Text>
            ))}
          </Table.Td>
        </>
      ) : (
        <>
          <Table.Td>Nincs adat</Table.Td>
          <Table.Td>-</Table.Td>
        </>
      )}
      <Table.Td>
        <Text fw={700} ta="left">{order.transport_company || "-"}</Text>
        <Text size="sm" ta="left">{order.transport_truck || "-"}</Text>
      </Table.Td>
      {/* <Table.Td> */}
        {/* <Select
          placeholder="Státusz"
          data={statusOptions}
          value={order.status}
          onChange={(val) => handleStatusChange(order.id, val)}
        /> */}
      {/* </Table.Td> */}
      <Table.Td>
        <Text ta="left">{order.load_date ? new Date(order.load_date).toLocaleDateString() : "-"}</Text>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Card withBorder shadow="sm" p="lg">
      <Group justify="space-between" mb="md">
        <Text fz="xl">Fuvarfeladatok</Text>
               {(role === 'Admin' || role === 'Transport' )&& (
        <Button onClick={() => navigate('add')}>
          Új fuvarfeladat
        </Button>
      )}
      </Group>
      <Table>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>ID</Table.Th>
            <Table.Th>Megrendelő</Table.Th>
            <Table.Th>Termék</Table.Th>
            <Table.Th>Mennyiség</Table.Th>
            <Table.Th>Szállító</Table.Th>
            {/* <Table.Th>Státusz</Table.Th> */}
            <Table.Th>Rakodás dátuma</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Card>
  );
};

export default TransportOrders;

