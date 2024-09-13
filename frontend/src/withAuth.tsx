import React from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function withAuth<P extends object>(WrappedComponent: React.ComponentType<P>) {
  return function WithAuth(props: P) {
    const navigate = useNavigate();

    useEffect(() => {
      const user = localStorage.getItem('user');
      if (!user) {
        navigate('/');
      }
    }, [navigate]);

    return <WrappedComponent {...props} />;
  };
}