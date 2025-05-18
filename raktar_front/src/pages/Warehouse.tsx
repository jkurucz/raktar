import { useEffect, useState } from "react";
import { Card, Table, Button, NumberInput, Select, Group, Text } from "@mantine/core";
import api from "../api/api";
import { IWarehouseStock } from "../interfaces/IWarehouseStock";
import { IWarehouse } from "../interfaces/IWarehouse";
import { IProducts } from "../interfaces/IProducts";

const Warehouse = () => {
  const [warehouses, setWarehouses] = useState<IWarehouse[]>([]);
  const [selectedWarehouse, setSelectedWarehouse] = useState<string | null>(null);
  const [stocks, setStocks] = useState<IWarehouseStock[]>([]);
  const [products, setProducts] = useState<IProducts[]>([]);
  const [editingStock, setEditingStock] = useState<number | null>(null);
  const [newQuantity, setNewQuantity] = useState<number | "">(0);

  // Betölti a raktárakat
  useEffect(() => {
    api.Warehouse.getWarehouses().then(res => setWarehouses(res.data));
    api.Products.getProducts().then(res => setProducts(res.data));
  }, []);

  // Ha raktárt váltunk, betölti a készletet
  useEffect(() => {
    if (selectedWarehouse) {
      api.Warehouse.getStock(Number(selectedWarehouse)).then(res => setStocks(res.data));
    }
  }, [selectedWarehouse]);

  // termék ID -> név
  const productMap = Object.fromEntries(products.map(p => [p.id, p.product_name]));

  const handleEdit = (stockId: number, quantity: number) => {
    setEditingStock(stockId);
    setNewQuantity(quantity);
  };

  const handleSave = (stock: IWarehouseStock) => {
    if (typeof newQuantity !== "number" || newQuantity < 0) {
      alert("A mennyiség nem lehet negatív!");
      return;
    }
    const diff = newQuantity - stock.quantity;
    if (stock.quantity + diff < 0) {
      alert("Készlet nem lehet 0 alatti!");
      return;
    }
    api.Warehouse.updateStock(stock.product_id, stock.warehouse_id, diff)
      .then(() => {
        // Frissítsd a készletlistát!
        api.Warehouse.getStock(stock.warehouse_id).then(res => setStocks(res.data));
        setEditingStock(null);
      });
  };

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Text fz="xl" mb="md">Raktárkészlet</Text>
      <Select
        label="Raktár"
        placeholder="Válassz raktárt"
        data={warehouses.map(w => ({ value: String(w.id), label: w.storage_location }))}
        value={selectedWarehouse}
        onChange={setSelectedWarehouse}
        mb="md"
      />
      {selectedWarehouse && (
        <Table>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Termék</Table.Th>
              <Table.Th>Darabszám</Table.Th>
              <Table.Th>Utolsó frissítés</Table.Th>
              <Table.Th>Művelet</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {stocks.map(stock => (
              <Table.Tr key={stock.id}>
                <Table.Td>{stock.product_name || productMap[stock.product_id]}</Table.Td>
                <Table.Td>
                  {editingStock === stock.id ? (
                    <NumberInput
                      value={newQuantity}
                      onChange={value => {
                        if (typeof value === "number" || value === "") {
                          setNewQuantity(value);
                        }
                      }}
                      min={0}
                    />
                  ) : (
                    stock.quantity
                  )}
                </Table.Td>
                <Table.Td>{new Date(stock.last_updated).toLocaleString()}</Table.Td>
                <Table.Td>
                  {editingStock === stock.id ? (
                    <Group>
                      <Button onClick={() => handleSave(stock)} size="xs" color="green">Mentés</Button>
                      <Button onClick={() => setEditingStock(null)} size="xs" color="gray">Mégse</Button>
                    </Group>
                  ) : (
                    <Button onClick={() => handleEdit(stock.id, stock.quantity)} size="xs">Módosít</Button>
                  )}
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      )}
    </Card>
  );
};

export default Warehouse;
