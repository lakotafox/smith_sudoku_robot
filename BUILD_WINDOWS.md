# Building KittySudoku for Windows

## Requirements
- Windows computer with Python 3.8 or higher
- Internet connection for downloading dependencies

## Build Steps

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Open Command Prompt**
   - Press Windows Key + R
   - Type `cmd` and press Enter

3. **Navigate to the project folder**
   ```
   cd path\to\smith_sudoku_robot
   ```

4. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

5. **Build the executable**
   ```
   python setup_windows.py
   ```

6. **Find your executable**
   - The executable will be in: `dist_windows\KittySudoku.exe`
   - Copy this file to your grandma's computer

## Running on Grandma's Computer
1. Double-click `KittySudoku.exe`
2. Click any difficulty button to print a puzzle
3. The program will automatically close after printing

## Troubleshooting
- If printing doesn't work, make sure a default printer is set in Windows
- The program creates a temporary PDF file that gets sent to the printer
- Windows Defender might briefly scan the exe - this is normal