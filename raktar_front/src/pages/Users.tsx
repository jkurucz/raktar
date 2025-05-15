import {
  Button,
  Card,
  Table,
  Text
} from "@mantine/core";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { User } from "../interfaces/IUsers.ts";
import { roleKeyName } from "../constants/constants";

const Users = () => {
  const [users, setUsers] = useState<User[]>([]);
  const navigate = useNavigate();
  const role = localStorage.getItem(roleKeyName);

 useEffect(() => {
  if (role === "Admin") {
    api.Users.getAllUsers()
      .then(res => {
        //console.log("Felhasználók:", res.data); 
        setUsers(res.data);
      })
      .catch(err => console.error("Hiba a felhasználók lekérésekor:", err));
  }
}, [role]);

  const rows = users.map((user) => {
    const roleNames = user.roles.map(r => r.name).join(", ");

  const address = Array.isArray(user.addresses) && user.addresses.length > 0
  ? user.addresses.map(c =>
      `${c.postalcode} ${c.city}, ${c.street}, ${c.country}`
    ).join(" | ")
  : "Nincs cím megadva";


    return (
      <Table.Tr key={user.id}>
        <Table.Td>{user.name}</Table.Td>
        <Table.Td>{user.email}</Table.Td>
        <Table.Td>{user.phone}</Table.Td>
        <Table.Td>{address}</Table.Td>
        <Table.Td>{roleNames}</Table.Td>
        <Table.Td>
          <Button onClick={() => navigate(`${user.id}`)} color="green">Módosítás</Button>
        </Table.Td>
      </Table.Tr>
    );
  });

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Text fz="xl" mb="md">Felhasználók</Text>
      <Table>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Név</Table.Th>
            <Table.Th>Email</Table.Th>
            <Table.Th>Telefon</Table.Th>
            <Table.Th>Cím</Table.Th>
            <Table.Th>Szerepkörök</Table.Th>
            <Table.Th>Művelet</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Card>
  );
};

export default Users;
