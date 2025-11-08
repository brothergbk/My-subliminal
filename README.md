# Subliminal Message App

A Python-based subliminal message application that flashes words on your screen at customizable intervals. Perfect for subliminal learning, affirmations, or reinforcement of concepts.

## Version 2.0 - New Features! 🎉

- 📁 **Category Management** - Organize words into multiple categories
- 🎯 **Multi-Select Categories** - Combine multiple categories for flashing
- 🎨 **Modern Dark UI** - Beautiful dark theme with improved user experience
- 📊 **Better Organization** - Two-panel layout for easier navigation

## Features

- 🎯 **Transparent Display** - Words appear floating on your screen with no background
- 📁 **Category System** - Organize your word lists into categories (NEW in v2.0)
- 🔀 **Multi-Category Selection** - Select and combine multiple categories (NEW in v2.0)
- ⚙️ **Customizable Settings** - Control flash duration, intervals, font size, and text color
- 📝 **Editable Word Lists** - Load from files or edit directly in the app
- 💾 **Persistent Settings** - Your preferences and categories are saved automatically
- 🎨 **Modern UI** - Beautiful dark theme with intuitive two-panel layout (NEW in v2.0)
- 🔄 **Real-time Updates** - Modify your word list on the fly

## Screenshots

The app displays words briefly on your screen in a non-intrusive way, allowing you to continue working while receiving subliminal messages.

## Installation

### Requirements

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/brothergbk/My-subliminal.git
cd My-subliminal
```

2. Install dependencies:
```bash
pip install -r requirement.txt
```

## Usage

### Version 2.0 (Modern UI with Categories)

1. **Run the application:**
```bash
python subliminal_app_modern.py
```

2. **Create and manage categories:**
   - Click "➕ Add Category" to create a new category
   - Click "📂 Load from File" to load a word list into a category
   - Click "🗑️ Delete" to remove selected categories

3. **Select categories:**
   - Click on a category to select it (words will appear in the preview)
   - Hold Ctrl and click to select multiple categories
   - Selected categories' words will be combined for flashing

4. **Edit words:**
   - Words from selected categories appear in the text area
   - Edit them directly in the preview window
   - Click "✓ Update Active Words" to save changes back to the category

5. **Configure settings:**
   - **Flash Duration**: How long each word appears (0.05-1.0 seconds)
   - **Interval**: Time between word flashes (1-30 seconds)
   - **Font Size**: Size of the displayed text (12-100)
   - **Text Color**: Color of the words (with color picker)

6. **Start flashing:**
   - Click "▶️ Start Flashing" to begin
   - The app will minimize and display words fullscreen
   - Click "⏹️ Stop Flashing" to stop

### Version 1.0 (Classic UI)

1. **Run the application:**
```bash
python subliminal_app.py
```

2. **Load your word list:**
   - Click "Browse CSV" to load a text file with words (one word per line)
   - Or manually type/edit words in the preview window and click "Update Words from Text"

3. **Configure and start** as described above

## Word List Format

Create a text file (`.txt` or `.csv`) with one word or phrase per line:

```
Success
Confidence
Focus
Productivity
Happiness
```

## How It Works

The app uses pygame to create a transparent fullscreen window that displays words at your configured intervals. The window uses Windows API calls to achieve true transparency, so only the text appears on your screen.

## Configuration

Settings and categories are automatically saved to `subliminal_settings.json` in the app directory and loaded on startup.

**Version 2.0** saves both your settings and all your categories with their word lists, so everything persists between sessions.

## Dependencies

- **pandas** - For data handling
- **pygame** - For rendering the transparent display window
- **tkinter** - For the GUI (included with Python)

## Platform Support

Currently optimized for **Windows**. The transparency features use Windows-specific API calls.

## Tips

- Start with longer intervals (10-15 seconds) and shorter flash durations (0.1-0.2 seconds) for true subliminal effect
- Use positive affirmations or key concepts you want to reinforce
- The app works best when you're doing other tasks on your computer

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Author

Created by Bosonkie (brothergbk)

## Disclaimer

This app is for educational and personal development purposes. The effectiveness of subliminal messaging varies by individual.

