DEFAULT_DB = '~/expense_tracking.db'


class CsvCols(object):
    DATE = 'date'
    VENDOR = 'vendor'
    DEBIT = 'debit'
    CREDIT = 'credit'
    BALANCE = 'balance'

    @classmethod
    def cols(cls):
        return [cls.DATE, cls.VENDOR, cls.DEBIT, cls.CREDIT, cls.BALANCE]


class Categories(object):
    all = ['phone',
           'internet',
           'loans',
           'utilities',
           'gas',
           'groceries',
           'vehicle',
           'entertainment',
           'extras',
           'clothing',
           'subscriptions',
           'restaurants']

    def __init__(self):
        self.full_to_short = dict()
        self.short_to_full = dict()

        for full_name in sorted(self.all):
            shortcut = ''
            for letter in full_name:
                shortcut += letter
                if shortcut not in self.short_to_full:
                    break
            self.full_to_short[full_name] = shortcut
            self.short_to_full[shortcut] = full_name

    def is_valid(self, category):
        return category in self.full_to_short or category in self.short_to_full

    def get_full_name(self, category):
        if category in self.full_to_short:
            return category
        elif category in self.short_to_full:
            return self.short_to_full[category]
        else:
            return None

    def print_categories(self):
        for full, short in sorted(self.full_to_short.items()):
            print('- {} ({})'.format(full, short))
        print()
