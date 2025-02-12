import { api } from "./api";
import { Grade } from "../types";

export const fetchGrades = async (): Promise<{ grades: Grade[] }> => {
  const response = await api.get<{ grades: Grade[] }>("/grades");
  return response.data;
};

export const fetchGradeById = async (gradeId: string): Promise<{ grade: Grade }> => {
  const response = await api.get<{ grade: Grade }>(`/grades/${gradeId}`);
  return response.data;
};

export const fetchStudentGrades = async (courseId: string, studentId: string): Promise<{ grades: Grade[] }> => {
    const response = await api.get<{ grades: Grade[] }>(`/grades/courses/${courseId}/students/${studentId}/grades`);
    return response.data;
  };

export const assignGrade = async (gradeData: { course_id: string; student_id: string; grade: number; grade_name: string }): Promise<{ message: string; grade: Grade }> => {
  const response = await api.post<{ message: string; grade: Grade }>("/grades", gradeData);
  return response.data;
};

export const updateGrade = async (gradeId: string, newGrade: number): Promise<{ message: string; grade: Grade }> => {
  const response = await api.put<{ message: string; grade: Grade }>(`/grades/${gradeId}`, { grade: newGrade });
  return response.data;
};

export const deleteGrade = async (gradeId: string): Promise<{ message: string }> => {
  const response = await api.delete<{ message: string }>(`/grades/${gradeId}`);
  return response.data;
};
