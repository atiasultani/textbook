import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import Link from '@docusaurus/Link';
import './ModuleNavigation.css';

const ModuleNavigation = () => {
  const location = useLocation();
  const [activeModule, setActiveModule] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);

  // Close dropdown when location changes
  useEffect(() => {
    setShowDropdown(false);
    setActiveModule(null);
  }, [location.pathname]);

  // Define modules with their chapters
  const modules = [
    {
      id: 1,
      title: 'Module 1: Introduction to Physical AI',
      path: '/docs/intro-physical-ai/intro',
      chapters: [
        { title: 'Introduction to Physical AI', path: '/docs/intro-physical-ai/intro' }
      ]
    },
    {
      id: 2,
      title: 'Module 2: Humanoid Robotics Fundamentals',
      path: '/docs/basics-humanoid-robotics/intro',
      chapters: [
        { title: 'Basics of Humanoid Robotics', path: '/docs/basics-humanoid-robotics/intro' },
        { title: 'ROS 2 Fundamentals', path: '/docs/ros-2-fundamentals/intro' }
      ]
    },
    {
      id: 3,
      title: 'Module 3: Advanced Systems',
      path: '/docs/digital-twin-simulation/intro',
      chapters: [
        { title: 'Digital Twin Simulation', path: '/docs/digital-twin-simulation/intro' },
        { title: 'Vision-Language-Action Systems', path: '/docs/vision-language-action/intro' }
      ]
    },
    {
      id: 4,
      title: 'Module 4: Capstone Project',
      path: '/docs/capstone/intro',
      chapters: [
        { title: 'Capstone', path: '/docs/capstone/intro' }
      ]
    }
  ];

  // Determine the current module based on the path
  const getCurrentModule = () => {
    for (const module of modules) {
      const chapter = module.chapters.find(ch => location.pathname.includes(ch.path));
      if (chapter) {
        return module.id;
      }
    }
    return 1; // default to module 1
  };

  const currentModuleId = getCurrentModule();

  const toggleDropdown = (moduleId) => {
    if (activeModule === moduleId && showDropdown) {
      setShowDropdown(false);
    } else {
      setActiveModule(moduleId);
      setShowDropdown(true);
    }
  };

  const isActiveChapter = (chapterPath) => {
    return location.pathname === chapterPath;
  };

  // Function to handle clicks outside the dropdown to close it
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showDropdown && !event.target.closest('.module-button-wrapper')) {
        setShowDropdown(false);
        setActiveModule(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showDropdown]);

  return (
    <div className="module-navigation-container">
      <div className="module-buttons">
        {modules.map((module) => (
          <div key={module.id} className="module-button-wrapper">
            <button
              className={`module-button ${currentModuleId === module.id ? 'active' : ''}`}
              onClick={() => toggleDropdown(module.id)}
              aria-expanded={activeModule === module.id && showDropdown}
              aria-haspopup="true"
            >
              {module.title}
            </button>

            {activeModule === module.id && showDropdown && (
              <div className="module-dropdown">
                <ul className="module-chapters-list">
                  {module.chapters.map((chapter, index) => (
                    <li key={index} className="module-chapter-item">
                      <Link
                        to={chapter.path}
                        className={`module-chapter-link ${isActiveChapter(chapter.path) ? 'active' : ''}`}
                        onClick={() => {
                          setShowDropdown(false);
                          setActiveModule(null);
                        }}
                      >
                        {chapter.title}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ModuleNavigation;