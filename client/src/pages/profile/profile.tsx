import { useEffect, useState } from "react";
import { fetchUserById, updateUser } from "../../services/userService";
import { User } from "../../types";
import { useAuth } from "../../hooks/useAuth";

const Profile = () => {
  const [editing, setEditing] = useState(false);
  const [updatedData, setUpdatedData] = useState<Partial<User>>({});
  const { user, setUser } = useAuth();

  useEffect(() => {
    if (user?.id) {
      fetchUserById(user.id).then((data) => setUser(data.user));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleUpdate = async () => {
    if (user) {
      await updateUser(user.id, updatedData);
      setUser({ ...user, ...updatedData });
      setEditing(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 to-indigo-100 p-4">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Profile</h1>
        {user ? (
          <div>
            <div className="mb-4">
              <p className="mb-2">
                <span className="font-semibold text-gray-700">Name:</span>{" "}
                <span className="text-gray-600">{user.name}</span>
              </p>
              <p className="mb-2">
                <span className="font-semibold text-gray-700">Email:</span>{" "}
                <span className="text-gray-600">{user.email}</span>
              </p>
              <p>
                <span className="font-semibold text-gray-700">Role:</span>{" "}
                <span className="text-gray-600">{user.role}</span>
              </p>
            </div>

            {editing ? (
              <div className="space-y-4">
                <input
                  type="text"
                  placeholder="New name"
                  onChange={(e) =>
                    setUpdatedData({ ...updatedData, name: e.target.value })
                  }
                  className="w-full border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
                <input
                  type="email"
                  placeholder="New email"
                  onChange={(e) =>
                    setUpdatedData({ ...updatedData, email: e.target.value })
                  }
                  className="w-full border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
                <button
                  onClick={handleUpdate}
                  className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-2 rounded transition duration-200"
                >
                  Save Changes
                </button>
                <button
                  onClick={() => setEditing(false)}
                  className="w-full bg-red-500 hover:bg-red-600 text-white font-semibold py-2 rounded transition duration-200"
                >
                  Cancel
                </button>
              </div>
            ) : (
              <button
                onClick={() => setEditing(true)}
                className="w-full mt-4 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded transition duration-200"
              >
                Edit Profile
              </button>
            )}
          </div>
        ) : (
          <p className="text-center text-gray-600">Loading...</p>
        )}
      </div>
    </div>
  );
};

export default Profile;
