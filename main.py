import socket

def create_board():
    return [["~"] * 5 for _ in range(5)]

def print_boards(my_board, enemy_hidden_board):
    """
    Displays the player's board and the enemy's tracking board side-by-side.
    Iterates through each row (i) and joins the list elements into a string.
    """
    print("\n  MY BOARD       ENEMY BOARD")
    for i in range(5):
        # We use [i] for both boards so that the rows align correctly.
        # (Note: changed 'enemy_hidden_board[1]' to 'enemy_hidden_board[i]')
        print(f"{' '.join(my_board[i])}   |   {' '.join(enemy_hidden_board[i])}")

def main():
    # --- Network Setup ---
    # Asks the user to define their role:
    # 's' (Server) will wait for a connection, 'c' (Client) will attempt to connect.
    choice = input("Host (s) or Join (c)? ").lower()

    # Creates a 'Socket' object:
    # socket.AF_INET: Specifies the address family (IPv4).
    # socket.SOCK_STREAM: Specifies the protocol (TCP), ensuring data arrives reliably and in order.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if choice == 's':
        # --- SERVER ROLE (The Host) ---
        # Automatically finds the local IP address of your computer on the Wi-Fi network
        host_ip = socket.gethostbyname(socket.gethostname())
        print(f"Hosting! Your IP is: {host_ip}")
        # Binds the socket to the IP and a specific Port (5555) so it knows where to listen
        s.bind((host_ip, 5555))
        # Tells the computer to start listening for exactly 1 incoming connection request
        s.listen(1)
        # This line "pauses" the program until a client connects;
        # 'conn' is the specific connection used to send/receive data
        conn, addr = s.accept()
        print(f"Connected to {addr}")
        turn = True  # The host traditionally takes the first shot
    else:
        # --- CLIENT ROLE (The Joiner) ---
        # Asks for the Host's IP (which the host sees printed on their screen)
        ip = input("Enter Host IP: ")
        # Attempts to knock on the Host's door at the same Port (5555)
        s.connect((ip, 5555))
        # Sets 'conn' to the socket itself so the logic below works the same for both players
        conn = s
        turn = False  # The client waits for the host to shoot first

        # --- Game Setup ---
        # Initializes a 5x5 grid for the player's own ships ('~' represents water)
        my_board = create_board()
        # Initializes a separate 5x5 grid to track shots fired at the opponent
        # This stays empty until we start receiving "HIT" or "MISS" feedback
        enemy_hidden = create_board()

        print("Place your ship (Row and Col 0-4):")
        # Takes user input, splits it (e.g., "1 2" becomes ["1", "2"]),
        # and converts both strings into integers for list indexing
        ship_r, ship_c = map(int, input("Enter row and col (e.g. 1 2): ").split())
        # Places the ship "S" at the chosen coordinates on your private board
        my_board[ship_r][ship_c] = "S"

    # --- Battle Loop ---