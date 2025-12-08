/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Textbook Chapters',
      items: [
        'intro-physical-ai/intro',
        'basics-humanoid-robotics/intro',
        'ros-2-fundamentals/intro',
        'digital-twin-simulation/intro',
        'vision-language-action/intro',
        'capstone/intro',
      ],
    },
  ],
};

module.exports = sidebars;
