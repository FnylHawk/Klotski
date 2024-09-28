from flask import Flask, request, jsonify

app = Flask(__name__)

def move_block_on_board(board, block, direction):
    # Find all positions of the block in the board string
    block_positions = [i for i, char in enumerate(board) if char == block]
    
    # Define how to change index for each direction (N, S, W, E)
    direction_map = {
        'N': -4,   # Move up by one row (4 positions back)
        'S': 4,    # Move down by one row (4 positions forward)
        'W': -1,   # Move left by one position
        'E': 1     # Move right by one position
    }
    
    shift = direction_map[direction]
    
    # Create a list of characters for board manipulation
    board_list = list(board)
    
    # Move the block by shifting each position
    for pos in block_positions:
        new_pos = pos + shift
        
        # Handle edge cases: Moving left or right across row boundaries
        if direction == 'W' and pos % 4 == 0:
            continue  # Can't move left from the first column
        if direction == 'E' and (pos + 1) % 4 == 0:
            continue  # Can't move right from the last column
        
        # Move the block to the new position
        board_list[pos] = '@'  # Vacate the original position
        if board_list[new_pos] == '@' or board_list[new_pos] < block:
            board_list[new_pos] = block  # Place the block in the new position if it is greater or the spot is empty
    
    return ''.join(board_list)

def apply_moves(board_str, moves_str):
    board = board_str
    # Process moves in pairs: block and direction
    for i in range(0, len(moves_str), 2):
        block = moves_str[i]
        direction = moves_str[i+1]
        board = move_block_on_board(board, block, direction)
    
    return board

@app.route('/klotski', methods=['POST'])
def klotski_handler():
    # Get JSON data from request
    request_data = request.get_json()
    
    results = []
    for item in request_data:
        board = item["board"]
        moves = item["moves"]
        result_board = apply_moves(board, moves)
        results.append(result_board)
    
    # Return results as JSON response
    return jsonify(results)

if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True)
