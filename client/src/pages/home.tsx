import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="flex h-screen">
      {/* Barre latérale */}

      {/* Contenu principal */}
      <div className="flex flex-col flex-1">
        {/* Barre de navigation */}
        <Navbar />

        {/* Section principale */}
        <div className="p-6">
          <h1 className="text-3xl font-bold mb-4">Welcome to University Portal</h1>
          <p className="text-gray-700 mb-6">
            Manage courses, students, and professors efficiently. Select an option below to get started.
          </p>

          {/* Boutons pour rediriger vers les sections */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 border rounded shadow-lg bg-white">
              <h2 className="text-xl font-bold">Authentication</h2>
              <p className="text-gray-600">Register, login, and manage user authentication.</p>
              <button onClick={() => navigate("/auth/login")} className="mt-4 bg-blue-500 text-white px-4 py-2 rounded">
                Login
              </button>
              or
              <button onClick={() => navigate("/auth/register")} className="mt-4 bg-blue-500 text-white px-4 py-2 rounded">
                Register
              </button>
            </div>

            <div className="p-6 border rounded shadow-lg bg-white">
              <h2 className="text-xl font-bold">Courses</h2>
              <p className="text-gray-600">View and manage courses, enroll or create new ones.</p>
              <button onClick={() => navigate("/student/courses")} className="mt-4 bg-green-500 text-white px-4 py-2 rounded">
                View Courses
              </button>
            </div>

            <div className="p-6 border rounded shadow-lg bg-white">
              <h2 className="text-xl font-bold">Users</h2>
              <p className="text-gray-600">Manage students, professors, and administrators.</p>
              <button onClick={() => navigate("/admin/users")} className="mt-4 bg-yellow-500 text-white px-4 py-2 rounded">
                Manage Users
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
