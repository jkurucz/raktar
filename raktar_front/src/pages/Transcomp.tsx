import { useEffect, useState } from "react";
import { Button, Card, Group, Table, Text, TextInput } from "@mantine/core";
import api from "../api/api";
import { ITranscomp } from "../interfaces/ITranscomp";

const Transcomp = () => {
  const [data, setData] = useState<ITranscomp[]>([]);
  const [truck, setTruck] = useState("");
  const [company, setCompany] = useState("");

  const fetchData = () => {
    api.Transcomp.getAll().then(res => setData(res.data));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAdd = () => {
    if (!truck || !company) return;
    api.Transcomp.create({ truck, company }).then(() => {
      setTruck("");
      setCompany("");
      fetchData();
    });
  };

  const handleDelete = (id: number) => {
    api.Transcomp.delete(id).then(fetchData);
  };

  const rows = data.map(d => (
    <Table.Tr key={d.id}>
      <Table.Td>{d.truck}</Table.Td>
      <Table.Td>{d.company}</Table.Td>
      <Table.Td>
        <Button color="red" onClick={() => handleDelete(d.id)} size="xs">Törlés</Button>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Card>
      <Text fz="xl" mb="md">Fuvarozók és Kamionok</Text>
      <Group>
        <TextInput placeholder="Kamion típusa" value={truck} onChange={(e) => setTruck(e.currentTarget.value)} />
        <TextInput placeholder="Cég neve" value={company} onChange={(e) => setCompany(e.currentTarget.value)} />
        <Button onClick={handleAdd}>Hozzáadás</Button>
      </Group>

      <Table mt="md">
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Kamion</Table.Th>
            <Table.Th>Cég</Table.Th>
            <Table.Th>Művelet</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Card>
  );
};

export default Transcomp;

