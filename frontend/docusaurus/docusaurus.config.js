// @ts-check
/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI-Native Textbook: Physical AI & Humanoid Robotics',
  tagline: 'An interactive textbook with RAG-powered chatbot',
  favicon: 'img/favicon.ico',

  url: 'https://your-organization.github.io',
  baseUrl: '/',

  organizationName: 'your-organization',
  projectName: 'textbook',

  onBrokenLinks: 'throw',

  // 🔥 Updated markdown config to fix the warning
  markdown: {},

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/your-organization/textbook/edit/main/frontend/docusaurus/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig: ({
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Robotics Textbook',
        logo: {
          alt: 'Textbook Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/your-organization/textbook',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Chapters',
            items: [
              { label: 'Introduction to Physical AI', to: '/docs/intro-physical-ai/intro' },
              { label: 'Basics of Humanoid Robotics', to: '/docs/basics-humanoid-robotics/intro' },
              { label: 'ROS 2 Fundamentals', to: '/docs/ros-2-fundamentals/intro' },
              { label: 'Digital Twin Simulation', to: '/docs/digital-twin-simulation/intro' },
              { label: 'Vision-Language-Action Systems', to: '/docs/vision-language-action/intro' },
              { label: 'Capstone', to: '/docs/capstone/intro' },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/your-organization/textbook',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
      },

      prism: {
        theme: require("prism-react-renderer").themes.github,
        darkTheme: require("prism-react-renderer").themes.dracula,
      },
  }),
};

module.exports = config;
