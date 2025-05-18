export interface Role {
  id: number;
  name: string;
}

export interface Address {
  city: string;
  country: string;
  postalcode: string;
  street: string;
}

export interface User {
  id: number;
  email: string;
  phone: string;
  name: string;
  token?: string;
  addresses?: Address[];
  roles: Role[];
}

export interface SafeUpdateUserRequest {
  name?: string;
  email?: string;
  phone?: string;
  address?: Address;
  roles?: string[]; 
}
