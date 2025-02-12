import { useState } from "react";
import { joinCourse } from "../../services/courseService";

const JoinCourse = () => {
  const [courseId, setCourseId] = useState("");
  const [error, setError] = useState("");

  const handleJoin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await joinCourse(courseId);
      alert("Joined course successfully!");
      setCourseId("");
    } catch {
      setError("Failed to join course");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Join Course</h1>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleJoin} className="space-y-4">
        <input type="text" placeholder="Course ID" value={courseId} onChange={(e) => setCourseId(e.target.value)} className="border p-2 w-full" required />
        <button className="bg-blue-500 text-white p-2 rounded w-full">Join</button>
      </form>
    </div>
  );
};

export default JoinCourse;
