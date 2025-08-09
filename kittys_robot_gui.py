import tkinter as tk
from tkinter import ttk, messagebox
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import subprocess
import textwrap
import platform


def get_family_quotes():
    quotes = [
        "I love making Waffle cones with you! Love you gran! - Karac",
        "I love being your little Navy brat - your daughter Sue",
        "keep thinking celestial - Dallin",
        "Hand me the child cheater - Ashley",
        "I'm just resting my eyes - Tiffany",
        "I love you so much we named a kid KIT - Carrie",
        "We love your grandma all of us - Kyle",
        "Thanks for being the best great grandma ever - fox kids",
        "We love you from 5 generations down - Ellie and her family",
        "Never stand when you can sit, and never sit when you can lay down - Carson Daneille and Indie"
    ]
    # Return 3 random quotes
    return random.sample(quotes, min(3, len(quotes)))


def get_random_inspiration():
    inspirations = [
        # Poems
        ("The Road Not Taken", "Robert Frost", 
         "Two roads diverged in a yellow wood,\nAnd sorry I could not travel both\nAnd be one traveler, long I stood\nAnd looked down one as far as I could\nTo where it bent in the undergrowth..."),
        
        ("Hope", "Emily Dickinson",
         "Hope is the thing with feathers\nThat perches in the soul,\nAnd sings the tune without the words,\nAnd never stops at all..."),
        
        ("Do Not Go Gentle Into That Good Night", "Dylan Thomas",
         "Do not go gentle into that good night,\nOld age should burn and rave at close of day;\nRage, rage against the dying of the light..."),
        
        # LDS Scriptures
        ("Proverbs 3:5-6", "",
         "Trust in the Lord with all thine heart; and lean not unto\nthine own understanding. In all thy ways acknowledge him,\nand he shall direct thy paths."),
        
        ("Alma 37:37", "Book of Mormon",
         "Counsel with the Lord in all thy doings, and he will\ndirect thee for good; yea, when thou liest down at night\nlie down unto the Lord, that he may watch over you in\nyour sleep; and when thou risest in the morning let thy\nheart be full of thanks unto God..."),
        
        ("Moroni 10:4-5", "Book of Mormon",
         "And when ye shall receive these things, I would exhort you\nthat ye would ask God, the Eternal Father, in the name of\nChrist, if these things are not true; and if ye shall ask\nwith a sincere heart, with real intent, having faith in\nChrist, he will manifest the truth of it unto you, by the\npower of the Holy Ghost."),
        
        ("D&C 6:36", "Doctrine and Covenants",
         "Look unto me in every thought; doubt not, fear not."),
        
        ("1 Nephi 3:7", "Book of Mormon",
         "And it came to pass that I, Nephi, said unto my father:\nI will go and do the things which the Lord hath commanded,\nfor I know that the Lord giveth no commandments unto the\nchildren of men, save he shall prepare a way for them\nthat they may accomplish the thing which he commandeth them."),
        
        ("Matthew 11:28-30", "",
         "Come unto me, all ye that labour and are heavy laden,\nand I will give you rest. Take my yoke upon you, and\nlearn of me; for I am meek and lowly in heart: and ye\nshall find rest unto your souls. For my yoke is easy,\nand my burden is light."),
        
        ("Isaiah 40:31", "",
         "But they that wait upon the Lord shall renew their strength;\nthey shall mount up with wings as eagles; they shall run,\nand not be weary; and they shall walk, and not faint."),
        
        ("D&C 89:10-11", "Doctrine and Covenants",
         "And again, verily I say unto you, all wholesome herbs\nGod hath ordained for the constitution, nature, and use of man—\nEvery herb in the season thereof, and every fruit in the\nseason thereof; all these to be used with prudence and thanksgiving."),
        
        ("D&C 89:12-13", "Doctrine and Covenants", 
         "Yea, flesh also of beasts and of the fowls of the air,\nI, the Lord, have ordained for the use of man with thanksgiving;\nnevertheless they are to be used sparingly;\nAnd it is pleasing unto me that they should not be used,\nonly in times of winter, or of cold, or famine.")
    ]
    
    return random.choice(inspirations)


def generate_sudoku(difficulty="medium"):
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, side + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # Adjust empty cells based on difficulty
    squares = side * side
    if difficulty == "easy":
        empties = squares * 1 // 2  # 50% empty
    elif difficulty == "medium":
        empties = squares * 3 // 4  # 75% empty
    else:  # hard
        empties = squares * 4 // 5  # 80% empty
    
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0

    solution = [[nums[pattern(r, c)] for c in cols] for r in rows]

    return board, solution


def draw_sudoku(c, sudoku, x_offset, y_offset, title, block_size=30, center_title=False, page_width=612, difficulty_label=None, show_difficulty=True):
    if title:
        lines = title.split('\n')
        y_pos = y_offset + 40
        for i, line in enumerate(lines):
            if i == 0:
                c.setFont("Helvetica-Bold", 16)
            else:
                c.setFont("Helvetica", 14)
                y_pos -= 20
            
            if center_title:
                text_width = c.stringWidth(line, c._fontname, c._fontsize)
                title_x = (page_width - text_width) / 2
                c.drawString(title_x, y_pos, line)
            else:
                c.drawString(x_offset, y_pos, line)
    
    # Add difficulty label in top right corner (only if show_difficulty is True)
    if difficulty_label and show_difficulty:
        c.setFont("Helvetica-Bold", 14)
        label_text = difficulty_label.upper()
        label_width = c.stringWidth(label_text, "Helvetica-Bold", 14)
        c.drawString(page_width - label_width - 50, y_offset + 40, label_text)

    c.setFont("Helvetica", 20)

    # Draw the 9x9 grid with proper 3x3 box divisions
    for i in range(10):
        # Determine line width based on position
        if i % 3 == 0:
            c.setLineWidth(2)  # Thick lines for 3x3 boxes
        else:
            c.setLineWidth(0.5)  # Thin lines for cells
        
        # Draw horizontal lines
        y = y_offset - i * block_size
        c.line(x_offset, y, x_offset + 9 * block_size, y)
        
        # Draw vertical lines
        x = x_offset + i * block_size
        c.line(x, y_offset, x, y_offset - 9 * block_size)
    
    # Reset line width for drawing numbers
    c.setLineWidth(1)
    
    # Draw numbers
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                x = x_offset + j * block_size + block_size // 3
                y = y_offset - i * block_size - 3 * block_size // 4
                c.drawString(x, y, str(sudoku[i][j]))


def draw_inspiration(c, y_position, width):
    title, source, text = get_random_inspiration()
    
    # Draw title
    c.setFont("Helvetica-Bold", 14)
    title_width = c.stringWidth(title, "Helvetica-Bold", 14)
    c.drawString((width - title_width) / 2, y_position, title)
    
    # Draw source if exists
    if source:
        c.setFont("Helvetica-Oblique", 12)
        source_width = c.stringWidth(source, "Helvetica-Oblique", 12)
        c.drawString((width - source_width) / 2, y_position - 20, source)
        y_position -= 20
    
    # Draw text
    c.setFont("Helvetica", 11)
    y_position -= 30
    
    # Wrap text to fit page width
    lines = text.split('\n')
    for line in lines:
        if line.strip():
            wrapped = textwrap.wrap(line, width=80)
            for wrapped_line in wrapped:
                line_width = c.stringWidth(wrapped_line, "Helvetica", 11)
                c.drawString((width - line_width) / 2, y_position, wrapped_line)
                y_position -= 16
        else:
            y_position -= 8
    
    return y_position


def create_pdf(puzzle, solution, difficulty, filename="sudoku_print.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    block_size = 38  # Increased from 36 for slightly larger puzzles

    puzzle_width = block_size * 9
    x_offset = (width - puzzle_width) // 2  # Center the puzzle

    # Draw title centered at top of first page with difficulty label (only at top)
    draw_sudoku(c, puzzle, x_offset=x_offset, y_offset=height - 75, 
                title="Kitty's Sudoku Puzzle\nYou are loved by many", block_size=block_size, 
                center_title=True, page_width=width, difficulty_label=difficulty, show_difficulty=True)
    
    # Add family quotes - split between left and right of first puzzle
    quotes = get_family_quotes()
    c.setFont("Helvetica-Oblique", 10)
    
    # First quote on the left
    if len(quotes) > 0:
        y_position = height - 180
        x_position = 30  # Left margin
        wrapped_lines = textwrap.wrap(quotes[0], width=18)
        for line in wrapped_lines:
            c.drawString(x_position, y_position, line)
            y_position -= 13
    
    # Second quote on the right
    if len(quotes) > 1:
        y_position = height - 180
        x_position = x_offset + puzzle_width + 20  # Right of puzzle
        wrapped_lines = textwrap.wrap(quotes[1], width=18)
        for line in wrapped_lines:
            c.drawString(x_position, y_position, line)
            y_position -= 13
    
    # Draw second copy of puzzle below (no difficulty label)
    draw_sudoku(c, puzzle, x_offset=x_offset, y_offset=height - 450, 
                title="", block_size=block_size, show_difficulty=False)
    
    # Third quote on left of second puzzle
    if len(quotes) > 2:
        c.setFont("Helvetica-Oblique", 10)
        y_position = height - 550
        x_position = 30  # Left margin
        wrapped_lines = textwrap.wrap(quotes[2], width=18)
        for line in wrapped_lines:
            c.drawString(x_position, y_position, line)
            y_position -= 13

    # Start new page for solution
    c.showPage()
    
    # Draw solution on second page (no difficulty label)
    draw_sudoku(c, solution, x_offset=x_offset, y_offset=height - 75, 
                title="Solution", block_size=block_size,
                center_title=True, page_width=width, show_difficulty=False)
    
    # Add inspiration below solution
    draw_inspiration(c, height - 440, width)
    
    c.save()


def open_pdf(filename):
    """Cross-platform PDF opening"""
    if platform.system() == 'Darwin':  # macOS
        subprocess.run(['open', filename])
    elif platform.system() == 'Windows':
        os.startfile(filename)
    else:  # Linux
        subprocess.run(['xdg-open', filename])


def print_pdf(filename):
    """Cross-platform PDF printing"""
    if platform.system() == 'Darwin':  # macOS
        subprocess.run(['lpr', filename])
    elif platform.system() == 'Windows':
        os.startfile(filename, 'print')
    else:  # Linux
        subprocess.run(['lpr', filename])


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kitty's Sudoku Printer")
        self.root.attributes('-fullscreen', True)  # Full screen mode
        self.root.configure(bg='#FFE4E1')  # Misty Rose background
        
        # Add escape key to exit fullscreen (helpful for testing)
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Main frame - centered
        main_frame = tk.Frame(root, bg='#FFE4E1')
        main_frame.pack(expand=True)
        
        # Button frame - horizontal layout
        button_frame = tk.Frame(main_frame, bg='#FFE4E1')
        button_frame.pack(pady=50)
        
        # Three buttons side by side - bigger for fullscreen
        easy_btn = tk.Button(button_frame, text="EASY", 
                           font=('Arial', 48, 'bold'),
                           bg='#90EE90',  # Light Green
                           fg='#006400',  # Dark Green text
                           width=12, height=3,
                           command=lambda: self.print_puzzle("easy"))
        easy_btn.grid(row=0, column=0, padx=20)
        
        medium_btn = tk.Button(button_frame, text="MEDIUM", 
                             font=('Arial', 48, 'bold'),
                             bg='#87CEEB',  # Sky Blue
                             fg='#00008B',  # Dark Blue text
                             width=12, height=3,
                             command=lambda: self.print_puzzle("medium"))
        medium_btn.grid(row=0, column=1, padx=20)
        
        hard_btn = tk.Button(button_frame, text="HARD", 
                           font=('Arial', 48, 'bold'),
                           bg='#FFB6C1',  # Light Pink
                           fg='#8B0000',  # Dark Red text
                           width=12, height=3,
                           command=lambda: self.print_puzzle("hard"))
        hard_btn.grid(row=0, column=2, padx=20)
        
        # Status label below buttons - bigger for fullscreen
        self.status_label = tk.Label(main_frame, text="Choose difficulty to print puzzle", 
                                   font=('Arial', 24),
                                   bg='#FFE4E1', fg='#4B0082')  # Indigo
        self.status_label.pack(pady=30)
    
    def print_puzzle(self, difficulty):
        self.status_label.config(text="Creating your puzzle...")
        self.root.update()
        
        try:
            puzzle, solution = generate_sudoku(difficulty)
            create_pdf(puzzle, solution, difficulty)
            # Print the puzzle
            print_pdf("sudoku_print.pdf")
            self.status_label.config(text="✓ Puzzle sent to printer!", fg='#228B22')  # Forest Green
            # Close GUI after 2 seconds
            self.root.after(2000, self.root.quit)
        except Exception as e:
            self.status_label.config(text="❌ Failed to create puzzle", fg='#DC143C')  # Crimson
            messagebox.showerror("Error", f"Could not create puzzle: {str(e)}")


def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()