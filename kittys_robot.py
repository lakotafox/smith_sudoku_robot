import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import subprocess
import textwrap


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
         "But they that wait upon the Lord shall renew their strength;\nthey shall mount up with wings as eagles; they shall run,\nand not be weary; and they shall walk, and not faint.")
    ]
    
    return random.choice(inspirations)


def generate_sudoku():
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

    squares = side * side
    empties = squares * 3 // 4
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0

    solution = [[nums[pattern(r, c)] for c in cols] for r in rows]

    return board, solution


def draw_sudoku(c, sudoku, x_offset, y_offset, title, block_size=30, center_title=False, page_width=612):
    c.setFont("Helvetica-Bold", 16)
    if center_title and title:
        text_width = c.stringWidth(title, "Helvetica-Bold", 16)
        title_x = (page_width - text_width) / 2
        c.drawString(title_x, y_offset + 40, title)
    elif title:
        c.drawString(x_offset, y_offset + 40, title)

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


def create_pdf(puzzle, solution, filename="sudoku_print.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    block_size = 36

    puzzle_width = block_size * 9
    x_offset = (width - puzzle_width) // 2

    # Draw title centered at top of first page
    draw_sudoku(c, puzzle, x_offset=x_offset, y_offset=height - 75, 
                title="Kitty's Sudoku Puzzle", block_size=block_size, 
                center_title=True, page_width=width)

    # Draw second copy of puzzle below the first (for final draft)
    draw_sudoku(c, puzzle, x_offset=x_offset, y_offset=height - 420, 
                title="", block_size=block_size)

    # Start new page for solution
    c.showPage()
    
    # Draw solution on second page
    draw_sudoku(c, solution, x_offset=x_offset, y_offset=height - 75, 
                title="Solution", block_size=block_size,
                center_title=True, page_width=width)
    
    # Add inspiration below solution
    draw_inspiration(c, height - 500, width)
    
    c.save()


def print_pdf(filename):
    if os.name == 'posix':
        subprocess.run(["lp", filename])
    elif os.name == 'nt':
        os.startfile(filename, "print")
    else:
        print("Printing not supported on this OS")


def main():
    puzzle, solution = generate_sudoku()
    create_pdf(puzzle, solution)
    # print_pdf("sudoku_print.pdf")  # Commented out for testing
    print("PDF created: sudoku_print.pdf")


if __name__ == "__main__":
    main()