import React from 'react';
import { useLocation } from '@docusaurus/router';
import Link from '@docusaurus/Link';

const ChapterNavigation = () => {
  const location = useLocation();

  // Define the chapter order
  const chapters = [
    { id: 'intro', title: 'Introduction', path: '/docs/intro' },
    { id: 'intro-physical-ai', title: 'Chapter 1: Introduction to Physical AI', path: '/docs/intro-physical-ai' },
    { id: 'basics-humanoid-robotics', title: 'Chapter 2: Basics of Humanoid Robotics', path: '/docs/basics-humanoid-robotics' },
    { id: 'ros-2-fundamentals', title: 'Chapter 3: ROS 2 Fundamentals', path: '/docs/ros-2-fundamentals' },
    { id: 'digital-twin-simulation', title: 'Chapter 4: Digital Twin Simulation', path: '/docs/digital-twin-simulation' },
    { id: 'vision-language-action', title: 'Chapter 5: Vision-Language-Action Systems', path: '/docs/vision-language-action' },
    { id: 'capstone', title: 'Chapter 6: Capstone', path: '/docs/capstone' },
  ];

  // Get current chapter index
  const currentPath = location.pathname;
  const currentChapterIndex = chapters.findIndex(chapter =>
    currentPath.includes(chapter.path)
  );

  if (currentChapterIndex === -1) {
    return null; // Don't show navigation on non-chapter pages
  }

  const prevChapter = currentChapterIndex > 0 ? chapters[currentChapterIndex - 1] : null;
  const nextChapter = currentChapterIndex < chapters.length - 1 ? chapters[currentChapterIndex + 1] : null;

  return (
    <div className="chapter-navigation" style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '16px 0',
      marginTop: '24px',
      borderTop: '1px solid #eee',
      borderBottom: '1px solid #eee'
    }}>
      {prevChapter ? (
        <Link to={prevChapter.path} className="button button--secondary button--sm">
          ← {prevChapter.title}
        </Link>
      ) : (
        <div></div> // Empty div to maintain spacing
      )}

      <div style={{ textAlign: 'center' }}>
        <span style={{ color: '#666', fontSize: '0.9em' }}>
          Chapter {currentChapterIndex + 1} of {chapters.length}
        </span>
      </div>

      {nextChapter ? (
        <Link to={nextChapter.path} className="button button--primary button--sm">
          {nextChapter.title} →
        </Link>
      ) : (
        <div></div> // Empty div to maintain spacing
      )}
    </div>
  );
};

export default ChapterNavigation;