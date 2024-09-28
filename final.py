from flask import Flask, request, jsonify

app = Flask(__name__)

def move_block_on_board(board, block, direction):
    # Find all positions of the block in the board string
    block_positions = [i for i, char in enumerate(board) if char == block]
    
    # Change index for each direction (N, S, E, W)
    direction_map = {
        'N': -4,   
        'S': 4,    
        'E': 1,
        'W': -1
             
    }
    
    shift = direction_map[direction]
    
    # Create a list of characters for board manipulation
    board_list = list(board)
    
    for pos in block_positions:
        board_list[pos] = '@'
    
    # Move the block to the new position
    new_positions = []
    for pos in block_positions:
        new_pos = pos + shift
        
        # Handle edge cases: Moving left or right across row boundaries
        if direction == 'W' and pos % 4 == 0:
            continue  # Can't move left from the first column
        if direction == 'E' and (pos + 1) % 4 == 0:
            continue  # Can't move right from the last column
        
        new_positions.append(new_pos)

    # Block's new positions
    for new_pos in new_positions:
        if board_list[new_pos] == '@' or board_list[new_pos] < block:
            board_list[new_pos] = block

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
