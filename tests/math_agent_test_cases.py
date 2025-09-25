BENCHMARK_TEST_CASES = [
    # Basic operation benchmarks
    {
        "category": "Addition",
        "test_cases": [
            {"message": "What is 5 + 7?", "expected": 12},
            {"message": "What is 123 + 456?", "expected": 579},
            {"message": "What is 9999 + 1?", "expected": 10000},
            {"message": "What is -25 + 50?", "expected": 25},
            {"message": "What is 0 + 0?", "expected": 0},
            {"message": "Add 42 and 58", "expected": 100},
            {"message": "Can you tell me the sum of 721 and 279?", "expected": 1000},
            {"message": "What's the result if I add -15 to -25?", "expected": -40},
            {"message": "If I have 785 and add 215 more, what do I get?", "expected": 1000},
            {"message": "What is the total of 133, 267, and 400?", "expected": 800}
        ]
    },
    {
        "category": "Multiplication",
        "test_cases": [
            {"message": "What is 6 × 8?", "expected": 48},
            {"message": "What is 25 * 4?", "expected": 100},
            {"message": "Multiply 13 by 11", "expected": 143},
            {"message": "What is the product of 99 and 99?", "expected": 9801},
            {"message": "What happens if I multiply 1000 by 0?", "expected": 0},
            {"message": "Calculate 17 multiplied by 23", "expected": 391},
            {"message": "What's -15 times 4?", "expected": -60},
            {"message": "If I multiply 0.5 by 10, what do I get?", "expected": 5},
            {"message": "What is 111 × 111?", "expected": 12321},
            {"message": "Compute the result of multiplying 256 by 16", "expected": 4096}
        ]
    },
    {
        "category": "Chained Operations",
        "test_cases": [
            {"message": "What is 5 + 7 + 3?", "expected": 15},
            {"message": "Calculate 4 × 5 + 10", "expected": 30},
            {"message": "What is 10 + 20 × 3?", "expected": 70},
            {"message": "Find the value of 5 × (3 + 2)", "expected": 25},
            {"message": "What is (7 + 3) × (8 + 2)?", "expected": 100},
            {"message": "Compute 25 × 4 + 50 × 2", "expected": 200},
            {"message": "If I add 5 and 7, then multiply by 3, what do I get?", "expected": 36},
            {"message": "What is the result of multiplying 6 by 4, then adding 12?", "expected": 36},
            {"message": "Calculate (10 + 15) × (20 + 5)", "expected": 625},
            {"message": "What's 100 + 50 × 2?", "expected": 200}
        ]
    },
    {
        "category": "Word Problems",
        "test_cases": [
            {"message": "If I have 12 boxes with 8 items each, how many items do I have in total?", "expected": 96},
            {"message": "Sarah has 45 dollars and gets 30 more from her parents. How much does she have now?", "expected": 75},
            {"message": "A theater has 25 rows with 30 seats in each row. How many seats are there in total?", "expected": 750},
            {"message": "John bought 3 books for 15 dollars each. How much did he spend in total?", "expected": 45},
            {"message": "A farmer has 7 fields with 12 cows in each field. If he adds 4 more cows to each field, how many cows does he have in total?", "expected": 112},
            {"message": "If a train travels at 60 miles per hour for 5 hours, how far will it travel?", "expected": 300},
            {"message": "A school ordered 24 boxes of pencils. If each box contains 12 pencils, how many pencils did they order?", "expected": 288},
            {"message": "Maria has 120 candies and wants to distribute them equally among 8 friends. How many candies will each friend receive?", "expected": 15},
            {"message": "If a shirt costs $25 and you buy 4 shirts, how much will you spend?", "expected": 100},
            {"message": "A recipe calls for 3 cups of flour. If you want to make 5 batches, how many cups of flour will you need?", "expected": 15}
        ]
    },
    {
        "category": "Unsupported Operations",
        "test_cases": [
            {"message": "What is the square of 5?", "expected": 25},  # Can be done as 5 * 5
            {"message": "What is 10 divided by 2?", "expected": 5},   # Not directly supported, but simple division
            {"message": "What is the square root of 16?", "expected": 4},  # Not directly supported
            {"message": "What is 2 raised to the power of 3?", "expected": 8},  # Can be done as 2 * 2 * 2
            {"message": "What is 5 minus 3?", "expected": 2},  # Not directly supported
            {"message": "Calculate 10 divided by 4", "expected": 2.5},  # Not directly supported
            {"message": "What is 3 to the power of 4?", "expected": 81},  # Can be done as 3 * 3 * 3 * 3
            {"message": "What is the remainder when 17 is divided by 5?", "expected": 2},  # Not directly supported
            {"message": "What is the cube root of 27?", "expected": 3},  # Not directly supported
            {"message": "What is log base 10 of 100?", "expected": 2}  # Not directly supported
        ]
    },
    {
        "category": "Edge Cases",
        "test_cases": [
            {"message": "What is the result of 9999999 + 1?", "expected": 10000000},  # Large numbers
            {"message": "What happens if I multiply a number by zero?", "expected": 0},  # Zero multiplication
            {"message": "What is the largest number you can add?", "expected": None},  # Testing agent limits
            {"message": "Add 0.1 and 0.2", "expected": 0.3},  # Floating point addition
            {"message": "Multiply 0.1 by 0.1", "expected": 0.01},  # Floating point multiplication
            {"message": "What is -5 + (-10)?", "expected": -15},  # Negative number addition
            {"message": "What is -7 * 8?", "expected": -56},  # Negative number multiplication
            {"message": "If I have no apples and get no more apples, how many do I have?", "expected": 0},  # Zero conceptual test
            {"message": "What is 1000000 * 1000000?", "expected": 1000000000000},  # Very large result
            {"message": "Can you add 'five' and 'seven'?", "expected": None}  # Non-numeric input
        ]
    }
]
