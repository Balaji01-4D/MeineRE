import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Meine',
  description: 'A cross-platform, regex-powered CLI for file operations with beautiful TUI',
  lastUpdated: true,
  base: '/meine/',

  head: [
    ['link', { rel: 'icon', type: 'image/png', href: '/logo.png' }],
    ['meta', { name: 'theme-color', content: '#6c5ce7' }],
    ['meta', { name: 'og:type', content: 'website' }],
    ['meta', { name: 'og:title', content: 'Meine' }],
    ['meta', { name: 'og:description', content: 'A cross-platform, regex-powered CLI for file operations with beautiful TUI' }],
    ['meta', { name: 'og:image', content: '/logo.png' }],
  ],

  themeConfig: {
    logo: '/logo.png',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/' },
      { text: 'Reference', link: '/reference/' },
      { text: 'GitHub', link: 'https://github.com/balaji/meine' }
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Guide',
          items: [
            { text: 'Getting Started', link: '/guide/getting-started' }
          ]
        },
        {
          text: 'Features',
          items: [
            { text: 'File Operations', link: '/guide/file-operations' },
            { text: 'System Commands', link: '/guide/system-commands' },
            { text: 'Terminal UI', link: '/guide/terminal-ui' },
            { text: 'Theming', link: '/guide/theming' }
          ]
        },
        {
          text: 'Advanced',
          items: [
            { text: 'Configuration', link: '/guide/configuration' },
            { text: 'Keyboard Shortcuts', link: '/guide/shortcuts' },
            { text: 'Plugins', link: '/guide/plugins' }
          ]
        }
      ],
      '/reference/': [
        {
          text: 'Reference',
          items: [
            { text: 'Commands', link: '/reference/commands' },
            { text: 'Configuration', link: '/reference/configuration' },
            { text: 'API', link: '/reference/api' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/balaji/meine' }
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
