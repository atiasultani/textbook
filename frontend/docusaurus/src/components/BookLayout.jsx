import React, { useState } from 'react';
import { useLocation } from '@docusaurus/router';
import Link from '@docusaurus/Link';
import clsx from 'clsx';
import AuthGuard from './Auth/AuthGuard';
import './BookLayout.css';

const BookLayout = ({ children, title, description }) => {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Define the book structure
  const bookStructure = [
    {
      id: 'intro',
      title: 'Introduction',
      path: '/docs/intro',
      chapters: []
    },
    {
      id: 'intro-physical-ai',
      title: 'Module 1: Introduction to Physical AI',
      path: '/docs/intro-physical-ai/intro',
      chapters: [
        { title: 'Chapter 1: Foundations', path: '/docs/intro-physical-ai/chapter1-foundations' },
        { title: 'Chapter 2: Practical Applications', path: '/docs/intro-physical-ai/chapter2-practical-applications' },
        { title: 'Chapter 3: Advanced Concepts', path: '/docs/intro-physical-ai/chapter3-advanced-concepts' },
        { title: 'Introduction', path: '/docs/intro-physical-ai/intro' }
      ]
    },
    {
      id: 'basics-humanoid-robotics',
      title: 'Module 2: Humanoid Robotics Fundamentals',
      path: '/docs/basics-humanoid-robotics/intro',
      chapters: [
        { title: 'ROS 2 Fundamentals', path: '/docs/ros-2-fundamentals/intro' },
        { title: 'Core Concepts', path: '/docs/ros-2-fundamentals/chapter1-core-concepts' },
        { title: 'Advanced Development', path: '/docs/ros-2-fundamentals/chapter2-advanced-development' },
        { title: 'Ecosystem Integration', path: '/docs/ros-2-fundamentals/chapter3-ecosystem-integration' },
        { title: 'Introduction', path: '/docs/basics-humanoid-robotics/intro' }
      ]
    },
    {
      id: 'digital-twin-simulation',
      title: 'Module 3: Advanced Systems',
      path: '/docs/digital-twin-simulation/intro',
      chapters: [
        { title: 'Digital Twin Simulation', path: '/docs/digital-twin-simulation/intro' },
        { title: 'Vision-Language-Action Systems', path: '/docs/vision-language-action/intro' }
      ]
    },
    {
      id: 'capstone',
      title: 'Module 4: Capstone Project',
      path: '/docs/capstone/intro',
      chapters: [
        { title: 'Capstone Project', path: '/docs/capstone/intro' }
      ]
    }
  ];

  // Find current chapter and module
  const currentChapter = bookStructure.flatMap(module => [
    { ...module, isModuleIntro: true },
    ...module.chapters.map(chapter => ({
      ...module,
      ...chapter,
      isModuleIntro: false
    }))
  ]).find(item => location.pathname === item.path);

  // Get previous and next chapters
  const allChapters = bookStructure.flatMap(module => [
    { ...module, isModuleIntro: true },
    ...module.chapters.map(chapter => ({
      ...module,
      ...chapter,
      isModuleIntro: false
    }))
  ]);

  const currentIndex = allChapters.findIndex(item => location.pathname === item.path);
  const prevChapter = currentIndex > 0 ? allChapters[currentIndex - 1] : null;
  const nextChapter = currentIndex < allChapters.length - 1 ? allChapters[currentIndex + 1] : null;

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  return (
    <AuthGuard requireAuth={true}>
      <div className="book-layout">
        {/* Mobile sidebar toggle button */}
        <button
          className="book-sidebar-toggle"
          onClick={toggleSidebar}
          aria-label="Toggle navigation"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>

        {/* Sidebar navigation */}
        <aside className={clsx("book-sidebar", { "book-sidebar--open": sidebarOpen })}>
          <div className="book-sidebar-header">
            <h3 className="book-sidebar-title">Textbook Contents</h3>
            <button
              className="book-sidebar-close"
              onClick={closeSidebar}
              aria-label="Close navigation"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>

          <nav className="book-navigation">
            <ul className="book-toc">
              {bookStructure.map((module) => (
                <li key={module.id} className="book-toc-item">
                  <Link
                    to={module.path}
                    className={clsx("book-toc-module", {
                      "book-toc-module--active": location.pathname.includes(module.path) && !module.chapters.some(ch => location.pathname === ch.path)
                    })}
                    onClick={closeSidebar}
                  >
                    {module.title}
                  </Link>

                  {module.chapters.length > 0 && (
                    <ul className="book-toc-chapters">
                      {module.chapters.map((chapter, index) => (
                        <li key={index} className="book-toc-chapter-item">
                          <Link
                            to={chapter.path}
                            className={clsx("book-toc-chapter", {
                              "book-toc-chapter--active": location.pathname === chapter.path
                            })}
                            onClick={closeSidebar}
                          >
                            {chapter.title}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  )}
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        {/* Main content area */}
        <main className="book-main">
          <div className="book-content">
            <header className="book-header">
              <h1 className="book-title">{title || currentChapter?.title || 'Textbook Chapter'}</h1>
              {description && <p className="book-subtitle">{description}</p>}
            </header>

            <div className="book-body">
              {children}
            </div>

            {/* Chapter navigation */}
            {(prevChapter || nextChapter) && (
              <nav className="book-chapter-navigation">
                <div className="book-chapter-nav">
                  {prevChapter && (
                    <Link to={prevChapter.path} className="book-nav-link book-nav-link--prev">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M15 18L9 12L15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                      <span className="book-nav-text">
                        <span className="book-nav-direction">Previous</span>
                        <span className="book-nav-title">{prevChapter.title}</span>
                      </span>
                    </Link>
                  )}

                  {nextChapter && (
                    <Link to={nextChapter.path} className="book-nav-link book-nav-link--next">
                      <span className="book-nav-text">
                        <span className="book-nav-direction">Next</span>
                        <span className="book-nav-title">{nextChapter.title}</span>
                      </span>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </Link>
                  )}
                </div>
              </nav>
            )}
          </div>
        </main>
      </div>
    </AuthGuard>
  );
};

export default BookLayout;