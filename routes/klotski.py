from flask import Blueprint, request, jsonify

# Create a Blueprint for the klotski routes
klotski_bp = Blueprint('klotski', __name__)

def move_block_on_board(board, block, direction):
    block_positions = [i for i, char in enumerate(board) if char == block]
    
    direction_map = {
        'N': -4,   # Move up by one row (4 positions back)
        'S': 4,    # Move down by one row (4 positions forward)
        'W': -1,   # Move left by one position
        'E': 1     # Move right by one position
    }
    
    shift = direction_map[direction]
    
    board_list = list(board)
    
    # First, remove the block from the board (set to '@')
    for pos in block_positions:
        board_list[pos] = '@'
    
    # Move the block to the new position
    new_positions = []
    for pos in block_positions:
        new_pos = pos + shift
        
        if direction == 'W' and pos % 4 == 0:
            continue
        if direction == 'E' and (pos + 1) % 4 == 0:
            continue
        
        new_positions.append(new_pos)

    for new_pos in new_positions:
        if board_list[new_pos] == '@' or board_list[new_pos] < block:
            board_list[new_pos] = block

    return ''.join(board_list)

def apply_moves(board_str, moves_str):
    board = board_str
    for i in range(0, len(moves_str), 2):
        block = moves_str[i]
        direction = moves_str[i+1]
        board = move_block_on_board(board, block, direction)
    
    return board

@klotski_bp.route('/klotski', methods=['POST'])
def klotski_handler():
    request_data = request.get_json()
    
    results = []
    for item in request_data:
        board = item["board"]
        moves = item["moves"]
        result_board = apply_moves(board, moves)
        results.append(result_board)
    
    return jsonify(results)