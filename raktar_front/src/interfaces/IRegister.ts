export interface Address {
  city: string;
  country: string;
  postalcode: string;
  street: string;
}

export interface RegistrationData {
  email: string;
  name: string;
  password: string;
  phone: string;
  address: Address;
}