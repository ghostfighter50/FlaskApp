  import { api } from "./api";
  import { Course } from "../types";

  export const fetchCourses = async (): Promise<{ courses: Course[] }> => {
    console.log(" Headers avant requête:", api.defaults.headers.common["Authorization"]); // ✅ Vérification du token
    const response = await api.get<{ courses: Course[] }>("/courses");
    return response.data;
  };


  export const fetchCourseById = async (courseId: string): Promise<{ course: Course }> => {
    const response = await api.get<{ course: Course }>(`/courses/${courseId}`);
    return response.data;
  };

  export const createCourse = async (courseData: { name: string }): Promise<{ message: string; course: Course }> => {
    const response = await api.post<{ message: string; course: Course }>("/courses", courseData);
    return response.data;
  };

  export const joinCourse = async (courseId: string): Promise<{ message: string }> => {
      const response = await api.post<{ message: string }>("/courses/join", { course_id: courseId });
      return response.data;
    };

    export const leaveCourse = async (courseId: string): Promise<{ message: string }> => {
      const response = await api.post<{ message: string }>("/courses/leave", { course_id: courseId });
      return response.data;
    };



  export const updateCourse = async (courseId: string, courseData: Partial<Course>): Promise<{ message: string; course: Course }> => {
    const response = await api.put<{ message: string; course: Course }>(`/courses/${courseId}`, courseData);
    return response.data;
  };

  export const deleteCourse = async (courseId: string): Promise<{ message: string }> => {
    const response = await api.delete<{ message: string }>(`/courses/${courseId}`);
    return response.data;
  };
