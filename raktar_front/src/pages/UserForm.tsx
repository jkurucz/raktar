import { useParams, useNavigate } from "react-router-dom";
import { useForm } from "@mantine/form";
import {
  Button,
  Card,
  Group,
  Text,
  TextInput,
  Select
} from "@mantine/core";
import { useEffect, useState } from "react";
import api from "../api/api";
import { Address } from "../interfaces/IUsers.ts";

interface IUserForm {
  isCreate?: boolean; 
}


const UserForm = ({ isCreate }: IUserForm) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [roleOptions, setRoleOptions] = useState<{ value: string; label: string }[]>([]);

  const form = useForm({
    initialValues: {
      name: '',
      email: '',
      phone: '',
      city: '',
      street: '',
      postalcode: '',
      country: '',
      role: ''
    },

    validate: {
      name: (value) => value.length >= 3 ? null : "A név túl rövid",
      email: (value) => /^\S+@\S+$/.test(value) ? null : "Érvénytelen e-mail cím",
      phone: (value) => value.length >= 6 ? null : "Nem érvényes telefonszám",
    }
  });

  useEffect(() => {
    // Szerepkörök betöltése
    api.Users.getRoles().then(res => {
      const mapped = res.data.map((r: { name: string }) => ({
        value: r.name,
        label: r.name
      }));
      setRoleOptions(mapped);
    });

    // Felhasználó adatainak betöltése
    if (!isCreate && id) {
      api.Users.getUserById(id).then(res => {
        const user = res.data;
        const addr = user.addresses?.[0] || {} as Address;
//        const addr = user.addresses || {} as Address;

        const roleName = user.roles?.[0]?.name || '';
       

        form.setValues({
          name: user.name,
          email: user.email,
          phone: user.phone || '',
          city: addr.city || '',
          street: addr.street || '',
          postalcode: addr.postalcode || '',
          country: addr.country || '',
          role: roleName
        
        });
      });
    }
  }, [id]);


  const handleSubmit = (values: typeof form.values) => {
  const updateObj = {
    name: values.name,
    email: values.email,
    phone: values.phone,
    addresses: [
        {
          city: values.city,
          street: values.street,
          postalcode: values.postalcode,
          country: values.country
        }
    ],
    roles: [values.role]
  };

  api.Users.safeUpdateUser(id!, updateObj).then(() => {
    // alert("Sikeres módosítás!");
    navigate('/app/users');
  }).catch(err => {
    console.log("updateObj", updateObj);
    console.error("Hiba a módosítás során:", err);
    alert("Nem sikerült a mentés.");
  });  
};
 

  return (
    <div>
      <Text mb="md">Felhasználó adatainak módosítása</Text>
      <Card withBorder>
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <TextInput
            label="Név"
            withAsterisk
            {...form.getInputProps('name')}
          />
          <TextInput
            label="Email"
            withAsterisk
            {...form.getInputProps('email')}
          />
          <TextInput
            label="Telefonszám"
            {...form.getInputProps('phone')}
          />
          <TextInput
            label="Város"
            {...form.getInputProps('city')}
          />
          <TextInput
            label="Utca"
            {...form.getInputProps('street')}
          />
          <TextInput
            label="Irányítószám"
            {...form.getInputProps('postalcode')}
          />
          <TextInput
            label="Ország"
            {...form.getInputProps('country')}
          />
          <Select
            label="Szerepkör"
            data={roleOptions}
            {...form.getInputProps('role')}
          />

          <Group justify="flex-end" mt="md">
            <Button type="submit">Mentés</Button>
          </Group>
        </form>
      </Card>
    </div>
  );
};

export default UserForm;