import React from 'react';
import { Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface PrivateRouteProps {
    redirectPath?: string;
    allowedRoles?: ("Administrator" | "Professor" | "Student")[];
}

/**
 * A private route component that wraps around child routes. If the user is not authenticated,
 * they will be redirected to the specified login page.
 *
 * @param {PrivateRouteProps} props - Component properties.
 * @param {string} [props.redirectPath='/login'] - The path to redirect unauthenticated users.
 *
 * @returns {JSX.Element} Either the outlet for child routes if authenticated, or a navigation component to redirect.
 */
const PrivateRoute: React.FC<PrivateRouteProps> = ({
    redirectPath = '/login',
    allowedRoles = []
}) => {
    const { isAuthenticated, user} = useAuth();

    console.log(isAuthenticated);
    if (!isAuthenticated || (allowedRoles.length > 0 && !allowedRoles.includes(user.role))) {
        console.log('Redirecting to login page...');
        return window.location.href.replace(window.location.pathname, redirectPath);
    }
    return <Outlet />;
};

export default PrivateRoute;
