import random

def play_game():
    user_score = 0
    computer_score = 0
    options = ["rock", "paper", "scissors"]

    print("---  Rock-Paper-Scissors ---")

    while True:
        # User Input
        user_choice = input("\nChoose rock, paper, or scissors (or 'quit' to exit): ").lower()
        
        if user_choice == 'quit':
            break
        if user_choice not in options:
            print("Invalid choice! Please try again.")
            continue

        # Computer Selection
        computer_choice = random.choice(options)

        print(f"\nYou chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")

        # Game Logic
        if user_choice == computer_choice:
            print("It's a tie! ")
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "scissors" and computer_choice == "paper") or \
             (user_choice == "paper" and computer_choice == "rock"):
            print("You win! ")
            user_score += 1
        else:
            print("You lose! ")
            computer_score += 1

        # Score Tracking
        print(f"Score -> You: {user_score} | Computer: {computer_score}")

        # Play Again
        again = input("\nPlay another round? (y/n): ").lower()
        if again != 'y':
            print(f"\nFinal Score - You: {user_score} | Computer: {computer_score}")
            print("Thanks for playing! ")
            break

if __name__ == "__main__":
    play_game()