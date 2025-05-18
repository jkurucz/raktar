import { Button, Card, Text, Textarea } from "@mantine/core";
import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/api";

const ComplaintForm = () => {
  const { orderId } = useParams();
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (!message.trim()) {
      setError("A panasz szövege nem lehet üres!");
      return;
    }
    try {
      await api.Complaints.createComplaint(Number(orderId), message);
      setSuccess("A panasz sikeresen elküldve.");
      setTimeout(() => navigate(-1), 1200); 
    } catch (err) {
      setError("Hiba a panasz küldésekor.");
    }
  };

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Text fz="xl" mb="md">Panasz beküldése</Text>
      <form onSubmit={handleSubmit}>
        <Textarea
          required
          label="Panasz leírása"
          minRows={4}
          value={message}
          onChange={e => setMessage(e.currentTarget.value)}
        />
        {error && <Text color="red" mt="sm">{error}</Text>}
        {success && <Text color="green" mt="sm">{success}</Text>}
        <Button type="submit" mt="md" color="red">Küldés</Button>
      </form>
      <Button mt="sm" variant="outline" onClick={() => navigate(-1)}>
        Mégse
      </Button>
    </Card>
  );
};

export default ComplaintForm;
