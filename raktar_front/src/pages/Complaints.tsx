import { Card, Table, Text } from "@mantine/core";
import { useEffect, useState } from "react";
import api from "../api/api";
import { IComplaint } from "../interfaces/IComplaints";

const Complaints = () => {
  const [complaints, setComplaints] = useState<IComplaint[]>([]);

  useEffect(() => {
    api.Complaints.getAllComplaints()
      .then((res) => setComplaints(res.data))
      .catch((err) => console.error("Hiba a panaszok betöltésekor:", err));
  }, []);

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Text fz="xl" mb="md">Panaszok</Text>
      <Table>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>ID</Table.Th>
            <Table.Th>Dátum</Table.Th>
            <Table.Th>Felhasználó</Table.Th>
            <Table.Th>Megrendelés ID</Table.Th>
            <Table.Th>Termékek</Table.Th>
            <Table.Th>Leírás</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {complaints.length === 0 && (
            <Table.Tr>
              <Table.Td colSpan={4} align="center">
                Nincs panasz.
              </Table.Td>
            </Table.Tr>
          )}
          {complaints.map((c) => (
            <Table.Tr key={c.id}>
              <Table.Td>{c.id}</Table.Td>
              <Table.Td>{new Date(c.created_at).toLocaleDateString()}</Table.Td>
              <Table.Td>{c.user_name || c.user_id}</Table.Td>
              <Table.Td>{c.order_id}</Table.Td>
              <Table.Td>
                {c.order_items && c.order_items.length > 0 ? (
                  <ul style={{margin: 0, padding: 0, listStyle: "none"}}>
                    {c.order_items.map((item, i) => (
                      <li key={i}>
                        {item.product_name} x {item.quantity}
                      </li>
                    ))}
                  </ul>
                ) : "-"}
              </Table.Td>
              <Table.Td>{c.message}</Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
    </Card>
  );
};

export default Complaints;
