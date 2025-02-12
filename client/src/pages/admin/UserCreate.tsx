import { useState } from "react";
import { registerUser } from "../../services/authService";
import { UserRole } from "../../types"; // On importe UserRole

const UserCreate = () => {
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
      alert("User created successfully!");
    } catch {
      setError("Creation failed");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Create User</h1>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleRegister} className="space-y-4">
        <input type="text" placeholder="Name" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} className="border p-2 w-full" required />
        <input type="email" placeholder="Email" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} className="border p-2 w-full" required />
        <input type="password" placeholder="Password" value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} className="border p-2 w-full" required />
        <label htmlFor="role" className="block text-sm font-medium text-gray-700">Role</label>
        <select id="role" value={formData.role} onChange={(e) => setFormData({ ...formData, role: e.target.value as UserRole })} className="border p-2 w-full">
          <option value="Student">Student</option>
          <option value="Professor">Professor</option>
          <option value="Administrator">Administrator</option>
        </select>
        <button className="bg-green-500 text-white p-2 rounded w-full">Create</button>
      </form>
    </div>
  );
};

export default UserCreate;
