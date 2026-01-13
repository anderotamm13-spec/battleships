import socket
import hexcode as hc

def create_board():
    return [["~"] * 5 for _ in range(5)]

def print_boards(my_board, enemy_hidden_board):

    print("\n  MY BOARD       ENEMY BOARD")
    for i in range(5):
        # We use [i] for both boards so that the rows align correctly.
        # (Note: changed 'enemy_hidden_board[1]' to 'enemy_hidden_board[i]')
        print(f"{' '.join(my_board[i])}   |   {' '.join(enemy_hidden_board[i])}")

def main():
    # --- Network Setup ---
    # 's' (Server) will wait for a connection, 'c' (Client) will attempt to connect.
    choice = input("Host (s) or Join (c)? ").lower()


    # socket.SOCK_STREAM: Specifies the protocol (TCP), ensuring data arrives reliably and in order.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if choice == 's':
        # --- SERVER ROLE (The Host) ---
        # Automatically finds the local IP address of your computer on the Wi-Fi network
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host_ip = ip #socket.gethostbyname(socket.gethostname())
        print(f"Hosting! Your join code is: {hc.encode(host_ip)}")
        # Binds the socket to the IP and a specific Port (5555) so it knows where to listen
        s.bind((host_ip, 5555))
        # Tells the computer to start listening for exactly 1 incoming connection request
        s.listen(1)
        # This line "pauses" the program until a client connects;
        # 'conn' is the specific connection used to send/receive data
        conn, addr = s.accept()
        print(f"Connected to {addr}")
        turn = True
    else:
        # --- CLIENT ROLE (The Joiner) ---
        ip = hc.decode(input("Enter Host IP: "))
        s.connect((ip, 5555))
        conn = s
        turn = False

        # comment

        # --- Game Setup ---

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
    while True:
        print_boards(my_board, enemy_hidden)

        if turn:
            print("YOUR TURN!")
            shot = input("Enter target row and col: ")
            conn.send(shot.encode())
            result = conn.recv(1024).decode()
            print(f"Result: {result}")

            r, c = map(int, shot.split())
            enemy_hidden[r][c] = "X" if result == "HIT!" else "O"
            if result == ("WIN"):
                print("YOU WIN!")
                break
            turn = False
            break
        else:
            print("WAITING FOR ENEMY...")
            data = conn.recv(1024).decode()
            r, c = map(int, data.split())

            if r == ship_r and c == ship_c:
                res = "WIN" if my_board[r][c] == "S" else "HIT"
                my_board[r][c] = "X"
                conn.send(res.encode())
                print("THEY HIT YOU! YOU LOSE.")
                break
            else:
                my_board[r][c] = "O"
                conn.send("MISS".encode())
                turn = True

    conn.close()

if __name__ == "__main__":
    main()
