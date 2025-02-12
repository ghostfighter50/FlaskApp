// Dashboard.tsx
import React, { useState, useEffect, useCallback } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

// ---------- Services ----------
import {
  fetchCourses,
  createCourse,
  updateCourse,
  deleteCourse,
  joinCourse,
  leaveCourse,
} from "../../services/courseService";

import {
  fetchGrades,
  assignGrade,
  updateGrade,
  deleteGrade,
} from "../../services/gradeService";

import {
  fetchUsers,
  createUser,
  updateUser,
  deleteUser,
} from "../../services/userService";

// ---------- Types ----------
import { Course, Grade, User, UserRole } from "../../types";

// We extend Course to include optional properties for professor/student views.
type ExtendedCourse = Course & { students?: User[]; isEnrolled?: boolean };

// ---------- Helper ----------
const getErrorMessage = (error: unknown): string =>
  error instanceof Error ? error.message : "An unknown error occurred.";

// ---------------------
// Modal Component
// ---------------------
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}
const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
        <div className="flex items-center justify-between border-b pb-2 mb-4">
          <h3 className="text-xl font-semibold">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
            aria-label="Close modal"
          >
            &times;
          </button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
};

// ---------------------
// Grade Modal Component (for Professor/Admin edit)
interface GradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  gradeData: { gradeName: string; gradeValue: number };
  onSave: (gradeName: string, gradeValue: number) => void;
  onDelete?: () => void;
}
const GradeModal: React.FC<GradeModalProps> = ({
  isOpen,
  onClose,
  gradeData,
  onSave,
  onDelete,
}) => {
  const [gradeName, setGradeName] = useState(gradeData.gradeName);
  const [gradeValue, setGradeValue] = useState(gradeData.gradeValue);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setGradeName(gradeData.gradeName);
    setGradeValue(gradeData.gradeValue);
    setError(null);
  }, [gradeData, isOpen]);

  const handleSave = () => {
    if (!gradeName.trim() || isNaN(gradeValue)) {
      setError("Please enter a valid grade name and a numeric grade value.");
      return;
    }
    onSave(gradeName, gradeValue);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Edit Grade">
      <div className="space-y-4">
        <div>
          <label htmlFor="gradeName" className="block text-sm font-medium text-gray-700">
            Grade Name
          </label>
          <input
            id="gradeName"
            type="text"
            value={gradeName}
            onChange={(e) => setGradeName(e.target.value)}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
            placeholder="e.g. Midterm"
          />
        </div>
        <div>
          <label htmlFor="gradeValue" className="block text-sm font-medium text-gray-700">
            Grade
          </label>
          <input
            id="gradeValue"
            type="number"
            value={gradeValue}
            onChange={(e) => setGradeValue(parseFloat(e.target.value))}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
            placeholder="e.g. 85"
          />
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <div className="flex justify-end space-x-3">
          <button onClick={handleSave} className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
            Save
          </button>
          {onDelete && (
            <button onClick={onDelete} className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
              Delete
            </button>
          )}
          <button onClick={onClose} className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded">
            Cancel
          </button>
        </div>
      </div>
    </Modal>
  );
};

// ---------------------
// Admin Grade Creation Modal (for admin to assign a new grade)
interface AdminGradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  courses: ExtendedCourse[];
  users: User[];
  onSave: (courseId: string, studentId: string, gradeName: string, gradeValue: number) => void;
}
const AdminGradeModal: React.FC<AdminGradeModalProps> = ({
  isOpen,
  onClose,
  courses,
  users,
  onSave,
}) => {
  const [selectedCourseId, setSelectedCourseId] = useState<string>("");
  const [selectedStudentId, setSelectedStudentId] = useState<string>("");
  const [gradeName, setGradeName] = useState("");
  const [gradeValue, setGradeValue] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  const handleSave = () => {
    if (!selectedCourseId || !selectedStudentId || !gradeName.trim() || isNaN(gradeValue)) {
      setError("All fields are required and grade must be numeric.");
      return;
    }
    onSave(selectedCourseId, selectedStudentId, gradeName, gradeValue);
  };

  useEffect(() => {
    setSelectedCourseId("");
    setSelectedStudentId("");
    setGradeName("");
    setGradeValue(0);
    setError(null);
  }, [isOpen]);

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Assign Grade">
      <div className="space-y-4">
        <div>
          <label htmlFor="selectCourse" className="block text-sm font-medium text-gray-700">
            Course
          </label>
          <select
            id="selectCourse"
            title="Select course"
            value={selectedCourseId}
            onChange={(e) => setSelectedCourseId(e.target.value)}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
          >
            <option value="">Select a course</option>
            {courses?.filter(Boolean).map((course) => (
              <option key={course.id} value={course.id}>
                {course.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="selectStudent" className="block text-sm font-medium text-gray-700">
            Student
          </label>
          <select
            id="selectStudent"
            title="Select student"
            value={selectedStudentId}
            onChange={(e) => setSelectedStudentId(e.target.value)}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
          >
            <option value="">Select a student</option>
            {users?.filter(Boolean).map((user) => (
              <option key={user.id} value={user.id}>
                {user.name} ({user.email})
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="adminGradeName" className="block text-sm font-medium text-gray-700">
            Grade Name
          </label>
          <input
            id="adminGradeName"
            type="text"
            value={gradeName}
            onChange={(e) => setGradeName(e.target.value)}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
            placeholder="e.g. Final Exam"
          />
        </div>
        <div>
          <label htmlFor="adminGradeValue" className="block text-sm font-medium text-gray-700">
            Grade
          </label>
          <input
            id="adminGradeValue"
            type="number"
            value={gradeValue}
            onChange={(e) => setGradeValue(parseFloat(e.target.value))}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
            placeholder="e.g. 90"
          />
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <div className="flex justify-end space-x-3">
          <button onClick={handleSave} className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
            Save
          </button>
          <button onClick={onClose} className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded">
            Cancel
          </button>
        </div>
      </div>
    </Modal>
  );
};

// ---------------------
// Dashboard Main Component
const DashboardMain: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/auth/login" replace />;
  if (user.role === "Administrator") return <AdminView />;
  if (user.role === "Professor") return <ProfessorView />;
  if (user.role === "Student") return <StudentView />;
  return <div className="p-8 text-center">Role not recognized.</div>;
};

// ---------------------
// Admin View Component
const AdminView: React.FC = () => {
  // Tabs: courses, users, grades
  const [activeTab, setActiveTab] = useState<"courses" | "users" | "grades">("courses");

  // Courses state
  const [courses, setCourses] = useState<Course[]>([]);
  const [loadingCourses, setLoadingCourses] = useState(false);
  const [errorCourses, setErrorCourses] = useState<string | null>(null);

  // Users state
  const [users, setUsers] = useState<User[]>([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [errorUsers, setErrorUsers] = useState<string | null>(null);

  // Grades state (for admin)
  const [adminGrades, setAdminGrades] = useState<Grade[]>([]);
  const [loadingGrades, setLoadingGrades] = useState(false);
  const [errorGrades, setErrorGrades] = useState<string | null>(null);

  // Course modal state
  const [isCourseModalOpen, setCourseModalOpen] = useState(false);
  const [courseModalData, setCourseModalData] = useState<{ id?: string; name: string }>({ name: "" });
  const [courseModalError, setCourseModalError] = useState<string | null>(null);

  // User modal state
  const [isUserModalOpen, setUserModalOpen] = useState(false);
  const [userModalData, setUserModalData] = useState<Partial<User & { password?: string }>>({});
  const [userModalError, setUserModalError] = useState<string | null>(null);

  // Admin grade modal state
  const [isAdminGradeModalOpen, setAdminGradeModalOpen] = useState(false);
  const [selectedGrade, setSelectedGrade] = useState<Grade | undefined>(undefined);

  // Load functions (using useCallback for dependencies)
  const loadCourses = useCallback(async () => {
    setLoadingCourses(true);
    setErrorCourses(null);
    try {
      const res = await fetchCourses();
      setCourses(Array.isArray(res.courses) ? res.courses : []);
    } catch (err) {
      setErrorCourses(getErrorMessage(err));
    } finally {
      setLoadingCourses(false);
    }
  }, []);

  const loadUsers = useCallback(async () => {
    setLoadingUsers(true);
    setErrorUsers(null);
    try {
      const res = await fetchUsers();
      setUsers(Array.isArray(res.users) ? res.users : []);
    } catch (err) {
      setErrorUsers(getErrorMessage(err));
    } finally {
      setLoadingUsers(false);
    }
  }, []);

  const loadAdminGrades = useCallback(async () => {
    setLoadingGrades(true);
    setErrorGrades(null);
    try {
      const res = await fetchGrades();
      setAdminGrades(Array.isArray(res.grades) ? res.grades : []);
    } catch (err) {
      setErrorGrades(getErrorMessage(err));
    } finally {
      setLoadingGrades(false);
    }
  }, []);

  useEffect(() => {
    if (activeTab === "courses") {
      loadCourses();
    } else if (activeTab === "users") {
      loadUsers();
    } else if (activeTab === "grades") {
      loadAdminGrades();
    }
  }, [activeTab, loadCourses, loadUsers, loadAdminGrades]);

  // ----- Course Modal Handlers -----
  const openCreateCourseModal = () => {
    setCourseModalData({ name: "" });
    setCourseModalError(null);
    setCourseModalOpen(true);
  };

  const openEditCourseModal = (course: Course) => {
    setCourseModalData({ id: course.id, name: course.name });
    setCourseModalError(null);
    setCourseModalOpen(true);
  };

  const handleCourseModalSave = async () => {
    if (!courseModalData.name.trim()) {
      setCourseModalError("Course name cannot be empty.");
      return;
    }
    try {
      if (courseModalData.id) {
        const res = await updateCourse(courseModalData.id, { name: courseModalData.name });
        setCourses((prev) =>
          prev.map((c) => (c.id === res.course.id ? res.course : c))
        );
      } else {
        const res = await createCourse({ name: courseModalData.name });
        setCourses((prev) => [...prev, res.course]);
      }
      setCourseModalOpen(false);
    } catch (err) {
      setCourseModalError(getErrorMessage(err));
    }
  };

  // ----- User Modal Handlers -----
  const openCreateUserModal = () => {
    setUserModalData({ name: "", email: "", role: "Professor", password: "" });
    setUserModalError(null);
    setUserModalOpen(true);
  };

  const openEditUserModal = (user: User) => {
    setUserModalData({ ...user });
    setUserModalError(null);
    setUserModalOpen(true);
  };

  const handleUserModalSave = async () => {
    if (!userModalData.name?.trim() || !userModalData.email?.trim()) {
      setUserModalError("Name and email cannot be empty.");
      return;
    }
    if (!userModalData.id) {
      if (!userModalData.password?.trim()) {
        setUserModalError("Password cannot be empty.");
        return;
      }
      if (userModalData.role === "Administrator") {
        setUserModalError("Cannot create an admin user.");
        return;
      }
      try {
        const res = await createUser({
          name: userModalData.name,
          email: userModalData.email,
          role: userModalData.role as "Professor" | "Student",
          password: userModalData.password as string,
        });
        setUsers((prev) => [...prev, res.user]);
        setUserModalOpen(false);
      } catch (err) {
        setUserModalError(getErrorMessage(err));
      }
    } else {
      try {
        const res = await updateUser(userModalData.id, { role: userModalData.role! });
        setUsers((prev) =>
          prev.map((u) => (u.id === res.user.id ? res.user : u))
        );
        setUserModalOpen(false);
      } catch (err) {
        setUserModalError(getErrorMessage(err));
      }
    }
  };

  const openCreateGradeModalAdmin = () => {
    setSelectedGrade(undefined);
    setAdminGradeModalOpen(true);
  };

  const handleAdminGradeSave = async (
    courseId: string,
    studentId: string,
    gradeName: string,
    gradeValue: number
  ) => {
    try {
      if (selectedGrade) {
        const res = await updateGrade(selectedGrade.id, gradeValue);
        setAdminGrades((prev) =>
          prev.map((g) => (g.id === res.grade.id ? res.grade : g))
        );
      } else {
        const res = await assignGrade({ course_id: courseId, student_id: studentId, grade: gradeValue, grade_name: gradeName });
        setAdminGrades((prev) => [...prev, res.grade]);
      }
      setAdminGradeModalOpen(false);
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  const handleGradeDeleteAdmin = async (gradeId: string) => {
    if (!window.confirm("Are you sure you want to delete this grade?")) return;
    try {
      await deleteGrade(gradeId);
      setAdminGrades((prev) => prev.filter((g) => g.id !== gradeId));
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
      <div className="flex space-x-4 mb-6 border-b pb-2">
        {(["courses", "users", "grades"] as const).map((tab) => (
          <button
            key={tab}
            className={`px-4 py-2 font-medium ${
              activeTab === tab
                ? "text-blue-600 border-b-2 border-blue-600"
                : "text-gray-600 hover:text-blue-600"
            }`}
            onClick={() => setActiveTab(tab)}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {activeTab === "courses" && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold">Manage Courses</h2>
            <button
              onClick={openCreateCourseModal}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
            >
              Create Course
            </button>
          </div>
          {loadingCourses ? (
            <p>Loading courses...</p>
          ) : errorCourses ? (
            <p className="text-red-500">{errorCourses}</p>
          ) : (
            <ul className="divide-y divide-gray-200">
              {courses.filter(Boolean).map((course) => (
                <li key={course.id} className="py-3 flex justify-between items-center">
                  <span>{course.name}</span>
                  <div className="space-x-2">
                    <button
                      onClick={() => openEditCourseModal(course)}
                      className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => {
                        if (window.confirm("Are you sure you want to delete this course?")) {
                          deleteCourse(course.id)
                            .then(() => loadCourses())
                            .catch((err) => alert(getErrorMessage(err)));
                        }
                      }}
                      className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {activeTab === "users" && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold">Manage Users</h2>
            <button
              onClick={openCreateUserModal}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
            >
              Create User
            </button>
          </div>
          {loadingUsers ? (
            <p>Loading users...</p>
          ) : errorUsers ? (
            <p className="text-red-500">{errorUsers}</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Email
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Role
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {users.filter(Boolean).map((u) => (
                    <tr key={u.id}>
                      <td className="px-6 py-4 whitespace-nowrap">{u.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{u.email}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{u.role}</td>
                      <td className="px-6 py-4 whitespace-nowrap space-x-2">
                        <button
                          onClick={() => openEditUserModal(u)}
                          className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => {
                            if (window.confirm("Are you sure you want to delete this user?")) {
                              deleteUser(u.id)
                                .then(() => loadUsers())
                                .catch((err) => alert(getErrorMessage(err)));
                            }
                          }}
                          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {activeTab === "grades" && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold">Manage Grades</h2>
            <button
              onClick={openCreateGradeModalAdmin}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
            >
              Create Grade
            </button>
          </div>
          {loadingGrades ? (
            <p>Loading grades...</p>
          ) : errorGrades ? (
            <p className="text-red-500">{errorGrades}</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Course
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Student
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Grade Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Grade
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {adminGrades.filter(Boolean).map((g) => {
                    const courseName = courses.find((c) => c.id === g.course_id)?.name || g.course_id;
                    const studentName = users.find((u) => u.id === g.student_id)?.name || g.student_id;
                    return (
                      <tr key={g.id}>
                        <td className="px-6 py-4 whitespace-nowrap">{courseName}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{studentName}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{g.grade_name}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{g.grade}</td>
                        <td className="px-6 py-4 whitespace-nowrap space-x-2">
                          <button
                            onClick={() => {
                              setSelectedGrade(g);
                              setAdminGradeModalOpen(true);
                            }}
                            className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => {
                              if (window.confirm("Are you sure you want to delete this grade?")) {
                                handleGradeDeleteAdmin(g.id);
                              }
                            }}
                            className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Course Modal */}
      <Modal
        isOpen={isCourseModalOpen}
        onClose={() => setCourseModalOpen(false)}
        title={courseModalData.id ? "Edit Course" : "Create Course"}
      >
        <div className="space-y-4">
          <label htmlFor="courseName" className="block text-sm font-medium text-gray-700">
            Course Name
          </label>
          <input
            id="courseName"
            type="text"
            value={courseModalData.name}
            onChange={(e) => setCourseModalData({ ...courseModalData, name: e.target.value })}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
            placeholder="Enter course name"
          />
          {courseModalError && <p className="text-red-500 text-sm mt-1">{courseModalError}</p>}
          <div className="flex justify-end space-x-3">
            <button onClick={handleCourseModalSave} className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
              Save
            </button>
            <button onClick={() => setCourseModalOpen(false)} className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded">
              Cancel
            </button>
          </div>
        </div>
      </Modal>

      {/* User Modal */}
      <Modal
        isOpen={isUserModalOpen}
        onClose={() => setUserModalOpen(false)}
        title={userModalData && userModalData.id ? "Edit User" : "Create User"}
      >
        {userModalData && (
          <div className="space-y-4">
            {!userModalData.id ? (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Name</label>
                  <input
                    type="text"
                    value={userModalData.name || ""}
                    onChange={(e) => setUserModalData({ ...userModalData, name: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                    placeholder="User Name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    type="email"
                    value={userModalData.email || ""}
                    onChange={(e) => setUserModalData({ ...userModalData, email: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                    placeholder="Email"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Password</label>
                  <input
                    type="password"
                    value={userModalData.password || ""}
                    onChange={(e) => setUserModalData({ ...userModalData, password: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                    placeholder="Password"
                  />
                </div>
                <div>
                  <label htmlFor="userRole" className="block text-sm font-medium text-gray-700">
                    Role
                  </label>
                  <select
                    id="userRole"
                    title="Select role"
                    value={userModalData.role}
                    onChange={(e) =>
                      setUserModalData({ ...userModalData, role: e.target.value as UserRole })
                    }
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                  >
                    <option value="Professor">Professor</option>
                    <option value="Student">Student</option>
                  </select>
                </div>
              </>
            ) : (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Name</label>
                  <input
                    type="text"
                    value={userModalData.name || ""}
                    readOnly
                    className="mt-1 block w-full rounded-md border border-gray-300 bg-gray-100 px-3 py-2"
                    placeholder="User Name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    type="text"
                    value={userModalData.email || ""}
                    readOnly
                    className="mt-1 block w-full rounded-md border border-gray-300 bg-gray-100 px-3 py-2"
                    placeholder="Email"
                  />
                </div>
                <div>
                  <label htmlFor="editUserRole" className="block text-sm font-medium text-gray-700">
                    Role
                  </label>
                  {userModalData.role === "Administrator" ? (
                    <input
                      title="Role"
                      type="text"
                      value="Administrator"
                      readOnly
                      className="mt-1 block w-full rounded-md border border-gray-300 bg-gray-100 px-3 py-2"
                    />
                  ) : (
                    <select
                      id="editUserRole"
                      title="Select role"
                      value={userModalData.role}
                      onChange={(e) =>
                        setUserModalData({ ...userModalData, role: e.target.value as UserRole })
                      }
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                    >
                      <option value="Professor">Professor</option>
                      <option value="Student">Student</option>
                    </select>
                  )}
                </div>
              </>
            )}
            {userModalError && <p className="text-red-500 text-sm">{userModalError}</p>}
            <div className="flex justify-end space-x-3">
              <button
                onClick={handleUserModalSave}
                className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
              >
                Save
              </button>
              <button
                onClick={() => setUserModalOpen(false)}
                className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </Modal>

      {/* Admin Grade Modal (Creation) */}
      <AdminGradeModal
        isOpen={isAdminGradeModalOpen && !selectedGrade}
        onClose={() => setAdminGradeModalOpen(false)}
        courses={courses?.filter(Boolean) as ExtendedCourse[]}
        users={users?.filter(Boolean)}
        onSave={handleAdminGradeSave}
      />

      {/* Admin Grade Modal (Editing) */}
      {selectedGrade && (
        <GradeModal
          isOpen={isAdminGradeModalOpen && Boolean(selectedGrade)}
          onClose={() => setAdminGradeModalOpen(false)}
          gradeData={{
            gradeName: selectedGrade.grade_name,
            gradeValue: selectedGrade.grade,
          }}
          onSave={(name, value) =>
            handleAdminGradeSave(selectedGrade.course_id, selectedGrade.student_id, name, value)
          }
          onDelete={() => handleGradeDeleteAdmin(selectedGrade.id)}
        />
      )}
    </div>
  );
};

// ---------------------
// Professor View Component
const ProfessorView: React.FC = () => {
  const [courses, setCourses] = useState<ExtendedCourse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Grade management state
  const [courseGrades, setCourseGrades] = useState<Grade[]>([]);
  const [isGradeModalOpen, setGradeModalOpen] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState<User | null>(null);
  const [selectedGrade, setSelectedGrade] = useState<Grade | undefined>(undefined);

  const loadCourses = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchCourses();
      setCourses(Array.isArray(res.courses) ? (res.courses as ExtendedCourse[]) : []);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const loadCourseGrades = async (courseId: string) => {
    try {
      const res = await fetchGrades();
      setCourseGrades(Array.isArray(res.grades) ? res.grades.filter((g) => g.course_id === courseId) : []);
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  useEffect(() => {
    loadCourses();
  }, []);

  const openManageGrades = async (course: ExtendedCourse) => {
    await loadCourseGrades(course.id);
  };

  const openGradeModal = (student: User) => {
    const grade = courseGrades.find((g) => g.student_id === student.id);
    setSelectedStudent(student);
    setSelectedGrade(grade);
    setGradeModalOpen(true);
  };

  const handleGradeSave = async (gradeName: string, gradeValue: number) => {
    if (!selectedStudent) return;
    try {
      if (selectedGrade) {
        const res = await updateGrade(selectedGrade.id, gradeValue);
        setCourseGrades((prev) =>
          prev.map((g) => (g.id === res.grade.id ? res.grade : g))
        );
      } else {
        if (courses.length === 0) return;
        // Assume the first course is the one being managed (adjust as needed)
        const courseId = courses[0].id;
        const res = await assignGrade({
          course_id: courseId,
          student_id: selectedStudent.id,
          grade: gradeValue,
          grade_name: gradeName,
        });
        setCourseGrades((prev) => [...prev, res.grade]);
      }
      setGradeModalOpen(false);
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  const handleGradeDelete = async () => {
    if (!selectedGrade) return;
    if (!window.confirm("Are you sure you want to delete this grade?")) return;
    try {
      await deleteGrade(selectedGrade.id);
      setCourseGrades((prev) => prev.filter((g) => g.id !== selectedGrade.id));
      setGradeModalOpen(false);
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Professor Dashboard</h1>
      {loading ? (
        <p>Loading courses...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <div className="space-y-6">
          {courses.filter(Boolean).map((course) => (
            <div key={course.id} className="border p-4 rounded-md">
              <div className="flex justify-between items-center mb-2">
                <h2 className="text-2xl font-semibold">{course.name}</h2>
                <button
                  onClick={() => openManageGrades(course)}
                  className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
                >
                  Manage Grades
                </button>
              </div>
              {course.students && course.students.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 uppercase">
                          Student
                        </th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 uppercase">
                          Grade
                        </th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 uppercase">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {course.students.map((student: User) => {
                        const grade = courseGrades.find((g) => g.student_id === student.id);
                        return (
                          <tr key={student.id}>
                            <td className="px-4 py-2 whitespace-nowrap">{student.name}</td>
                            <td className="px-4 py-2 whitespace-nowrap">
                              {grade ? `${grade.grade_name}: ${grade.grade}` : "No grade"}
                            </td>
                            <td className="px-4 py-2 whitespace-nowrap">
                              <button
                                onClick={() => openGradeModal(student)}
                                className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                              >
                                {grade ? "Edit Grade" : "Assign Grade"}
                              </button>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p>No students enrolled in this course.</p>
              )}
            </div>
          ))}
        </div>
      )}
      {selectedStudent && (
        <GradeModal
          isOpen={isGradeModalOpen}
          onClose={() => setGradeModalOpen(false)}
          gradeData={{
            gradeName: selectedGrade ? selectedGrade.grade_name : "",
            gradeValue: selectedGrade ? selectedGrade.grade : 0,
          }}
          onSave={handleGradeSave}
          onDelete={selectedGrade ? handleGradeDelete : undefined}
        />
      )}
    </div>
  );
};

// ---------------------
// Student View Component
const StudentView: React.FC = () => {
  const { user } = useAuth();
  const [courses, setCourses] = useState<ExtendedCourse[]>([]);
  const [grades, setGrades] = useState<Grade[]>([]);
  const [loadingCourses, setLoadingCourses] = useState(false);
  const [errorCourses, setErrorCourses] = useState<string | null>(null);
  const [loadingGrades, setLoadingGrades] = useState(false);
  const [errorGrades, setErrorGrades] = useState<string | null>(null);

  const loadCourses = async () => {
    setLoadingCourses(true);
    setErrorCourses(null);
    try {
      const res = await fetchCourses();
      setCourses(Array.isArray(res.courses) ? (res.courses as ExtendedCourse[]) : []);
    } catch (err) {
      setErrorCourses(getErrorMessage(err));
    } finally {
      setLoadingCourses(false);
    }
  };

  const loadGrades = async () => {
    setLoadingGrades(true);
    setErrorGrades(null);
    try {
      const res = await fetchGrades();
      setGrades(
        Array.isArray(res.grades)
          ? res.grades.filter((g) => g.student_id === user.id)
          : []
      );
    } catch (err) {
      setErrorGrades(getErrorMessage(err));
    } finally {
      setLoadingGrades(false);
    }
  };

  useEffect(() => {
    loadCourses();
    loadGrades();
  });

  const handleJoinCourse = async (courseId: string) => {
    try {
      await joinCourse(courseId);
      loadCourses();
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  const handleLeaveCourse = async (courseId: string) => {
    try {
      await leaveCourse(courseId);
      loadCourses();
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Student Dashboard</h1>
      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-2">Courses</h2>
        {loadingCourses ? (
          <p>Loading courses...</p>
        ) : errorCourses ? (
          <p className="text-red-500">{errorCourses}</p>
        ) : (
          <ul className="divide-y divide-gray-200">
            {courses.filter(Boolean).map((course) => (
              <li key={course.id} className="py-3 flex justify-between items-center">
                <span>{course.name}</span>
                <div>
                  {course.isEnrolled ? (
                    <button
                      onClick={() => handleLeaveCourse(course.id)}
                      className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                    >
                      Leave
                    </button>
                  ) : (
                    <button
                      onClick={() => handleJoinCourse(course.id)}
                      className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded"
                    >
                      Join
                    </button>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
      <div>
        <h2 className="text-2xl font-semibold mb-2">Your Grades</h2>
        {loadingGrades ? (
          <p>Loading grades...</p>
        ) : errorGrades ? (
          <p className="text-red-500">{errorGrades}</p>
        ) : (
          <ul className="divide-y divide-gray-200">
            {grades.filter(Boolean).map((grade) => (
              <li key={grade.id} className="py-3">
                {grade.grade_name}: {grade.grade}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default DashboardMain;
