import { useState } from "react";
import { registerUser } from "../../services/authService";
import { UserRole } from "../../types"; // Import du type UserRole

const Register = () => {
  const [formData, setFormData] = useState<{ name: string; email: string; password: string; role: UserRole }>({
    name: "",
    email: "",
    password: "",
    role: "Student",
  });

  const [error, setError] = useState("");

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await registerUser(formData);
      alert("User registered successfully!");
    } catch {
      setError("Registration failed");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-bold mb-4">Register</h2>
        {error && <p className="text-red-500">{error}</p>}
        <form onSubmit={handleRegister}>
          <input type="text" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} className="w-full p-2 border rounded mb-3" required placeholder="Name" />
          <input type="email" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} className="w-full p-2 border rounded mb-3" required placeholder="Email" />
          <input type="password" value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} className="w-full p-2 border rounded mb-3" required placeholder="Password" />

          {/* Correction de la conversion du rôle */}
          <label htmlFor="role" className="block mb-2">Role</label>
          <select id="role" value={formData.role} onChange={(e) => setFormData({ ...formData, role: e.target.value as UserRole })} className="w-full p-2 border rounded mb-3">
            <option value="Student">Student</option>
            <option value="Professor">Professor</option>
            <option value="Administrator">Administrator</option>
          </select>

          <button className="w-full bg-green-500 text-white p-2 rounded">Register</button>
        </form>
      </div>
    </div>
  );
};

export default Register;
