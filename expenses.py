import os
import pandas as pd
from constants import CsvCols, Categories
from db_functions import add_vendors_to_db, get_vendors_to_add


def get_expense_data(args):
    """
    Reads in the expense data and parses it into a list dataframes.
    If a month is supplied in the cmd line args, only the data for
    the specified month will be returned, otherwise each month will
    be parsed into its own dataframe.

    :param: NameSpace args: cmd line arguments
    :return: A list dataframes containing all the requested expense data
    :rtype: List[pd.DataFrame]
    """
    df = _parse_expense_csvs(args.expenses)

    if args.month is not None:
        return [df[df['date'].dt.month == args.month]]

    num_years = len(set(df['date'].dt.year))
    if num_years > 1:
        print('Error: found multiple years in input data. Currently, only data from the same year is supported.')
        exit(1)

    all_months = sorted(set(df['date'].dt.month))
    return list(
        df[df['date'].dt.month == month] for month in all_months
    )


def categorize_expenses(expense_dfs, connection, cursor):
    """
    Categorizes the expenses for each dataframe of expense data.
    If one or more transactions does not appear in the database,
    the user will be prompted to either categorize or skip them.

    :param List[pd.DataFrame] expense_dfs: expenses to categorize
    :param sqlite3.Connection connection: connection to expense database
    :param sqlite3.Cursor cursor: cursor pointing to expense database

    """
    all_skipped = list()
    for df in expense_dfs:
        vendors_to_add = get_vendors_to_add(df, cursor)
        if len(vendors_to_add) == 0:
            continue

        categorized_vendors, skipped = _add_vendor_repl(vendors_to_add)
        if len(categorized_vendors) > 0:
            add_vendors_to_db(connection, cursor, categorized_vendors)

        all_skipped.extend(skipped)

    return all_skipped


def calculate_categorical_expenses(dfs, skipped):
    pass


def _parse_expense_csvs(csvs):
    """
    Reads the provided expense csv files into a dataframe
    :param List[str] csvs: list of csv files to parse
    :return: A dataframe with all the CSV information
    :rtype: DataFrame
    """
    col_names = CsvCols.cols()

    def str_to_float(x):
        return 0 if x == '' else float(x)

    converters = {
        CsvCols.DATE: pd.to_datetime,
        CsvCols.VENDOR: str,
        CsvCols.DEBIT: str_to_float,
        CsvCols.CREDIT: str_to_float,
        CsvCols.BALANCE: str_to_float
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
                        converters=converters)
        )

    if len(expense_data) == 0:
        exit(1)

    return pd.concat(expense_data)


def _add_vendor_repl(vendors_to_add):
    """
    A repl that will prompt the user to categorize the given vendors.
    :param List[str] vendors_to_add: list of vendors that need to be categorized
    :return: A list of tuples of vendors and their categories where each tuple is
             of the form (vendor, category) and a list of the skipped vendors.
    :rtype: List[Tuple[str, str]], List[str]
    """
    print('There are {} expenses to categorize.\n'
          'Options:\n'
          '  - help (h): list expense categories\n'
          '  - skip (sk): skip current expense\n'
          '  - exit: exit program\n'.format(len(vendors_to_add)))

    cat_helper = Categories()
    vendors_and_categories = list()
    skipped = list()

    i = 0
    while i < len(vendors_to_add):
        vendor = vendors_to_add[i]
        res = input('{}. {}\n'
                    '>> '.format(i + 1, vendor))

        if res == 'help' or res == 'h':
            cat_helper.print_categories()
            continue

        if res == 'skip' or res == 'sk':
            skipped.append(vendor)
            continue

        if res == 'exit':
            print('exiting program')
            exit(1)

        # For testing
        if res == 'stop':
            break

        category = cat_helper.get_full_name(res)
        if category is None:
            print('Invalid category - try again.')
            continue

        vendors_and_categories.append((vendor, category))
        i += 1

    return vendors_and_categories, skipped


