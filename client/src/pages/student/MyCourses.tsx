import { useEffect, useState } from "react";
import { fetchCourses } from "../../services/courseService";
import { Course } from "../../types";

const MyCourses = () => {
  const [courses, setCourses] = useState<Course[]>([]);

  useEffect(() => {
    fetchCourses().then((data) => setCourses(data.courses));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">My Courses</h1>
      <ul>
        {courses.map((course) => (
          <li key={course.id} className="p-2 border-b">{course.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default MyCourses;
