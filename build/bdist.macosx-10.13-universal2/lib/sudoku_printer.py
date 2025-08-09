import random  # conjoure logic of random number into this universe

from reportlab.pdfgen import canvas  # conjure pdf generation tools

from reportlab.lib.pagesizes import letter  # tool for "standerd" letter page size (8.5x11 inches, 612x792 points)

import os # conjure operating system tools IDFK what this does tbh

import subprocess #subprocess... tool used to run puter "user style" commands (wtf am I saying),  stuff user does like "printing" puter does automatically with this tool... maybe idfk


#mother of all sudoku generation methods/functions. (cob creates personal tool tis algorithm) will be used for program l8r
def generate_sudoku():
    base = 3                  # size of  cube (3x3)
    side = base * base        #  size of the grid (9x9)

    # mother algorithm for a complete valid Sudoku
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # shuffles
    def shuffle(s):
        return random.sample(s, len(s))
#shuffleing with algs
    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, side + 1))

    # assign board with maths
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # 75% of the blocks emptied for the puzzle
    squares = side * side
    empties = squares * 3 // 4
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0

    #  solution is the same as the fully filled board
    solution = [[nums[pattern(r, c)] for c in cols] for r in rows]

    return board, solution
# drawing func takes x and y postions title, and block size
def draw_sudoku(c, sudoku, x_offset, y_offset, title, block_size=30):
   # title font, size and psotion 
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_offset, y_offset + 40, title)

    c.setFont("Helvetica", 20)  # size for numbers

    # Draw the 9x9 grid
    for i in range(9):
        for j in range(9):
            x = x_offset + j * block_size
            y = y_offset - i * block_size
            c.rect(x, y, block_size, block_size)
            if sudoku[i][j] != 0:
                c.drawString(x + block_size // 3, y + block_size // 4, str(sudoku[i][j]))

# creates a PDF func for later use in the program
def create_pdf(puzzle, solution, filename="sudoku_print.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    block_size = 36  # change cell size for larger puzzle

    puzzle_width = block_size * 9
    x_offset = (width - puzzle_width) // 2  # 

    # draw puzzle near top
    draw_sudoku(c, puzzle, x_offset=x_offset, y_offset=height - 75, 
                title="Hi Grandma I love you!", block_size=block_size)

    # draw answer below the puzzle
    draw_sudoku(c, solution, x_offset=x_offset, y_offset=height - 466, 
                title="Don't look until you're ready!", block_size=block_size)
    c.save()

# sends the puzzle to the users default printer

# bot code for using windows or linux.
def print_pdf(filename):
    if os.name == 'posix':
        subprocess.run(["lp", filename])
    elif os.name == 'nt':
        os.startfile(filename, "print")
    else:
        print(" sorry this program is to shite to work on your OS, please use create new hardware, Write a new os, and build your own language, from scratch. do it yourself you rat bastard")


# main func squash all ideas together calling all other functions and variables
def main():
    puzzle, solution = generate_sudoku()
    create_pdf(puzzle, solution) # create pdf func called
    print_pdf("sudoku_print.pdf")


# this if "checks" and makes sure main() only runs when this file is executed
# not when it is imported for use in other files
if __name__ == "__main__":
    main()