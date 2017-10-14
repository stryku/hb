from database.tables_metadata import TablesMetadataFactory


class CreationQueryBuilder:
    def __init__(self):
        self.query = ''
        self.table_name = ''
        self.columns = []

    def _build_columns(self):
        result = ''
        separator = ''
        for column in self.columns:
            result += '{} {}'.format(separator, column)
            separator = ','

        return result

    def with_table_name(self, name):
        self.table_name = name
        return self

    def with_column(self, column):
        self.columns.append(column)
        return self

    def with_columns(self, columns):
        self.columns += columns
        return self

    def build(self):
        if len(self.table_name) == 0:
            raise Exception('Missing table name')

        return 'CREATE TABLE IF NOT EXISTS {} ({});'.format(self.table_name,
                                                            self._build_columns())


class CreationQueryFactory:
    @staticmethod
    def _create_from_metadata(metadata):
        return CreationQueryBuilder() \
            .with_columns(metadata.get_columns()) \
            .with_table_name(metadata.get_table_name()) \
            .build()

    @staticmethod
    def create(table_type):
        table_metadata = TablesMetadataFactory.create(table_type)
        return CreationQueryFactory._create_from_metadata(table_metadata)


def get_table_name(table_type):
    return TablesMetadataFactory.create(table_type).get_name()
