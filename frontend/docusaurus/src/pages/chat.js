import React from 'react';
import Layout from '@theme/Layout';
import Chatbot from '../components/Chatbot';
import AuthGuard from '../components/Auth/AuthGuard';

export default function ChatPage() {
  return (
    <Layout title="Chat" description="Textbook Assistant Chat">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--12">
            <AuthGuard requireAuth={true}>
              <Chatbot />
            </AuthGuard>
          </div>
        </div>
      </div>
    </Layout>
  );
}