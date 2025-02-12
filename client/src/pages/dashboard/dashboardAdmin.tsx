import { useEffect, useState } from "react";
import { fetchCourses } from "../../services/courseService";
import { Course } from "../../types";

const DashboardAdministrator = () => {
  const [error, setError] = useState<string | null>(null);
  const [courses, setCourses] = useState<Course[]>([]);

  useEffect(() => {
    fetchCourses()
      .then((response) => {
        console.log("📡 Réponse API:", response);
        setCourses(response.courses);
      })
      .catch((err) => {
        console.error("❌ Erreur API:", err);
        setError("Impossible de charger les cours.");
      });
  }, []);

  console.log(error)
  console.log(courses)

  return (
    <p>ADMIN</p>
  );
};

export default DashboardAdministrator;
