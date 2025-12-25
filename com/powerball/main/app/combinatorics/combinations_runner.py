from com.powerball.main.app.combinatorics.combinations_generator import CombinationsGenerator

def generate_combinations_csv():
    """
    Executes the combination generation process.
    Defining pools and triggering the generator.
    """
    # Define the input data pools here
    numbers_pool = [i for i in range(1, 69 + 1)]
    extras_pool = [4, 5, 9, 14, 18, 21, 24]
    extras_pool = [-1]
    positional_filters = {
        1: [4, 5, 8, 9], # 3
        2: [11, 12, 15, 17, 21, 23, 30], # 4
        3: [27, 31, 33, 39, 47], # 8
        4: [36, 46, 47, 51, 52, 53, 61], # 4
        5: [63, 65, 67, 68, 69] # 4
    }

    CombinationsGenerator.generate_combinations(numbers_pool, extras_pool, positional_filters)
