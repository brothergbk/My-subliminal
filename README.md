# Subliminal Message App

A Python-based subliminal message application that flashes words on your screen at customizable intervals. Perfect for subliminal learning, affirmations, or reinforcement of concepts.

## Features

- 🎯 **Transparent Display** - Words appear floating on your screen with no background
- ⚙️ **Customizable Settings** - Control flash duration, intervals, font size, and text color
- 📝 **Editable Word Lists** - Load from files or edit directly in the app
- 💾 **Persistent Settings** - Your preferences are saved automatically
- 🎨 **Clean UI** - Simple, intuitive interface built with Tkinter
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
git clone https://github.com/brothergbk/sublim.git
cd sublim
```

2. Install dependencies:
```bash
pip install -r requirement.txt
```

## Usage

1. **Run the application:**
```bash
python subliminal_app.py
```

2. **Load your word list:**
   - Click "Browse CSV" to load a text file with words (one word per line)
   - Or manually type/edit words in the preview window and click "Update Words from Text"

3. **Configure settings:**
   - **Flash Duration**: How long each word appears (0.05-1.0 seconds)
   - **Interval**: Time between word flashes (1-30 seconds)
   - **Font Size**: Size of the displayed text (12-72)
   - **Text Color**: Color of the words

4. **Start flashing:**
   - Click "Start Flashing" to begin
   - The app will minimize and display words fullscreen
   - Click "Stop Flashing" to stop

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

Settings are automatically saved to `subliminal_settings.json` in the app directory and loaded on startup.

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

