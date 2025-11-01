"""
CodeNCash Logo and Branding Assets
"""

LOGO_SVG = """
<svg width="200" height="60" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0066FF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00D9A3;stop-opacity:1" />
    </linearGradient>
  </defs>
  <text x="10" y="40" font-family="Inter, sans-serif" font-size="36" font-weight="800" fill="url(#logoGradient)">
    Code<tspan fill="#FFB800">N</tspan>Cash
  </text>
</svg>
"""

FAVICON_SVG = """
<svg width="32" height="32" xmlns="http://www.w3.org/2000/svg">
  <circle cx="16" cy="16" r="14" fill="#0066FF"/>
  <text x="16" y="22" font-family="Arial" font-size="18" font-weight="bold" fill="white" text-anchor="middle">?</text>
</svg>
"""

BRAND_COLORS = {
    "primary": "#0066FF",
    "secondary": "#00D9A3",
    "accent": "#FFB800",
    "success": "#10B981",
    "danger": "#EF4444",
    "bg_dark": "#0A0E27",
    "bg_card": "#151B3D",
    "text": "#FFFFFF",
    "text_secondary": "#A0AEC0"
}

TAGLINE = "AI-Powered Investment Advisor for Indian Markets"
APP_NAME = "CodeNCash"
