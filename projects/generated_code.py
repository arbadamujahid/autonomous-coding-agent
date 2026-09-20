# Step 5: Write the code
def check_even_odd(number):
    # Step 5.1: Determine if the number is even or odd
    if number % 2 == 0:
        print(f"{number} is even.")
    else:
        print(f"{number} is odd.")

# Step 5.2: Get user input
number = int(input("Enter a number: "))

# Step 5.3: Call the function
check_even_odd(number)