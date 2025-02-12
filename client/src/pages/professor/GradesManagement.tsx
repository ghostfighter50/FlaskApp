import { useEffect, useState } from "react";
import { fetchGrades, assignGrade, updateGrade } from "../../services/gradeService";
import { Grade } from "../../types";

const GradesManagement = () => {
  const [grades, setGrades] = useState<Grade[]>([]);
  const [newGrade, setNewGrade] = useState<number | null>(null);
  const [selectedGradeId, setSelectedGradeId] = useState<string | null>(null);
  const [newStudentId, setNewStudentId] = useState<string>("");
  const [newCourseId, setNewCourseId] = useState<string>("");
  const [newGradeName, setNewGradeName] = useState<string>("");

  useEffect(() => {
    fetchGrades().then((data) => setGrades(data.grades));
  }, []);

  const handleUpdateGrade = async () => {
    if (selectedGradeId && newGrade !== null) {
      await updateGrade(selectedGradeId, newGrade);
      alert("Grade updated successfully!");
      setNewGrade(null);
      setSelectedGradeId(null);
    }
  };

  const handleAssignGrade = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newStudentId && newCourseId && newGrade !== null && newGradeName) {
      await assignGrade({
        student_id: newStudentId,
        course_id: newCourseId,
        grade: newGrade,
        grade_name: newGradeName,
      });
      alert("Grade assigned successfully!");
      setNewStudentId("");
      setNewCourseId("");
      setNewGrade(null);
      setNewGradeName("");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Manage Grades</h1>

      {/* Formulaire d'attribution de note */}
      <h2 className="text-xl font-bold mt-6">Assign New Grade</h2>
      <form onSubmit={handleAssignGrade} className="mt-4 space-y-2">
        <input type="text" placeholder="Student ID" value={newStudentId} onChange={(e) => setNewStudentId(e.target.value)} className="border p-2 w-full" required />
        <input type="text" placeholder="Course ID" value={newCourseId} onChange={(e) => setNewCourseId(e.target.value)} className="border p-2 w-full" required />
        <input type="text" placeholder="Grade Name" value={newGradeName} onChange={(e) => setNewGradeName(e.target.value)} className="border p-2 w-full" required />
        <input type="number" placeholder="Grade" value={newGrade || ""} onChange={(e) => setNewGrade(parseFloat(e.target.value))} className="border p-2 w-full" required />
        <button type="submit" className="bg-blue-500 text-white p-2 rounded w-full">Assign Grade</button>
      </form>

      {/* Liste des notes existantes */}
      <h2 className="text-xl font-bold mt-6">Existing Grades</h2>
      <ul>
        {grades.map((grade) => (
          <li key={grade.id} className="p-2 border-b">
            {grade.grade_name}: {grade.grade} - Student ID: {grade.student_id}
            <button onClick={() => setSelectedGradeId(grade.id)} className="ml-4 bg-yellow-500 text-white px-2 py-1 rounded">Edit</button>
          </li>
        ))}
      </ul>

      {/* Formulaire de modification de note */}
      {selectedGradeId && (
        <div className="mt-4">
          <h2 className="text-xl font-bold">Update Grade</h2>
          <input type="number" placeholder="New Grade" value={newGrade || ""} onChange={(e) => setNewGrade(parseFloat(e.target.value))} className="border p-2 w-full" />
          <button onClick={handleUpdateGrade} className="bg-green-500 text-white p-2 mt-2 rounded w-full">Update</button>
        </div>
      )}
    </div>
  );
};

export default GradesManagement;
