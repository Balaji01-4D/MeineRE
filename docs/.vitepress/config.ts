import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Meine',
  description: 'A cross-platform, regex-powered CLI for file operations with beautiful TUI',
  lastUpdated: true,

  themeConfig: {
    logo: '/logo.png',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Reference', link: '/reference/commands' },
      { text: 'GitHub', link: 'https://github.com/Balaji01-4D/meine' }
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Introduction',
          items: [
            { text: 'Getting Started', link: '/guide/getting-started' },
            { text: 'Installation', link: '/guide/installation' },
            { text: 'Basic Usage', link: '/guide/basic-usage' }
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
