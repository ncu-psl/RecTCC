class table_manager(object):

    def __init__(self):
        self.table_list = []
        

class symbol_table(object):

    def __init__(self):
        self.table = {}

    def update(self, symbol: symbol):
        self.table.update({symbol.name: symbol.value})

    def get_symbol_value(self, symbol_name: str):
        return self.table[symbol_name]
        

class symbol():

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
