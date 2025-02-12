import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchUserById, updateUser, deleteUser } from "../../services/userService";
import { User, UserRole } from "../../types";

const UserDetails = () => {
  const { user_id } = useParams<{ user_id: string }>(); // Récupération de l'ID depuis l'URL
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [editMode, setEditMode] = useState(false);
  const [updatedData, setUpdatedData] = useState<Partial<User>>({});

  useEffect(() => {
    if (user_id) {
      fetchUserById(user_id).then((data) => setUser(data.user));
    }
  }, [user_id]);

  const handleUpdate = async () => {
    if (user) {
      await updateUser(user.id, updatedData);
      alert("User updated successfully!");
      setEditMode(false);
      setUser({ ...user, ...updatedData });
    }
  };

  const handleDelete = async () => {
    if (user) {
      const confirmDelete = window.confirm("Are you sure you want to delete this user?");
      if (confirmDelete) {
        await deleteUser(user.id);
        alert("User deleted successfully!");
        navigate("/admin/users"); // Redirection après suppression
      }
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">User Details</h1>

      {user ? (
        <div className="mt-4 p-4 border rounded shadow-lg">
          <p><strong>Name:</strong> {user.name}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Role:</strong> {user.role}</p>

          {editMode ? (
            <div className="mt-4">
              <input
                type="text"
                placeholder="New Name"
                defaultValue={user.name}
                onChange={(e) => setUpdatedData({ ...updatedData, name: e.target.value })}
                className="border p-2 w-full mb-2"
              />
              <input
                type="email"
                placeholder="New Email"
                defaultValue={user.email}
                onChange={(e) => setUpdatedData({ ...updatedData, email: e.target.value })}
                className="border p-2 w-full mb-2"
              />
              <label htmlFor="user-role" className="block mb-2">Role</label>
              <select
                id="user-role"
                defaultValue={user.role}
                onChange={(e) => setUpdatedData({ ...updatedData, role: e.target.value as UserRole })}
                className="border p-2 w-full mb-2"
              >
                <option value="Student">Student</option>
                <option value="Professor">Professor</option>
                <option value="Administrator">Administrator</option>
              </select>
              <button onClick={handleUpdate} className="bg-green-500 text-white px-4 py-2 rounded mr-2">
                Save
              </button>
              <button onClick={() => setEditMode(false)} className="bg-gray-500 text-white px-4 py-2 rounded">
                Cancel
              </button>
            </div>
          ) : (
            <div className="mt-4">
              <button onClick={() => setEditMode(true)} className="bg-blue-500 text-white px-4 py-2 rounded mr-2">
                Edit
              </button>
              <button onClick={handleDelete} className="bg-red-500 text-white px-4 py-2 rounded">
                Delete
              </button>
            </div>
          )}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default UserDetails;
