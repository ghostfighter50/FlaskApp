import axios from "axios";

const API_URL = "http://127.0.0.1:5000/api/v1";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

export const setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    console.log("Token ajouté aux headers:", api.defaults.headers.common["Authorization"]);
  } else {
    delete api.defaults.headers.common["Authorization"];
    console.log("Aucun token trouvé, suppression de l'en-tête Authorization");
  }
};
