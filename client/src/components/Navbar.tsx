import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token"); // Suppression du token d'authentification
    localStorage.removeItem("userId"); // Suppression de l'ID utilisateur
    navigate("/auth/login");
  };

  return (
    <nav className="bg-gray-800 text-white py-4 px-6 flex justify-between items-center shadow-md">
      {/* Logo et titre */}
      <div className="flex items-center cursor-pointer" onClick={() => navigate("/home")}>
        <h1 className="text-2xl font-bold">University Portal</h1>
      </div>

      {/* Liens de navigation */}
      <div className="hidden md:flex space-x-6">
        <button onClick={() => navigate("/home")} className="hover:text-gray-300 transition">Home</button>
        <button onClick={() => navigate("/student/courses")} className="hover:text-gray-300 transition">Courses</button>
        <button onClick={() => navigate("/profile")} className="hover:text-gray-300 transition">Profile</button>
        <button onClick={() => navigate("/admin/users")} className="hover:text-gray-300 transition">Users</button>
      </div>

      {/* Bouton Logout */}
      <button onClick={handleLogout} className="bg-red-500 px-4 py-2 rounded hover:bg-red-600 transition">
        Logout
      </button>
    </nav>
  );
};

export default Navbar;
