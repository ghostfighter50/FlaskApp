import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchCourseById } from "../../services/courseService";
import { fetchStudentGrades } from "../../services/gradeService";
import { leaveCourse } from "../../services/courseService";
import { Course, Grade } from "../../types";

const StudentCourseDetails = () => {
  const { course_id } = useParams<{ course_id: string }>(); // Récupération de l'ID du cours depuis l'URL
  const navigate = useNavigate();
  const studentId = localStorage.getItem("userId") || "";
  const [course, setCourse] = useState<Course | null>(null);
  const [grades, setGrades] = useState<Grade[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (course_id) {
      fetchCourseById(course_id)
        .then((data) => setCourse(data.course))
        .catch(() => setError("Failed to load course details"));

      fetchStudentGrades(course_id, studentId)
        .then((data) => setGrades(data.grades))
        .catch(() => setError("Failed to load grades"));
    }
  }, [course_id, studentId]);

  const handleLeaveCourse = async () => {
    const confirmLeave = window.confirm("Are you sure you want to leave this course?");
    if (confirmLeave && course_id) {
      try {
        await leaveCourse(course_id);
        alert("You have left the course successfully!");
        navigate("/student/courses");
      } catch {
        setError("Failed to leave the course.");
      }
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Course Details</h1>

      {error && <p className="text-red-500">{error}</p>}

      {course ? (
        <div className="mt-4 p-4 border rounded shadow-lg">
          <p><strong>Course Name:</strong> {course.name}</p>
          <p><strong>Professor ID:</strong> {course.professor_id}</p>

          {/* Notes de l'étudiant */}
          <h2 className="text-xl font-bold mt-6">My Grades</h2>
          {grades.length > 0 ? (
            <ul>
              {grades.map((grade) => (
                <li key={grade.id} className="p-2 border-b">
                  {grade.grade_name}: {grade.grade}
                </li>
              ))}
            </ul>
          ) : (
            <p>No grades available for this course.</p>
          )}

          {/* Bouton quitter le cours */}
          <button onClick={handleLeaveCourse} className="bg-red-500 text-white px-4 py-2 mt-4 rounded">
            Leave Course
          </button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default StudentCourseDetails;
