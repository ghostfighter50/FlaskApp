import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./providers/authProvider";
import PrivateRoute from "./routes/privateRoute";
import Home from "./pages/home";
import Login from "./pages/auth/login";
import Profile from "./pages/profile/profile";
import UsersList from "./pages/admin/UsersList";
import UserDetails from "./pages/admin/UserDetails";
import CoursesList from "./pages/professor/courseList";
import CourseDetails from "./pages/professor/CourseDetails";
import GradesManagement from "./pages/professor/GradesManagement";
import Dashboard from "./pages/dashboard/dashboard";

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          <Route path="/auth/login" element={<Login />} />

          {/* Private routes available to all authenticated users */}
          <Route
            element={
              <PrivateRoute
                allowedRoles={["Administrator", "Professor", "Student"]}
                redirectPath="/auth/login"
              />
            }
          >
            <Route path="/profile" element={<Profile />} />
          </Route>

          {/* Administrator */}
          <Route
            element={
              <PrivateRoute allowedRoles={["Administrator"]} redirectPath="/auth/login" />
            }
          >
            <Route path="/users" element={<UsersList />} />
            <Route path="/users/:id" element={<UserDetails />} />
          </Route>

          <Route
            element={
              <PrivateRoute allowedRoles={["Professor", "Administrator", "Student"]} redirectPath="/auth/login" />
            }
          >
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/courses" element={<CoursesList />} />
            <Route path="/courses/:id" element={<CourseDetails />} />
            <Route
              path="/courses/:id/grades"
              element={<GradesManagement />}
            />
          </Route>


          {/* Fallback for unknown routes could be added here */}
          <Route path="*" element={<div>404 Not Found</div>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
