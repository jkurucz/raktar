import {
  Stack,
  TextInput,
  PasswordInput,
  Group,
  Button,
  Text
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useNavigate } from "react-router-dom";
import AuthContainer from "../components/AuthContainer";
import api from "../api/api"; 

const Register = () => {
  const navigate = useNavigate();

  const form = useForm({
    initialValues: {
      email: '',
      name: '',
      password: '',
      phone: '',
      city: '',
      country: '',
      postalcode: '',
      street: '',
    },

    validate: {
      email: (val) => (/^\S+@\S+$/.test(val) ? null : 'Érvénytelen e-mail cím'),
      name: (val) => (val.length < 2 ? 'A név túl rövid' : null),
      password: (val) => (val.length < 6 ? 'A jelszónak legalább 6 karakter hosszúnak kell lennie' : null),
      phone: (val) => (val.length < 7 ? 'Nem érvényes telefonszám' : null),
      city: (val) => (!val ? 'Város megadása kötelező' : null),
      country: (val) => (!val ? 'Ország megadása kötelező' : null),
      postalcode: (val) => (!val ? 'Irányítószám megadása kötelező' : null),
      street: (val) => (!val ? 'Utca megadása kötelező' : null),
    },
  });

  const submit = () => {
    const values = form.values;

    api.Registrate.registrate(
      values.email,
      values.name,
      values.password,
      values.phone,
      {
        city: values.city,
        country: values.country,
        postalcode: values.postalcode,
        street: values.street,
      }
    ).then(() => {
      navigate("/"); // Sikeres regisztráció után navigálás pl. login oldalra
    }).catch((err) => {
      console.error("Regisztrációs hiba:", err);
      // Itt adhatsz hozzá hibakezelést, toast üzenetet stb.
    });
  };

  return (
    <AuthContainer>
      <div>
        <Text>Regisztráció</Text><br />
        <form onSubmit={form.onSubmit(submit)}>
          <Stack>

            <TextInput
              required
              label="Email"
              placeholder="user@example.com"
              key={form.key('email')}
              {...form.getInputProps('email')}
            />

            <TextInput
              required
              label="Név"
              placeholder="Teljes név"
              key={form.key('name')}
              {...form.getInputProps('name')}
            />

            <PasswordInput
              required
              label="Jelszó"
              placeholder="Minimum 6 karakter"
              key={form.key('password')}
              {...form.getInputProps('password')}
            />

            <TextInput
              required
              label="Telefonszám"
              placeholder="+36..."
              key={form.key('phone')}
              {...form.getInputProps('phone')}
            />

            <TextInput
              required
              label="Város"
              placeholder="Budapest"
              key={form.key('city')}
              {...form.getInputProps('city')}
            />

            <TextInput
              required
              label="Ország"
              placeholder="Magyarország"
              key={form.key('country')}
              {...form.getInputProps('country')}
            />

            <TextInput
              required
              label="Irányítószám"
              placeholder="1111"
              key={form.key('postalcode')}
              {...form.getInputProps('postalcode')}
            />

            <TextInput
              required
              label="Utca"
              placeholder="Fő utca 1."
              key={form.key('street')}
              {...form.getInputProps('street')}
            />
          </Stack>

          <Group justify="flex-end" mt="xl">
            <Button type="submit" radius="xl">
              Regisztráció
            </Button>
          </Group>
        </form>
      </div>
    </AuthContainer>
  );
};

export default Register;
