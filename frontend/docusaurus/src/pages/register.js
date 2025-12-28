import React from 'react';
import Layout from '@theme/Layout';
import Register from '../components/Auth/Register';

export default function RegisterPage() {
  return (
    <Layout title="Register" description="Create a new account">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <Register />
          </div>
        </div>
      </div>
    </Layout>
  );
}