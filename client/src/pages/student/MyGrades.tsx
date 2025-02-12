import { useEffect, useState } from "react";
import { fetchStudentGrades } from "../../services/gradeService";
import { Grade } from "../../types";

const MyGrades = () => {
  const [grades, setGrades] = useState<Grade[]>([]);
  const studentId = localStorage.getItem("userId") || "";

  useEffect(() => {
    fetchStudentGrades("course_id_placeholder", studentId).then((data) => setGrades(data.grades));
  }, [studentId]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">My Grades</h1>
      <ul>
        {grades.map((grade) => (
          <li key={grade.id} className="p-2 border-b">{grade.grade_name}: {grade.grade}</li>
        ))}
      </ul>
    </div>
  );
};

export default MyGrades;
