# Terminal UI Guide

Meine features a modern, responsive Terminal User Interface (TUI) built with Textual. This guide covers the UI layout, customization options, and interaction methods.

## Layout Overview

The interface is divided into three main panels:

```
┌─Directory Tree─┬─File Operations─┬─Preview/Info──┐
│               │                │              │
│  Folders      │   Command      │   File       │
│  and Files    │   Input and    │   Preview    │
│  Structure    │   Output       │   or Info    │
│               │                │              │
│               │                │              │
└───────────────┴────────────────┴──────────────┘
```

### Directory Tree Panel

- Shows hierarchical file system structure
- Expandable/collapsible folders
- Visual indicators for file types
- Selection highlighting
- Scroll bars for navigation

### File Operations Panel

- Command input area
- Operation output display
- Status messages
- Progress indicators
- Command history

### Preview/Info Panel

- File content preview
- File metadata
- System information
- Help content
- Error messages

## Theme Customization

Meine uses Textual CSS for styling. You can customize the appearance in `~/.config/meine/theme.tcss`:

```css
/* Panel colors */
#directory-tree {
    background: $surface;
    border: solid $primary;
}

#command-panel {
    background: $background;
    color: $text;
}

#preview-panel {
    background: $surface-darken-1;
}

/* Text styling */
.filename {
    color: $text;
}

.directory {
    color: $primary;
    bold: true;
}

.selected {
    background: $primary-darken-2;
    color: $text-lighten-1;
}
```

## Color Schemes

Meine includes several built-in color schemes:

```bash
# Switch color schemes
theme dark
theme light
theme system    # Follow system theme
theme custom    # Use custom theme
```

### Custom Colors

Define custom colors in your theme file:

```css
/* Custom colors */
$custom-primary: #6c5ce7;
$custom-secondary: #a29bfe;
$custom-accent: #fd79a8;

/* Apply custom colors */
.custom-element {
    color: $custom-primary;
    background: $custom-secondary;
    border: solid $custom-accent;
}
```

## Interactive Elements

### Buttons and Controls

```css
/* Button styling */
Button {
    background: $primary;
    color: $text;
    padding: 1 2;
    margin: 1;
    border: none;
}

Button:hover {
    background: $primary-lighten-1;
}

Button:focus {
    border: solid $accent;
}
```

### Input Fields

```css
/* Input field styling */
Input {
    background: $surface;
    border: solid $primary;
    padding: 0 1;
}

Input:focus {
    border: solid $accent;
}
```

## Responsive Design

The UI adapts to different terminal sizes:

```css
/* Responsive layout */
@media (width < 100) {
    #preview-panel {
        display: none;
    }
}

@media (width < 60) {
    #directory-tree {
        width: 20;
    }
}
```

## Animations

Add smooth transitions and animations:

```css
/* Animations */
.fade-in {
    transition: opacity 200ms;
}

.slide-in {
    transition: transform 200ms;
}
```

## Status Indicators

```css
/* Status indicators */
.success {
    color: $success;
}

.error {
    color: $error;
}

.warning {
    color: $warning;
}
```

## Keyboard Focus

Visual indicators for keyboard navigation:

```css
/* Focus indicators */
*:focus {
    border: solid $accent;
}

.focusable:focus {
    background: $primary-darken-1;
}
```

## Toast Notifications

Styling for notification popups:

```css
/* Toast notifications */
Toast {
    background: $surface;
    border: solid $primary;
    padding: 1 2;
}

Toast.error {
    border-left: solid $error;
}

Toast.success {
    border-left: solid $success;
}
```

## Best Practices

1. Use system color variables for consistency
2. Maintain contrast ratios for readability
3. Provide visual feedback for interactions
4. Keep the interface responsive
5. Use consistent spacing and alignment

## Configuration

UI settings can be adjusted in the configuration file:

```json
{
  "ui": {
    "theme": "dark",
    "show_hidden": false,
    "show_preview": true,
    "panel_ratio": [30, 40, 30]
  }
}
```

## Next Steps

- Explore [Keyboard Shortcuts](/guide/shortcuts)
- Learn about [File Operations](/guide/file-operations)
- Configure [Settings](/guide/configuration)
- Check out [System Commands](/guide/system-commands)
