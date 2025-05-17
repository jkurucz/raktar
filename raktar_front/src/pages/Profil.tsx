

import { useEffect, useState } from "react";
import { Card, TextInput, Button, Text, Group, Stack } from "@mantine/core";
import api from "../api/api";
import { User, Address } from "../interfaces/IUsers";

const Profile = () => {
  const [user, setUser] = useState<User | null>(null);
  const [form, setForm] = useState<Partial<User>>({});
  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.Users.getMyProfile()
      .then((res) => {
        setUser(res.data);
        setForm({
          name: res.data.name,
          email: res.data.email,
          phone: res.data.phone,
          addresses: res.data.addresses?.length
            ? [{ ...res.data.addresses[0] }]
            : [{ country: "", city: "", street: "", postalcode: "" }]
        });
      })
      .catch(() => setError("Nem sikerült betölteni a profilt!"))
      .finally(() => setLoading(false));
  }, []);

  const handleInput = (field: keyof User, value: string) => {
    setForm({ ...form, [field]: value });
  };

  const handleAddressInput = (field: keyof Address, value: string) => {
    if (!form.addresses) return;
    const addresses = [...form.addresses];
    addresses[0] = { ...addresses[0], [field]: value };
    setForm({ ...form, addresses });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    try {
      await api.Users.updateMyProfile(form);
      setSuccess("A profilod sikeresen frissítve!");
    } catch {
      setError("Nem sikerült frissíteni a profilt.");
    }
  };

  if (loading) return <Text>Betöltés...</Text>;
  if (error) return <Text color="red">{error}</Text>;

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Text fz="xl" mb="md">Profilom</Text>
      <form onSubmit={handleSubmit}>
        <Stack gap="md">
          <TextInput
            label="Név"
            value={form.name ?? ""}
            onChange={(e) => handleInput("name", e.target.value)}
            required
          />
          <TextInput
            label="E-mail"
            value={form.email ?? ""}
            onChange={(e) => handleInput("email", e.target.value)}
            required
          />
          <TextInput
            label="Telefonszám"
            value={form.phone ?? ""}
            onChange={(e) => handleInput("phone", e.target.value)}
            required
          />
          {form.addresses && (
            <>
              <TextInput
                label="Ország"
                value={form.addresses[0]?.country ?? ""}
                onChange={(e) => handleAddressInput("country", e.target.value)}
                required
              />
              <TextInput
                label="Város"
                value={form.addresses[0]?.city ?? ""}
                onChange={(e) => handleAddressInput("city", e.target.value)}
                required
              />
              <TextInput
                label="Utca, házszám"
                value={form.addresses[0]?.street ?? ""}
                onChange={(e) => handleAddressInput("street", e.target.value)}
                required
              />
              <TextInput
                label="Irányítószám"
                value={form.addresses[0]?.postalcode ?? ""}
                onChange={(e) => handleAddressInput("postalcode", e.target.value)}
                required
              />
            </>
          )}
          <Text>
            <b>Szerepkör:</b> {user?.roles.map(r => r.name).join(", ")}
          </Text>
          <Group>
            <Button type="submit">Mentés</Button>
            {success && <Text color="green">{success}</Text>}
            {error && <Text color="red">{error}</Text>}
          </Group>
        </Stack>
      </form>
    </Card>
  );
};

export default Profile;
