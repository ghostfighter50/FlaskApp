import { api } from "./api";
import { User } from "../types";

export const fetchUsers = async (): Promise<{ users: User[] }> => {
  const response = await api.get<{ users: User[] }>("/users");
  return response.data;
};

export const fetchUserById = async (userId: string): Promise<{ user: User }> => {
  const response = await api.get<{ user: User }>(`/users/${userId}`);
  return response.data;
};

export const updateUser = async (userId: string, userData: Partial<User>): Promise<{ message: string; user: User }> => {
  const response = await api.put<{ message: string; user: User }>(`/users/${userId}`, userData);
  return response.data;
};

export const deleteUser = async (userId: string): Promise<{ message: string }> => {
  const response = await api.delete<{ message: string }>(`/users/${userId}`);
  return response.data;
};


export const createUser = async (data: {email: string, name: string, role: "Professor" | "Student", password: string} ): Promise<{ message: string; user: User }> => {
  const response = await api.post<{ message: string; user: User }>(`/users`, data);
  return response.data;
}
