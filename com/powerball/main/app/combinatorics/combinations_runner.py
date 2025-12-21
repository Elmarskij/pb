from com.powerball.main.app.combinatorics.combinations_generator import CombinationsGenerator

def generate_combinations_csv():
    """
    Executes the combination generation process.
    Defining pools and triggering the generator.
    """
    # Define the input data pools here
    numbers_pool = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]
    extras_pool = [1, 3, 4, 5, 9, 14, 18, 20, 21, 24, 25]
    extras_pool = [-1]
    positional_filters = {
        1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], # 3
        2: [12, 13, 14, 15, 16, 17, 18, 20, 21, 23, 25, 28, 30], # 4
        3: [20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 50], # 8
        4: [39, 44, 45, 46, 47, 48, 50, 51, 52, 53, 55, 59, 61], # 4
        5: [58, 61, 62, 63, 64, 65, 66, 67, 68, 69] # 4
    }

    CombinationsGenerator.generate_combinations(numbers_pool, extras_pool, positional_filters)
