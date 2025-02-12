import { api } from "./api";
import { AuthResponse } from "../types";

/**
 * Logs in a user with the provided email and password.
 * @param {string} email - The email of the user.
 * @param {string} password - The password of the user.
 * @returns {Promise<AuthResponse>} A promise that resolves to an authentication response.
 */
export const login = async (email: string, password: string): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>("/auth/login", { email, password });
  return response.data;
};

/**
 * Registers a new user.
 * @param {object} userData - An object containing the user's name, email, password, and role.
 * @param {string} userData.name - The name of the user.
 * @param {string} userData.email - The email of the user.
 * @param {string} userData.password - The password of the user.
 * @param {string} userData.role - The role of the user.
 * @returns {Promise<{ message: string; id: string }>} A promise that resolves to an object containing a message and the user's ID.
 */
export const registerUser = async (userData: { name: string; email: string; password: string; role: "Administrator" | "Professor" | "Student" }): Promise<{ message: string; id: string }> => {
  const response = await api.post<{ message: string; id: string }>("/auth/register", userData);
  return response.data;
};

/**
 * Changes the password for a given user.
 * @param {string} email - The email of the user.
 * @param {string} password - The current password of the user.
 * @param {string} newPassword - The new password for the user.
 * @returns {Promise<{ message: string }>} A promise that resolves to an object containing a message.
 */
export const changePassword = async (email: string, password: string, newPassword: string): Promise<{ message: string }> => {
  const response = await api.post<{ message: string }>("/auth/change-password", { email, password, new_password: newPassword });
  return response.data;
};
