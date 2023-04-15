import argparse
import os
import pandas as pd
import sqlite3


def parse_args():
    """
    Creates an arg parser and returns the Namespace containing the
    parsed command line arguments.
    :return: parsed cmd line arguments
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(
        prog='Expense Tracker',
        description='A program to take in expense reports and classify the expenses into general categories.'
    )

    parser.add_argument('expenses',
                        nargs='+',
                        type=str,
                        help='Expense csv\'s to process')

    parser.add_argument('-m', '--month',
                        type=int,
                        help='The month to process in the given expense csv\'s. Must be an integer in the '
                             'range [1-12].')

    parsed_args = parser.parse_args()

    if not (1 <= parsed_args.month <= 12):
        print('Error: month must be in range [1-12] but received value {}.'.format(parsed_args.month))
        exit(1)

    return parser.parse_args()


def parse_expense_csvs(csvs):
    """
    Reads the provided expense csv files into a dataframe
    :param List[str] csvs: list of csv files to parse
    :return: A dataframe with all the CSV information
    :rtype: DataFrame
    """
    col_names = ['date', 'transaction', 'debit', 'credit', 'balance']
    data_types = {
        'data': str,
        'transaction': str,
        'debit': float,
        'credit': float,
        'balance': float
    }

    def str_to_float(x):
        return 0 if x == '' else float(x)

    converters = {
        'date': pd.to_datetime,
        'debit': str_to_float,
        'credit': str_to_float,
        'balance': str_to_float
    }

    expense_data = list()
    for csv in csvs:
        abs_path = os.path.abspath(csv)
        if not os.path.exists(abs_path):
            print("The file {} does not exist, this data will not be included.".format(csv))
            continue
        expense_data.append(
            pd.read_csv(abs_path,
                        names=col_names,
                        index_col=False,
                        dtype=data_types,
                        converters=converters)
        )

    if len(expense_data) == 0:
        exit(1)

    return pd.concat(expense_data)


if __name__ == '__main__':
    args = parse_args()
    df = parse_expense_csvs(args.expenses)
