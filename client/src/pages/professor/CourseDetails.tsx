import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchCourseById, updateCourse, deleteCourse } from "../../services/courseService";
import { Course } from "../../types";

const CourseDetails = () => {
  const { course_id } = useParams<{ course_id: string }>(); // Récupération de l'ID du cours depuis l'URL
  const navigate = useNavigate();

  const [course, setCourse] = useState<Course | null>(null);
  const [editMode, setEditMode] = useState(false);
  const [updatedName, setUpdatedName] = useState("");

  useEffect(() => {
    if (course_id) {
      fetchCourseById(course_id).then((data) => {
        setCourse(data.course);
        setUpdatedName(data.course.name);
      });
    }
  }, [course_id]);

  const handleUpdate = async () => {
    if (course) {
      await updateCourse(course.id, { name: updatedName });
      alert("Course updated successfully!");
      setEditMode(false);
      setCourse({ ...course, name: updatedName });
    }
  };

  const handleDelete = async () => {
    if (course) {
      const confirmDelete = window.confirm("Are you sure you want to delete this course?");
      if (confirmDelete) {
        await deleteCourse(course.id);
        alert("Course deleted successfully!");
        navigate("/professor/courses"); // Redirection après suppression
      }
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Course Details</h1>

      {course ? (
        <div className="mt-4 p-4 border rounded shadow-lg">
          <p><strong>Course Name:</strong> {course.name}</p>
          <p><strong>Professor ID:</strong> {course.professor_id}</p>

          {editMode ? (
            <div className="mt-4">
              <input
                type="text"
                placeholder="New Course Name"
                value={updatedName}
                onChange={(e) => setUpdatedName(e.target.value)}
                className="border p-2 w-full mb-2"
              />
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

export default CourseDetails;
