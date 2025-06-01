from textual.theme import Theme

BUILTIN_THEMES: dict[str, Theme] = {
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
