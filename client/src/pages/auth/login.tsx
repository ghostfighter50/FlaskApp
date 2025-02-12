import { useState } from "react";
import { login } from "../../services/authService";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { setAuthToken } from "../../services/api";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { setIsAuthenticated, setUser } = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await login(email, password);
      console.log("Token reçu:", response.access_token);
      setIsAuthenticated(response.access_token !== null);
      setUser(response.user);
      setAuthToken(response.access_token);
      console.log("Token stocké:", localStorage.getItem("token"));
        navigate("/dashboard");

    } catch (error) {
      console.error("Login error:", error);
      setError("Invalid credentials");
    }
  };

  return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <div className="bg-white p-6 rounded-lg shadow-lg w-96">
          <h2 className="text-2xl font-bold mb-4">Login</h2>
          {error && <p className="text-red-500">{error}</p>}
          <form onSubmit={handleLogin}>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full p-2 border rounded mb-3" required placeholder="Email" />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full p-2 border rounded mb-3" required placeholder="Password" />
            <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">Login</button>
          </form>
        </div>
      </div>
  );
};

export default Login;
