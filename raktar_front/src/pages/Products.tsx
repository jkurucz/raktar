import { Card, Table, Badge, NumberFormatter, Button } from '@mantine/core';
import { useEffect, useState } from 'react';
import api from '../api/api.ts';
import { IProducts } from '../interfaces/IProducts.ts';
import { useNavigate } from 'react-router-dom';
import { roleKeyName } from "../constants/constants.ts";


const Products = () => {
  const [items, setItems] = useState<IProducts[]>([]);
  const navigate = useNavigate();
 


useEffect(() => {
  api.Products.getProducts()
    .then(res => {
      setItems(res.data);
    })
    .catch(error => {
      console.error('Hiba a termékek betöltésekor:', error);
    });
}, []);


  //console.log('items', items);

  const role = localStorage.getItem(roleKeyName);
  // const role = localStorage.getItem('role');
  //console.log('role', role);

  const rows = items.map((element) => (
    <Table.Tr key={element.id}>
      <Table.Td>{element.product_name}</Table.Td>
      <Table.Td>{element.description}</Table.Td>
      <Table.Td><Badge><NumberFormatter value={element.price} suffix=" Ft" thousandSeparator={" "} /></Badge></Table.Td>
      <Table.Td>
        {role === 'Admin' ? (
          <>
            <Button onClick={() => navigate(`${element.id}`)} color="green">Módosítás</Button>
            <Button onClick={() => {api.Products.deleteProduct(`${element.id}`);}} color="red">Törlés</Button>
          </>
        ) : (
          <Button
  color="dark"
  onClick={() => {
    api.Orders.createOrder({
      items: [{ product_id: element.id, quantity: 1 }]
    }).then(() => {
      alert("Megrendelés sikeres!");
      // opcionálisan újratöltés vagy navigálás:
      // navigate('/orders');
    }).catch((err) => {
      console.error("Megrendelés hiba:", err);
      alert("Nem sikerült megrendelni a terméket.");
    });
  }}
>
  Megrendelem
</Button>
        )}
      </Table.Td>
      
    </Table.Tr>
  ));


  return <div>
    {/* Role szereposztás */}
      {role === 'Admin' && (
        <Button onClick={() => navigate('add')}>Új Termék</Button>
      )}
    <Card shadow="sm" padding="lg" radius="md" withBorder>
   
    <Table>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Termék:</Table.Th>
          <Table.Th>Leírás:</Table.Th>
          <Table.Th>Ár:</Table.Th>
          <Table.Th>Műveletek:</Table.Th>

          
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>{rows}</Table.Tbody>
    </Table>

    </Card>
  </div>
}

export default Products;