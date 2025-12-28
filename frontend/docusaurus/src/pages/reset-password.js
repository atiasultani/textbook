import React from 'react';
import Layout from '@theme/Layout';
import ResetPassword from '../components/Auth/ResetPassword';

export default function ResetPasswordPage() {
  return (
    <Layout title="Reset Password" description="Enter your new password">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <ResetPassword />
          </div>
        </div>
      </div>
    </Layout>
  );
}