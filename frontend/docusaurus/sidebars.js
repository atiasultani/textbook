/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: Introduction to Physical AI',
      items: [
        'intro-physical-ai/intro',
        'intro-physical-ai/chapter1-foundations',
        'intro-physical-ai/chapter2-practical-applications',
        'intro-physical-ai/chapter3-advanced-concepts',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Humanoid Robotics Fundamentals',
      items: [
        'basics-humanoid-robotics/intro',
        'ros-2-fundamentals/intro',
        'ros-2-fundamentals/chapter1-core-concepts',
        'ros-2-fundamentals/chapter2-advanced-development',
        'ros-2-fundamentals/chapter3-ecosystem-integration',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Advanced Systems',
      items: [
        'digital-twin-simulation/intro',
        'vision-language-action/intro',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Capstone Project',
      items: [
        'capstone/intro',
      ],
    },
  ],
};

module.exports = sidebars;
