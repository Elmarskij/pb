from com.powerball.main.app.combinatorics.combinations_generator import CombinationsGenerator

def generate_combinations_csv():
    """
    Executes the combination generation process.
    Defining pools and triggering the generator.
    """
    # Define the input data pools here
    numbers_pool = [10, 21, 23, 28, 32, 33, 39, 61, 62, 63, 64, 69]
    extras_pool = [4, 18, 21, 24]

    CombinationsGenerator.generate_combinations(numbers_pool, extras_pool)
