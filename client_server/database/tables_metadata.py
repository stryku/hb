from database.table_type import TableType


class ReceiptsTableMetadata:
    @staticmethod
    def get_columns():
        return [
            'id INTEGER PRIMARY KEY',
            'name varchar(255)',
            'original_name varchar(255)',
            'status int DEFAULT 0'
        ]

    @staticmethod
    def get_name():
        return 'Receipts'


class ExtractedReceiptsTextsTableMetadata:
    @staticmethod
    def get_columns():
        return [
            'id INTEGER PRIMARY KEY',
            'receipt_id int',
            'txt text',
            'status int DEFAULT 0'
        ]

    @staticmethod
    def get_name():
        return 'ExtractedReceiptTexts'


class ShopsTableMetadata:
    @staticmethod
    def get_columns():
        return [
            'id INTEGER PRIMARY KEY',
            'name varchar(255)'
        ]

    @staticmethod
    def get_name():
        return 'Shops'


class ProductsTableMetadata:
    @staticmethod
    def get_columns():
        return [
            'id INTEGER PRIMARY KEY',
            'shop_id int',
            'name varchar(255)'
        ]

    @staticmethod
    def get_name():
        return 'Products'


class ExpensesTableMetadata:
    @staticmethod
    def get_columns():
        return [
            'id INTEGER PRIMARY KEY',
            'product_id int',
            'piece_price REAL',
            'amount REAL',
        ]

    @staticmethod
    def get_name():
        return 'Expenses'


class TablesMetadataFactory:
    @staticmethod
    def create(table_type):
        return {
            TableType.RECEIPTS: ReceiptsTableMetadata(),
            TableType.EXTRACTED_RECEIPTS_TEXTS: ExtractedReceiptsTextsTableMetadata(),
            TableType.SHOPS: ShopsTableMetadata(),
            TableType.PRODUCTS: ProductsTableMetadata(),
            TableType.EXPENSES: ExpensesTableMetadata()
        }[table_type]
