import { ReactNode } from "react";

export type UserRole = "Administrator" | "Professor" | "Student";

export interface User {
    id: string;
    name: string;
    email: string;
    role: UserRole;
}

export interface Course {
    id: string;
    name: string;
    professor_id: string;
}

export interface Grade {
    course_name: ReactNode;
    id: string;
    course_id: string;
    student_id: string;
    grade: number;
    grade_name: string;
}

export interface AuthResponse {
    access_token: string;
    user: User;
}

export interface APIError {
    error: string;
}
