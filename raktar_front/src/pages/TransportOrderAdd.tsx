// import {
//   Card,
//   Text,
//   TextInput,
//   Button,
//   Group,
//   Select,
// } from "@mantine/core";
// import { useForm } from "@mantine/form";
// import { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";
// import api from "../api/api";
// import { ITranscomp } from "../interfaces/ITranscomp";
// import { Order } from "../interfaces/IOrders";

// const TransportOrderAdd = () => {
//   const [orders, setOrders] = useState<Order[]>([]);
//   const [transcomps, setTranscomps] = useState<ITranscomp[]>([]);
//   const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
//   const navigate = useNavigate();

//   const form = useForm({
//     initialValues: {
//       order_id: "",
//       transport_id: "",
//       load_date: "",
//       direction: "out",
//     },
//     validate: {
//       order_id: (value) => (value ? null : "Kötelező mező"),
//       transport_id: (value) => (value ? null : "Kötelező mező"),
//       load_date: (value) => (value ? null : "Kötelező mező"),
//     },
//   });

//   // useEffect(() => {
//   //   api.Orders.getUnassignedOrders().then((res) => {
//   //     setOrders(res.data);
//   //   });
  
//   //   api.Transcomp.getAll().then((res) => setTranscomps(res.data));
//   // }, []);

//   useEffect(() => {
//   api.Orders.getUnassignedOrders().then((res) => {
//     const options = res.data.map((order: any) => ({
//       value: String(order.id),
//       label: `#${order.id} - ${order.user_name}`,
//     }));
//     setAvailableOrders(options);
//   });

//   api.Transcomp.getAll().then((res) => setTranscomps(res.data));
// }, []);

//   const handleOrderSelect = (value: string | null) => {
//     if (value) {
//       form.setFieldValue("order_id", value);
//       // Ha szükséges, itt kérhetsz további adatokat a rendelésről
//     } else {
//       form.setFieldValue("order_id", "");
//     }
//   };

//   return (
//     <Card withBorder shadow="sm" p="lg">
//       <Text fz="xl" mb="md">
//         Új fuvarfeladat hozzáadása
//       </Text>
//       <form
//       onSubmit={form.onSubmit((values) => {
//         api.TransportOrders.assignTransport(Number(values.order_id), {
//           transport_id: Number(values.transport_id),
//           status: "assigned",
//           load_date: new Date(values.load_date).toISOString()
//         }).then(() => {
//           navigate("/app/transport");
//         }).catch((err) => {
//           console.error("Mentés hiba:", err);
//           alert("Nem sikerült menteni a fuvarfeladatot.");
//         });
//       })}
//       >
//         <Select
//           label="Megrendelés kiválasztása"
//           placeholder="Válassz egy megrendelést"
//           data={orders.map((o) => ({ value: String(o.id), label: `#${o.id}` }))}
//           {...form.getInputProps("order_id")}
//           onChange={(value) => handleOrderSelect(value)}
//         />

//         {selectedOrder && (
//           <>
//             <Text mt="xs" size="sm">
//               Név: {selectedOrder.user_name}
//             </Text>
//             <Text size="sm">
//               Cím: {selectedOrder.user_address}
//             </Text>
//           </>
//         )}

//         <Select
//           mt="md"
//           label="Szállító kiválasztása"
//           placeholder="Válassz fuvarozót"
//           data={transcomps.map((tc) => ({
//             value: String(tc.id),
//             label: `${tc.company} - ${tc.truck}`,
//           }))}
//           {...form.getInputProps("transport_id")}
//         />

//         <TextInput
//           mt="md"
//           type="date"
//           label="Rakodás dátuma"
//           {...form.getInputProps("load_date")}
//         />

//         <Group justify="flex-end" mt="md">
//           <Button type="submit">Mentés</Button>
//         </Group>
//       </form>
//     </Card>
//   );
// };

// export default TransportOrderAdd;


import {
  Card,
  Text,
  TextInput,
  Button,
  Group,
  Select,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { ITranscomp } from "../interfaces/ITranscomp";
import { Order } from "../interfaces/IOrders";

const TransportOrderAdd = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [transcomps, setTranscomps] = useState<ITranscomp[]>([]);
  const navigate = useNavigate();

  const form = useForm({
    initialValues: {
      order_id: "",
      transport_id: "",
      load_date: "",
    },
    validate: {
      order_id: (value) => (value ? null : "Kötelező mező"),
      transport_id: (value) => (value ? null : "Kötelező mező"),
      load_date: (value) => (value ? null : "Kötelező mező"),
    },
  });

  useEffect(() => {
    api.Orders.getUnassignedOrders().then((res) => {
      setOrders(res.data);
    });

    api.Transcomp.getAll().then((res) => setTranscomps(res.data));
  }, []);

  return (
    <Card withBorder shadow="sm" p="lg">
      <Text fz="xl" mb="md">
        Új fuvarfeladat hozzáadása
      </Text>
      <form
        onSubmit={form.onSubmit((values) => {
        api.TransportOrders.create({
          order_id: Number(values.order_id),
          transport_id: Number(values.transport_id),
          load_date: values.load_date + "T00:00:00",
          direction: "outbound"
        })
    .then(() => navigate("/app/transport"))
    .catch((err) => {
      console.error("Mentés hiba:", err);
      alert("Nem sikerült menteni a fuvarfeladatot.");
    });
})}
      >
        <Select
          label="Megrendelés kiválasztása"
          placeholder="Válassz egy megrendelést"
          data={orders.map((o) => ({ value: String(o.id), label: `#${o.id}` }))}
          {...form.getInputProps("order_id")}
        />

        <Select
          mt="md"
          label="Szállító kiválasztása"
          placeholder="Válassz fuvarozót"
          data={transcomps.map((tc) => ({
            value: String(tc.id),
            label: `${tc.company} - ${tc.truck}`,
          }))}
          {...form.getInputProps("transport_id")}
        />

        <TextInput
          mt="md"
          type="date"
          label="Rakodás dátuma"
          {...form.getInputProps("load_date")}
        />

        <Group justify="flex-end" mt="md">
          <Button type="submit">Mentés</Button>
        </Group>
      </form>
    </Card>
  );
};

export default TransportOrderAdd;
