import { Card, Table, Badge, NumberFormatter, Button, NumberInput } from '@mantine/core';
import { useEffect, useState } from 'react';
import api from '../api/api.ts';
import { IProducts } from '../interfaces/IProducts.ts';
import { IWarehouseStock } from '../interfaces/IWarehouseStock.ts';
import { useNavigate } from 'react-router-dom';
import { roleKeyName } from "../constants/constants.ts";

const WAREHOUSE_ID = 1;

const Products = () => {
  const [items, setItems] = useState<IProducts[]>([]);
  const [stock, setStock] = useState<IWarehouseStock[]>([]);
  const [quantities, setQuantities] = useState<{ [key: number]: number }>({});
  const navigate = useNavigate();

  useEffect(() => {
    api.Products.getProducts()
      .then(res => setItems(res.data))
      .catch(error => {
        console.error('Hiba a termékek betöltésekor:', error);
      });
    api.Warehouse.getStock(WAREHOUSE_ID)
      .then(res => setStock(res.data))
      .catch(error => {
        console.error('Hiba a raktárkészlet betöltésekor:', error);
      });
  }, []);

  const role = localStorage.getItem(roleKeyName);
  const stockMap = Object.fromEntries(stock.map(s => [s.product_id, s.quantity]));

  const handleQuantityChange = (productId: number, value: number | string) => {
    if (typeof value === "number" && value >= 0) {
      setQuantities(prev => ({ ...prev, [productId]: value }));
    }
  };

  const handleOrder = async (product: IProducts) => {
    const qty = quantities[product.id] || 1;
    if (qty < 1) {
      alert("Válassz legalább 1 darabot!");
      return;
    }
    if ((stockMap[product.id] ?? 0) < qty) {
      alert("Nincs elég raktárkészlet!");
      return;
    }
    try {
      await api.Orders.createOrder({
        items: [{ product_id: product.id, quantity: qty }]
      });

      await api.Warehouse.updateStock(product.id, WAREHOUSE_ID, -qty);
      alert("Megrendelés sikeres!");
      const res = await api.Warehouse.getStock(WAREHOUSE_ID);
      setStock(res.data);
      setQuantities(prev => ({ ...prev, [product.id]: 1 }));
    } catch (err) {
      console.error("Megrendelés hiba:", err);
      alert("Nem sikerült megrendelni a terméket vagy nincs készlet.");
    }
  };

  const rows = items.map(element => (
    <Table.Tr key={element.id}>
      <Table.Td>{element.product_name}</Table.Td>
      <Table.Td>{element.description}</Table.Td>
      <Table.Td>
        <Badge>
          <NumberFormatter value={element.price} suffix=" Ft" thousandSeparator={" "} />
        </Badge>
      </Table.Td>
      <Table.Td>
        {stockMap[element.id] ?? 0}
      </Table.Td>
      {role === 'User' && (
        <Table.Td>
          <NumberInput
            min={1}
            max={stockMap[element.id] ?? 0}
            value={quantities[element.id] ?? 1}
            onChange={val => handleQuantityChange(element.id, val)}
            disabled={(stockMap[element.id] ?? 0) === 0}
            style={{ width: 100, marginRight: 10 }}
          />
          <Button
            color="dark"
            disabled={(stockMap[element.id] ?? 0) < 1}
            onClick={() => handleOrder(element)}
          >
            Megrendelem
          </Button>
        </Table.Td>
      )}
      {(role === 'Admin' || role === 'Warehouse' ) && (
        <Table.Td>
          <Button onClick={() => navigate(`${element.id}`)} color="green">Módosítás</Button>
          <Button onClick={() => { api.Products.deleteProduct(`${element.id}`); }} color="red">Törlés</Button>
        </Table.Td>
      )}
    </Table.Tr>
  ));

  return (
    <div>
      {(role === 'Admin' || role === 'Warehouse' || role === 'Supplier' )&& (
        <Button onClick={() => navigate('add')}>Új Termék</Button>
      )}
      <Card shadow="sm" padding="lg" radius="md" withBorder>
        <Table>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Termék</Table.Th>
              <Table.Th>Leírás</Table.Th>
              <Table.Th>Ár</Table.Th>
              <Table.Th>Készlet</Table.Th>
              <Table.Th>Műveletek</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>{rows}</Table.Tbody>
        </Table>
      </Card>
    </div>
  );
};

export default Products;
