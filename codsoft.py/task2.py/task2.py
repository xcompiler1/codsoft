"""
Simple Command-Line Calculator
Prompts user for two numbers and an operation, then displays the result.
"""

import math

def display_menu():
    """Display available operations"""
    print("\n" + "="*50)
    print("          SIMPLE CALCULATOR")
    print("="*50)
    print("\nAvailable Operations:")
    print("  1. Addition (+)")
    print("  2. Subtraction (-)")
    print("  3. Multiplication (*)")
    print("  4. Division (/)")
    print("  5. Modulus (%)")
    print("  6. Power (^)")
    print("  7. Square Root (√)")
    print("  0. Exit")
    print("="*50)

def get_number(prompt):
    """Get a valid number from user"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")

def get_operation():
    """Get operation choice from user"""
    while True:
        try:
            choice = int(input("\nSelect operation (0-7): "))
            if 0 <= choice <= 7:
                return choice
            else:
                print("❌ Invalid choice! Please select a number between 0 and 7.")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")

def add(num1, num2):
    """Addition operation"""
    return num1 + num2

def subtract(num1, num2):
    """Subtraction operation"""
    return num1 - num2

def multiply(num1, num2):
    """Multiplication operation"""
    return num1 * num2

def divide(num1, num2):
    """Division operation"""
    if num2 == 0:
        return "Error: Cannot divide by zero!"
    return num1 / num2

def modulus(num1, num2):
    """Modulus operation"""
    if num2 == 0:
        return "Error: Cannot perform modulus with zero!"
    return num1 % num2

def power(num1, num2):
    """Power operation"""
    try:
        return num1 ** num2
    except OverflowError:
        return "Error: Result too large!"

def square_root(num):
    """Square root operation"""
    if num < 0:
        return "Error: Cannot calculate square root of negative number!"
    return math.sqrt(num)

def calculate():
    """Main calculation function"""
    while True:
        display_menu()
        
        operation = get_operation()
        
        # Exit option
        if operation == 0:
            print("\n👋 Thank you for using the calculator. Goodbye!")
            break
        
        # Get numbers based on operation
        if operation == 7:  # Square root only needs one number
            num1 = get_number("\nEnter a number: ")
            result = square_root(num1)
            operation_symbol = "√"
            expression = f"√{num1}"
        else:
            num1 = get_number("\nEnter first number: ")
            num2 = get_number("Enter second number: ")
            
            # Perform calculation based on choice
            if operation == 1:
                result = add(num1, num2)
                operation_symbol = "+"
            elif operation == 2:
                result = subtract(num1, num2)
                operation_symbol = "-"
            elif operation == 3:
                result = multiply(num1, num2)
                operation_symbol = "*"
            elif operation == 4:
                result = divide(num1, num2)
                operation_symbol = "/"
            elif operation == 5:
                result = modulus(num1, num2)
                operation_symbol = "%"
            elif operation == 6:
                result = power(num1, num2)
                operation_symbol = "^"
            
            expression = f"{num1} {operation_symbol} {num2}"
        
        # Display result
        print("\n" + "-"*50)
        if isinstance(result, str):  # Error message
            print(f"❌ {result}")
        else:
            # Format result nicely
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            print(f"✅ Result: {expression} = {result}")
        print("-"*50)
        
        # Ask if user wants to continue
        continue_calc = input("\nDo you want to perform another calculation? (yes/no): ").lower()
        if continue_calc not in ['yes', 'y']:
            print("\n👋 Thank you for using the calculator. Goodbye!")
            break

def main():
    """Main function"""
    try:
        calculate()
    except KeyboardInterrupt:
        print("\n\n👋 Calculator interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()