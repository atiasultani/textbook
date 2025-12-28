import React from 'react';
import Layout from '@theme/Layout';
import ForgotPassword from '../components/Auth/ForgotPassword';

export default function ForgotPasswordPage() {
  return (
    <Layout title="Forgot Password" description="Reset your password">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <ForgotPassword />
          </div>
        </div>
      </div>
    </Layout>
  );
}