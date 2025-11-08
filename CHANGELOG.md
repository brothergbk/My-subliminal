# Changelog

All notable changes to the Subliminal Message App will be documented in this file.

## [2.0.1] - 2025-11-08

### Fixed
- **Always-on-top behavior**: Flashing window now properly stays on top of ALL applications
- **Click-through support**: Added WS_EX_TRANSPARENT flag so you can click through the transparent areas
- **Improved window flags**: Enhanced Windows API integration for better topmost behavior
  - Added WS_EX_TOPMOST flag
  - Added WS_EX_TRANSPARENT flag for click-through
  - Improved SetWindowPos call with proper flags

### Technical Details
The flashing window now uses these Windows extended styles:
- `WS_EX_LAYERED` - Enables transparency
- `WS_EX_TOPMOST` - Keeps window on top
- `WS_EX_TRANSPARENT` - Allows clicking through transparent areas

This ensures the subliminal messages appear on top of any application you're using, while still allowing you to interact with your applications normally.

## [2.0.0] - 2025-11-08

### Added
- **Category Management System**: Organize words into multiple categories
- **Multi-Category Selection**: Select and combine multiple categories for flashing
- **Modern Dark UI**: Beautiful Catppuccin Mocha-inspired dark theme
- **Two-Panel Layout**: Categories on left, settings and controls on right
- **Enhanced Word Editing**: Edit words directly and save back to categories
- **Improved Persistence**: Categories and all words saved between sessions
- **Better UX Elements**:
  - Emoji icons for visual clarity
  - Live value displays on sliders
  - Color picker with visual preview
  - Status indicators showing category/word counts
- **Batch File Launchers**: Easy-to-use .bat files to launch the app

### Changed
- Increased maximum font size from 72 to 100
- Window size increased to 1000x750 for better layout
- Settings now include category data in JSON file
- Improved file loading with better error handling

### Technical
- New file: `subliminal_app_modern.py` - Modern version with all new features
- Original `subliminal_app.py` maintained for backward compatibility
- Enhanced category data structure with set-based selection tracking
- Improved threading for flash loop

## [1.0.0] - 2025-11-08

### Initial Release
- Basic subliminal message flashing
- Transparent fullscreen display
- Customizable flash duration and intervals
- Font size and text color customization
- CSV/TXT file loading (newline-delimited)
- Editable word preview
- Settings persistence
- Windows transparency support

