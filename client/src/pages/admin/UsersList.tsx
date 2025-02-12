import { useEffect, useState } from "react";
import { fetchUsers } from "../../services/userService";
import { User } from "../../types";

const UsersList = () => {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    fetchUsers().then((data) => setUsers(data.users));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Users List</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id} className="p-2 border-b">{user.name} - {user.email} - {user.role}</li>
        ))}
      </ul>
    </div>
  );
};

export default UsersList;
