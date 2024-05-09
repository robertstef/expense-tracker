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
    all = [('phone', 'p'),
           ('internet', 'i'),
           ('loans', 'l'),
           ('utilities', 'u'),
           ('gas', 'g'),
           ('groceries', 'gr'),
           ('vehicle', 'v'),
           ('entertainment', 'e'),
           ('extras', 'ex'),
           ('clothing', 'c'),
           ('subscriptions', 's'),
           ('restaurants', 'r')]

    def __init__(self):
        self.full_to_short = {f: s for f, s in self.all}
        self.short_to_full = {s: f for f, s in self.all}

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
        for full, short in sorted(self.all, key=lambda x: x[0]):
            print('- {} ({})'.format(full, short))
        print()
