import { useState } from "react";
import { createCourse } from "../../services/courseService";

const CourseCreate = () => {
  const [courseName, setCourseName] = useState("");
  const [error, setError] = useState("");

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createCourse({ name: courseName });
      alert("Course created successfully!");
      setCourseName("");
    } catch {
      setError("Failed to create course");
    }
  };

  const handleClick = async () => {
    try {
      await createCourse({ name: courseName });
      alert("Course created successfully!");
      setCourseName("");
    } catch {
      setError("Failed to create course");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Create Course</h1>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleCreate} className="space-y-4">
        <input type="text" placeholder="Course Name" value={courseName} onChange={(e) => setCourseName(e.target.value)} className="border p-2 w-full" required />
        <button type="button" onClick={handleClick} className="bg-green-500 text-white p-2 rounded w-full">Create</button>
      </form>
    </div>
  );
};

export default CourseCreate;
