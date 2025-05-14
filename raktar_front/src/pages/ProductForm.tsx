import { useParams } from "react-router-dom";
import { useForm } from "@mantine/form";
import { Button, Text, Group, TextInput, Card, Textarea, NumberInput } from '@mantine/core';
import api from '../api/api.ts';
import { useEffect } from "react";


interface IProductForm {
  isCreate: boolean;
}

const ProductForm = ({isCreate}: IProductForm) => {
  const {id} = useParams();
 

    const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      product_name: '',
      description: '',
      price: 0,

    },

    validate: {
      product_name: (value) => (value.length >=3) ? null : 'Legalább 3 karakter',
      description: (value) => (value.length >=3) ? null : 'Legalább 3 karakter',
      price: (value) => (value > 0 ? null : 'Az árnak nagyobbnak kell lennie mint 0'),
    },
  });

  useEffect(() => {
    if (!isCreate && id) {
      api.Products.getProduct(id).then(res => {
        form.setValues({
          product_name: res.data.product_name,
          description: res.data.description,
          price: res.data.price,
        });
      })
    }
  }, [id]);


  return <div>
  
      <Text>{isCreate ? "Új termék létrehozása" : "Termék módosítása"}</Text>


    {/* <p>{id}</p>
    <p>{JSON.stringify(isCreate)}</p> */}
    

    <Card>
      <form onSubmit={form.onSubmit((values) => {
        console.log(values)
        if (isCreate) { //létrehozás
          api.Products.createProduct({
            description: values.description,
            price: values.price,
            product_name: values.product_name
         }).then();
        } else { //módosítás
          api.Products.updateProduct(id!, {
            description: values.description,
            price: values.price,
            product_name: values.product_name}).then()
        }
      })}>

      <TextInput
        withAsterisk
        label="Név"
        placeholder="Termék neve"
        key={form.key('product_name')}
        {...form.getInputProps('product_name')}
      />
      <Textarea
        withAsterisk
        label="Leírás"
        placeholder="Termék leírása"
        key={form.key('description')}
        {...form.getInputProps('description')}
      />
      <NumberInput
        withAsterisk
        label="Ár"
        min={0}
        thousandSeparator=" "
        suffix=" Ft"
        clampBehavior="strict"
        placeholder="Termék ára"
        key={form.key('price')}
        {...form.getInputProps('price')}
      />

      {/* <Select
      label="Role"
      placeholder="Role TESZT!"
      data={['React', 'Angular', 'Vue', 'Svelte']}
      key={form.key('role')}
      {...form.getInputProps('role')}
    /> */}

      <Group justify="flex-end" mt="md">
        <Button type="submit">Küldés</Button>
      </Group>
    </form>
    </Card>

  </div>
}

export default ProductForm;