from django.db import connection


class ExpenseRepo:
    def get_tags(self):
        try:
            with connection.cursor() as curs:
                curs.execute("select tagID,tagTEXT from tags")
                return curs.fetchall()
        except:
            return []

    def add_tag(self, tag):
        try:
            with connection.cursor() as curs:
                curs.execute("insert into tags (tagtext) values (%(tagText)s)", {"tagText": tag})
                return curs.rowcount == 1
        except:
            return False

    def add_subtag(self, tag, subtag):
        try:
            with connection.cursor() as curs:
                curs.execute("insert into subtags (tagID, subtagText) values (%(tagID)s, %(subtagText)s)", {
                             "tagID": tag,
                             "subtagText": subtag})
                return curs.rowcount == 1
        except:
            return False
    
    def add_expense(self, expense):
        try:
            balance = self.get_balance()
            expense['balance'] = balance - float(expense["amount"])
            with connection.cursor() as curs:
                curs.execute("insert into debits (amount, remainingbalance, description, tagid, subtagid) values (%(amount)s, %(balance)s, %(expense_desc)s, %(tagid)s, %(subtagid)s)", expense)
                if curs.rowcount == 1:
                    return self.update_balance(expense['balance'])
                return False
        except:
            return False

    def update_balance(self, balance):
        try:
            with connection.cursor() as curs:
                curs.execute("update balance set amount=%(balance)s", {"balance":balance})
                return curs.rowcount >= 1
        except:
            return False

    def get_subtags(self):
        try:
            with connection.cursor() as curs:
                curs.execute(
                    "select t.tagid,t.tagtext,s.subtagid,s.subtagtext from tags t left outer join subtags s on s.tagid = t.tagid;")
                return curs.fetchall()
        except:
            return []

    def get_balance(self):
        try:
            with connection.cursor() as curs:
                curs.execute("select amount from balance")
                return curs.fetchone()[0]
        except:
            return -1
    
    def get_expenses(self):
        try:
            with connection.cursor() as curs:
                curs.execute("select d.amount,d.description,t.tagtext,s.subtagtext from debits d join tags t on d.tagid = t.tagid left outer join subtags s on s.subtagid = d.subtagid order by d.datedebited")
                return curs.fetchall()
        except:
            return []
