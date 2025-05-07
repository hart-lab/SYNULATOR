"""
This file formats and writes the output for the tool
"""


from pandas import DataFrame


def write_fitness_table(fitness_table: DataFrame, output_filepath: str, float_format: str = '%4.3f',
                         sep: str = '\t') -> None:
    """
    Writes simulation results to .csv

    Parameters:
        fitness_table: DataFrame
            instance of `DataFrame` representing the simulation results
        output_filepath: str
            string of the filepath to which data is written
        float_format: str
            string of the format for the floats (default = "%4.3f")
        sep: str
            string separator (default = "\t")
    """
    numeric_columns = fitness_table.select_dtypes(include=['float', 'int']).columns
    
    formatted_fitness_table = fitness_table.copy()
    formatted_fitness_table[numeric_columns] = formatted_fitness_table[numeric_columns].apply(lambda col: col.map(lambda x: float_format % x))
    formatted_fitness_table.to_csv(output_filepath, sep=sep, index=True)
