import random

# Step 2: Generate 10 unique random numbers between 1 and 100
random_numbers = random.sample(range(1, 101), 10)

# Step 3: Find the largest number
largest_number = max(random_numbers)

# Step 4: Output the result
print("The largest number is:", largest_number)