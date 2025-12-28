import React from 'react';
import Layout from '@theme/Layout';
import Login from '../components/Auth/Login';

export default function LoginPage() {
  return (
    <Layout title="Login" description="Sign in to your account">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <Login />
          </div>
        </div>
      </div>
    </Layout>
  );
}