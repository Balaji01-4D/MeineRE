from textual.theme import Theme

BUILTIN_THEMES: dict[str, Theme] = {
    "textual": Theme(
        name="textual",
        primary="#004578",
        secondary="#0178D4",
        warning="#ffa62b",
        error="#ba3c5b",
        success="#4EBF71",
        accent="#ffa62b",
        dark=True,
    ),
    "monokai 1": Theme(
        name="monokai 0.1",
        primary="#F92672",  # Pink
        secondary="#66D9EF",  # Light Blue
        warning="#FD971F",  # Orange
        error="#F92672",  # Pink (same as primary for consistency)
        success="#A6E22E",  # Green
        accent="#AE81FF",  # Purple
        background="#272822",  # Dark gray-green
        surface="#3E3D32",  # Slightly lighter gray-green
        panel="#3E3D32",  # Same as surface for consistency
        dark=True,
    ),
    "galaxy": Theme(
        name="galaxy",
        primary="#8A2BE2",  # Improved Deep Magenta (Blueviolet)
        secondary="#a684e8",
        warning="#FFD700",  # Gold, more visible than orange
        error="#FF4500",  # OrangeRed, vibrant but less harsh than pure red
        success="#00FA9A",  # Medium Spring Green, kept for vibrancy
        accent="#FF69B4",  # Hot Pink, for a pop of color
        dark=True,
        background="#0F0F1F",  # Very Dark Blue, almost black
        surface="#1E1E3F",  # Dark Blue-Purple
        panel="#2D2B55",  # Slightly Lighter Blue-Purple
    ),
    "nebula": Theme(
        name="nebula",
        primary="#4169E1",  # Royal Blue, more vibrant than Midnight Blue
        secondary="#9400D3",  # Dark Violet, more vibrant than Indigo Dye
        warning="#FFD700",  # Kept Gold for warnings
        error="#FF1493",  # Deep Pink, more nebula-like than Crimson
        success="#00FF7F",  # Spring Green, slightly more vibrant
        accent="#FF00FF",  # Magenta, for a true neon accent
        dark=True,
        background="#0A0A23",  # Dark Navy, closer to a night sky
        surface="#1C1C3C",  # Dark Blue-Purple
        panel="#2E2E5E",  # Slightly Lighter Blue-Purple
    ),
    "alpine": Theme(
        name="alpine",
        primary="#4A90E2",  # Clear Sky Blue
        secondary="#81A1C1",  # Misty Blue
        warning="#EBCB8B",  # Soft Sunlight
        error="#BF616A",  # Muted Red
        success="#A3BE8C",  # Alpine Meadow Green
        accent="#5E81AC",  # Mountain Lake Blue
        dark=True,
        background="#2E3440",  # Dark Slate Grey
        surface="#3B4252",  # Darker Blue-Grey
        panel="#434C5E",  # Lighter Blue-Grey
    ),
    "cobalt": Theme(
        name="cobalt",
        primary="#334D5C",  # Deep Cobalt Blue
        secondary="#4878A6",  # Slate Blue
        warning="#FFAA22",  # Amber, suitable for warnings related to primary
        error="#E63946",  # Red, universally recognized for errors
        success="#4CAF50",  # Green, commonly used for success indication
        accent="#D94E64",  # Candy Apple Red
        dark=True,
        surface="#27343B",  # Dark Lead
        panel="#2D3E46",  # Storm Gray
        background="#1F262A",  # Charcoal
    ),
    "twilight": Theme(
        name="twilight",
        primary="#367588",
        secondary="#5F9EA0",
        warning="#FFD700",
        error="#FF6347",
        success="#00FA9A",
        accent="#FF7F50",
        dark=True,
        background="#191970",
        surface="#3B3B6D",
        panel="#4C516D",
    ),
    "hacker": Theme(
        name="hacker",
        primary="#00FF00",  # Bright Green (Lime)
        secondary="#32CD32",  # Lime Green
        warning="#ADFF2F",  # Green Yellow
        error="#FF4500",  # Orange Red (for contrast)
        success="#00FA9A",  # Medium Spring Green
        accent="#39FF14",  # Neon Green
        dark=True,
        background="#0D0D0D",  # Almost Black
        surface="#1A1A1A",  # Very Dark Gray
        panel="#2A2A2A",  # Dark Gray
    ),
    "aurora": Theme(
        name="aurora",
        primary="#76B3F0",  # Glacier Blue
        secondary="#A1D6E2",  # Ice Blue
        warning="#F8E71C",  # Bright Yellow
        error="#FF6B6B",  # Warm Red
        success="#50C878",  # Emerald Green
        accent="#DDA0DD",  # Orchid
        dark=True,
        background="#0B132B",  # Deep Midnight Blue
        surface="#1C2541",  # Dark Blue Slate
        panel="#3A506B",  # Muted Teal
    ),
    "cyberpunk": Theme(
        name="cyberpunk",
        primary="#FF007F",  # Neon Pink
        secondary="#00E5FF",  # Neon Cyan
        warning="#FFD700",  # Bright Gold
        error="#FF3131",  # Vivid Red
        success="#00FF7F",  # Bright Green
        accent="#8A2BE2",  # Deep Purple
        dark=True,
        background="#080808",  # Almost Black
        surface="#181818",  # Dark Gray
        panel="#282828",  # Lighter Gray
    ),
    "retro_wave": Theme(
        name="retro_wave",
        primary="#FF6EC7",  # Neon Pink
        secondary="#FFD700",  # Golden Yellow
        warning="#FFA500",  # Orange
        error="#E60000",  # Deep Red
        success="#39FF14",  # Electric Green
        accent="#8B00FF",  # Electric Purple
        dark=True,
        background="#2D1E2F",  # Dark Purple
        surface="#3B2E50",  # Muted Dark Blue
        panel="#503571",  # Deep Magenta
    ),
}


testing = {
    "holographic": Theme(
        name="holographic",
        primary="rgba(173, 216, 230, 0.7)",  # Soft Light Blue
        secondary="rgba(255, 182, 193, 0.7)",  # Light Pink
        warning="rgba(255, 215, 0, 0.7)",  # Gold
        error="rgba(255, 99, 71, 0.7)",  # Tomato Red
        success="rgba(124, 252, 0, 0.7)",  # Neon Green
        accent="rgba(186, 85, 211, 0.7)",  # Medium Orchid
        dark=False,
        background="rgba(240, 248, 255, 0.2)",  # Very Light Transparent Blue
        surface="rgba(200, 225, 255, 0.3)",  # Soft Blue Tint
        panel="rgba(175, 200, 255, 0.4)",  # Slightly Darker Blue Tint
    ),
    "transparent_night": Theme(
        name="transparent_night",
        primary="rgba(100, 200, 255, 0.7)",  # Soft Cyan
        secondary="rgba(200, 150, 255, 0.7)",  # Light Purple
        warning="rgba(255, 165, 0, 0.7)",  # Orange
        error="rgba(255, 69, 0, 0.7)",  # Red-Orange
        success="rgba(50, 205, 50, 0.7)",  # Lime Green
        accent="rgba(255, 105, 180, 0.7)",  # Hot Pink
        dark=True,
        background="rgba(15, 15, 40, 0.3)",  # Deep Navy Transparency
        surface="rgba(25, 25, 50, 0.4)",  # Dark Blue Tint
        panel="rgba(45, 45, 75, 0.5)",  # Slightly Lighter Blue Tint
    ),
    "ethereal": Theme(
        name="ethereal",
        primary="rgba(255, 240, 245, 0.7)",  # Lavender Blush
        secondary="rgba(221, 160, 221, 0.7)",  # Plum
        warning="rgba(255, 223, 186, 0.7)",  # Peach Puff
        error="rgba(255, 69, 96, 0.7)",  # Bright Red-Pink
        success="rgba(144, 238, 144, 0.7)",  # Light Green
        accent="rgba(135, 206, 250, 0.7)",  # Light Sky Blue
        dark=False,
        background="rgba(245, 245, 245, 0.2)",  # Ultra Soft White
        surface="rgba(225, 225, 225, 0.3)",  # Light Mist Gray
        panel="rgba(205, 205, 205, 0.4)",  # Slightly Darker Mist Gray
    ),
    "cyber_glass": Theme(
        name="cyber_glass",
        primary="rgba(255, 0, 255, 0.7)",  # Neon Magenta
        secondary="rgba(0, 255, 255, 0.7)",  # Cyan Glow
        warning="rgba(255, 255, 0, 0.7)",  # Neon Yellow
        error="rgba(255, 0, 0, 0.7)",  # Bright Red
        success="rgba(0, 255, 127, 0.7)",  # Neon Green
        accent="rgba(75, 0, 130, 0.7)",  # Electric Indigo
        dark=True,
        background="rgba(10, 10, 10, 0.2)",  # Almost Black Transparency
        surface="rgba(20, 20, 20, 0.3)",  # Dark Gray Tint
        panel="rgba(40, 40, 40, 0.4)",  # Slightly Brighter Gray
    ),
    "glass-ansi": Theme(
        name="glass-ansi",
        primary="ansi_bright_white",
        secondary="ansi_bright_cyan",
        warning="ansi_yellow",
        error="ansi_red",
        success="ansi_green",
        accent="ansi_bright_blue",
        foreground="ansi_default",  # Uses terminal's default text color
        background="ansi_default",  # Transparent effect
        surface="ansi_default",
        panel="ansi_default",
        boost="ansi_default",
        dark=False,
        variables={
            "block-cursor-text-style": "b",
            "block-cursor-blurred-text-style": "i",
            "input-selection-background": "ansi_cyan",
            "input-cursor-text-style": "reverse",
            "scrollbar": "ansi_blue",
            "border-blurred": "ansi_bright_blue",
            "border": "ansi_cyan",
        },
    ),
    "frosted-ansi": Theme(
        name="frosted-ansi",
        primary="ansi_bright_cyan",
        secondary="ansi_bright_white",
        warning="ansi_yellow",
        error="ansi_bright_red",
        success="ansi_bright_green",
        accent="ansi_bright_magenta",
        foreground="ansi_default",
        background="ansi_default",
        surface="ansi_default",
        panel="ansi_default",
        boost="ansi_default",
        dark=True,
        variables={
            "block-cursor-text-style": "b",
            "block-cursor-blurred-text-style": "i",
            "input-selection-background": "ansi_blue",
            "input-cursor-text-style": "reverse",
            "scrollbar": "ansi_bright_cyan",
            "border-blurred": "ansi_bright_white",
            "border": "ansi_blue",
        },
    ),
    "holographic-ansi": Theme(
        name="holographic-ansi",
        primary="ansi_bright_magenta",
        secondary="ansi_bright_cyan",
        warning="ansi_yellow",
        error="ansi_red",
        success="ansi_green",
        accent="ansi_bright_blue",
        foreground="ansi_default",
        background="ansi_default",
        surface="ansi_default",
        panel="ansi_default",
        boost="ansi_default",
        dark=False,
        variables={
            "block-cursor-text-style": "b",
            "block-cursor-blurred-text-style": "i",
            "input-selection-background": "ansi_bright_magenta",
            "input-cursor-text-style": "reverse",
            "scrollbar": "ansi_blue",
            "border-blurred": "ansi_bright_cyan",
            "border": "ansi_bright_magenta",
        },
    ),
    "transparent_night-ansi": Theme(
        name="transparent_night-ansi",
        primary="ansi_bright_blue",
        secondary="ansi_bright_white",
        warning="ansi_bright_yellow",
        error="ansi_bright_red",
        success="ansi_bright_green",
        accent="ansi_bright_cyan",
        foreground="ansi_default",
        background="ansi_default",
        surface="ansi_default",
        panel="ansi_default",
        boost="ansi_default",
        dark=True,
        variables={
            "block-cursor-text-style": "b",
            "block-cursor-blurred-text-style": "i",
            "input-selection-background": "ansi_blue",
            "input-cursor-text-style": "reverse",
            "scrollbar": "ansi_cyan",
            "border-blurred": "ansi_blue",
            "border": "ansi_bright_white",
        },
    ),
}
