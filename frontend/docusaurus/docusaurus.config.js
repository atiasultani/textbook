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

  markdown: {},

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  themes: [],

  plugins: [
    [
      '@docusaurus/plugin-client-redirects',
      {
        fromExtensions: ['html'],
        redirects: [],
      },
    ],
  ],

  // ⚠️ Docusaurus v3 DOES NOT allow devMiddleware / webpack headers
  // Use a proxy or backend CORS instead

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/your-organization/textbook/edit/main/frontend/docusaurus/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',

    navbar: {
      title: 'Physical AI & Robotics Textbook',
      logo: {
        alt: 'Physical AI Robot Logo',
        src: 'img/robot-cover.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          type: 'dropdown',
          label: 'Modules',
          position: 'left',
          items: [
            {
              label: 'Module 1: Introduction to Physical AI',
              to: '/docs/intro-physical-ai/intro',
            },
            {
              label: 'Module 2: Humanoid Robotics Fundamentals',
              to: '/docs/basics-humanoid-robotics/intro',
            },
            {
              label: 'Module 3: Advanced Systems',
              to: '/docs/digital-twin-simulation/intro',
            },
            {
              label: 'Module 4: Capstone Project',
              to: '/docs/capstone/intro',
            },
          ],
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
          title: 'Modules',
          items: [
            { label: 'Module 1: Introduction to Physical AI', to: '/docs/intro-physical-ai/intro' },
            { label: 'Module 2: Humanoid Robotics Fundamentals', to: '/docs/basics-humanoid-robotics/intro' },
            { label: 'Module 3: Advanced Systems', to: '/docs/digital-twin-simulation/intro' },
            { label: 'Module 4: Capstone Project', to: '/docs/capstone/intro' },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/your-organization/textbook',
            },
            {
              label: 'Physical AI Community',
              href: 'https://example.com/physical-ai-community',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
    },

    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
    },
  },
};

module.exports = config;
