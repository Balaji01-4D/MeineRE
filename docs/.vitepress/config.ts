import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Meine',
  description: 'A cross-platform, regex-powered CLI for file operations with beautiful TUI',
  lastUpdated: true,
  ignoreDeadLinks: true,
  base: '/meine/',

  head: [
    ['link', { rel: 'icon', type: 'image/x-icon', href: '/meine/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#6c5ce7' }],
    ['meta', { name: 'og:type', content: 'website' }],
    ['meta', { name: 'og:title', content: 'Meine' }],
    ['meta', { name: 'og:description', content: 'A cross-platform, regex-powered CLI for file operations with beautiful TUI' }],
    ['meta', { name: 'og:image', content: '/meine/logo.png' }],
  ],

  themeConfig: {
    logo: '/logo.png',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'GitHub', link: 'https://github.com/Balaji01-4D/meine' }
    ],

   sidebar: {
  '/guide/': [
    {
      text: 'Guide',
      items: [
        { text: 'Getting Started', link: '/guide/getting-started' },
        { text: 'Installation', link: '/guide/installation.md' },
        { text: 'File Operations', link: '/guide/file-operations' },
        { text: 'System Commands', link: '/guide/system-commands' },
        { text: 'Keyboard Shortcuts', link: '/guide/shortcuts' }
      ]
    },
    { text: 'Credits', link: '/guide/credits.md' },
    { text: 'Support', link: '/guide/support.md' }
  ],
},


    socialLinks: [
      { icon: 'github', link: 'https://github.com/Balaji01-4D/meine' }

    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024-present Balaji J'
    },

    search: {
      provider: 'local'
    }
  }
})
