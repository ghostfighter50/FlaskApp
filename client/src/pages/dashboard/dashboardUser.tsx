// import { SetStateAction, useEffect, useState } from "react";
// import { fetchStudentGrades, fetchStudentCourses, fetchProfessors } from "../../services/userService";
// import { Grade, Course, Professor } from "../../types";
// import { useAuth } from "../../hooks/useAuth";

// const DashboardStudent = () => {
//     const { role } = useAuth();
//     const [grades, setGrades] = useState<Grade[]>([]);
//     const [courses, setCourses] = useState<Course[]>([]);
//     const [professors, setProfessors] = useState<Professor[]>([]);
//     const [error, setError] = useState<string | null>(null);

//     useEffect(() => {
//         if (role !== "Student") {
//             setError("Accès refusé. Ce tableau de bord est réservé aux étudiants.");
//             return;
//         }

//         fetchStudentGrades()
//             .then((response: { grades: SetStateAction<Grade[]>; }) => setGrades(response.grades))
//             .catch(() => setError("Impossible de charger les notes."));

//         fetchStudentCourses()
//             .then((response: { courses: SetStateAction<Course[]>; }) => setCourses(response.courses))
//             .catch(() => setError("Impossible de charger les cours."));

//         fetchProfessors()
//             .then((response: { professors: SetStateAction<Professor[]>; }) => setProfessors(response.professors))
//             .catch(() => setError("Impossible de charger les professeurs."));
//     }, [role]);

//     return (
//         <div className="p-6">
//             <h1 className="text-2xl font-bold mb-4">🎓 Dashboard Étudiant</h1>

//             {error && <p className="text-red-500">{error}</p>}

//             <h2 className="text-xl font-semibold mt-4">📚 Mes Matières</h2>
//             {courses.length > 0 ? (
//                 <ul className="list-disc pl-4">
//                     {courses.map((course) => (
//                         <li key={course.id} className="p-2 border-b">{course.name}</li>
//                     ))}
//                 </ul>
//             ) : (
//                 <p className="text-gray-500">Aucune matière disponible.</p>
//             )}

//             <h2 className="text-xl font-semibold mt-4">👨‍🏫 Mes Professeurs</h2>
//             {professors.length > 0 ? (
//                 <ul className="list-disc pl-4">
//                     {professors.map((prof) => (
//                         <li key={prof.id} className="p-2 border-b">{prof.name}</li>
//                     ))}
//                 </ul>
//             ) : (
//                 <p className="text-gray-500">Aucun professeur trouvé.</p>
//             )}

//             <h2 className="text-xl font-semibold mt-4">📊 Mes Notes</h2>
//             {grades.length > 0 ? (
//                 <table className="w-full border-collapse border border-gray-300 mt-2">
//                     <thead>
//                         <tr className="bg-gray-200">
//                             <th className="border p-2">Matière</th>
//                             <th className="border p-2">Note</th>
//                             <th className="border p-2">Évaluation</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         {grades.map((grade) => (
//                             <tr key={grade.id}>
//                                 <td className="border p-2">{grade.course_name}</td>
//                                 <td className="border p-2">{grade.grade}</td>
//                                 <td className="border p-2">{grade.grade_name}</td>
//                             </tr>
//                         ))}
//                     </tbody>
//                 </table>
//             ) : (
//                 <p className="text-gray-500">Aucune note disponible.</p>
//             )}
//         </div>
//     );
// };

// export default DashboardStudent;
