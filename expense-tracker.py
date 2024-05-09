import argparse

from db_functions import connect_db
from expenses import get_expense_data, categorize_expenses, calculate_categorical_expenses
from constants import DEFAULT_DB


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

    parser.add_argument('-db', '--database',
                        type=str,
                        help='Path to database used for categorizing the inputted expenses.',
                        default=DEFAULT_DB)

    parsed_args = parser.parse_args()

    if parsed_args.month is not None and not (1 <= parsed_args.month <= 12):
        print('Error: month must be in range [1-12] but received value {}.'.format(parsed_args.month))
        exit(1)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    expense_dfs = get_expense_data(args)
    connection, cursor = connect_db(args.database)
    skipped = categorize_expenses(expense_dfs, connection, cursor)
    calculate_categorical_expenses(expense_dfs, skipped)
