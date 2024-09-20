from pyscript import document
import random
import card_matrix
# this array stores all possible numbers the caller can call, and should be shuffled during reset
all_bingo_numbers = []  # Bingo numbers from 1 to 75
# this array stores the numbers that have been called this game.
called_numbers = []
# this array stores the 25 numbers generated for the bingo card
card_numbers = []

# EVENTS
def reset_game(event):
    print("calling 'reset_game'")
    shuffle_caller()
    reset_calls()
    generate_card()

def check_cell(event):
    print("calling 'check_cell'")
    cell_id = event.target.id
    cell_val = int(event.target.innerHTML)

    listr = cell_id.split("_")
    x = int(listr[1])
    y = int(listr[2])
    # Highlight the cell if it is in called_numbers

    if cell_val in called_numbers and not card_matrix.is_position_marked(x, y):
        highlight_card_cell(f'#{cell_id}')
        game_won = card_matrix.mark_position(x, y)
        if game_won:
            document.querySelector("#win_game").showModal()
    else:
        reset_card_cell(f'#{cell_id}')

def call_next(event):
    global all_bingo_numbers
    print("calling 'call_next'")

    if all_bingo_numbers:
        next_call = all_bingo_numbers.pop(0)  # Get the next number
        add_called(next_call)
        highlight_caller_cell(f"#caller{next_call}")  # Highlight the caller cell
        document.getElementById('next-call').innerHTML = str(next_call)  # Display next call
    else:
        print("All numbers have been called!")

# INTERNAL FUNCTIONS
def shuffle_caller():
    global all_bingo_numbers
    all_bingo_numbers = list(range(1, 76))
    random.shuffle(all_bingo_numbers)
    print("Caller numbers shuffled.")
    for number in all_bingo_numbers:
        reset_caller_cell(f'#caller{number}')

def reset_calls():
    global called_numbers
    document.querySelector("#next-call").innerHTML = ""
    called_numbers = []  # Clear the called numbers
    print("Called numbers reset.")

def generate_card():
    global card_numbers
    card_numbers = list(range(1, 76))[:25]
    random.shuffle(card_numbers)  # Generate 25 unique numbers
    for i in range(5):  # Assuming a 5x5 card layout
        for j in range(5):
            cell_id = f'#cell_{i+1}_{j+1}'  # Example cell ID
            print(cell_id)
            document.querySelector(cell_id).innerHTML = card_numbers.pop()
            reset_card_cell(cell_id)
    print("Bingo card generated.")

def add_called(num):
    global called_numbers
    called_numbers.append(num)  # Add number to called numbers
    print(f"Number {num} has been called.")

# adds/removes highlight CSS classes from cells (these are complete, don't change)
def highlight_card_cell(cell_id):
    document.querySelector(cell_id).className = "highlight-card"

def reset_card_cell(cell_id):
    document.querySelector(cell_id).className = ""

def highlight_caller_cell(cell_id):
    document.querySelector(cell_id).className = "highlight-caller"

def reset_caller_cell(cell_id):
    document.querySelector(cell_id).className = ""

# initial setup
reset_game(0)
