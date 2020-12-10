from sql_query.mysql_dbconfig import read_db_config
from sql_query.list_to_string import list_to_string
from sql_query.iter_row import iter_row

def sql_express_refund(date_refund, cursor):
        need_refund_all = []
        refund_follow_on_accepted = []

        cursor.execute(f"SELECT DISTINCT o.code\
                            FROM orders AS o\
                                JOIN enumerationvalueslp AS elp\
                                    ON elp.ITEMPK=o.statuspk\
                                JOIN orderentries AS oe\
                                    ON oe.p_order=o.PK\
                                JOIN deliverymodes AS d\
                                    ON o.deliverymodepk=d.PK\
                                JOIN paymentmodes AS p\
                                    ON p.pk=o.paymentmodepk\
                                JOIN orderhistoryentries AS oh\
                                    ON oh.p_order=o.pk\
                                JOIN paymenttransactions AS pt\
                                    ON pt.p_order=o.PK\
                                JOIN paymnttrnsctentries AS pte\
                                    ON pte.p_paymenttransaction=pt.PK\
                            WHERE elp.LANGPK=8796093349920\
                                AND o.createdTS > (CURDATE() - INTERVAL 20 DAY)\
                                AND o.modifiedTS < CURDATE() - INTERVAL 40 MINUTE\
                                AND p.code='card'\
                                AND d.code='express_courier'\
                                AND oh.p_description like '%новый статус=Частичный возврат%'\
                                AND date(oh.createdts) = '{date_refund}'\
                                AND pte.p_transactionstatus='CREATE_SUBSCRIPTION_ACCEPTED'")

        for row in iter_row(cursor, 10):
            need_refund_all.extend(list(row))


        orders = list_to_string(need_refund_all)

        if orders != '':
            cursor.execute(f"SELECT DISTINCT o.code\
                            FROM orders AS o\
                                JOIN enumerationvalueslp AS elp\
                                    ON elp.ITEMPK=o.statuspk\
                                JOIN orderentries AS oe\
                                    ON oe.p_order=o.PK\
                                JOIN deliverymodes AS d\
                                    ON o.deliverymodepk=d.PK\
                                JOIN paymentmodes AS p\
                                    ON p.pk=o.paymentmodepk\
                                JOIN orderhistoryentries AS oh\
                                    ON oh.p_order=o.pk\
                                JOIN paymenttransactions AS pt\
                                    ON pt.p_order=o.PK\
                                JOIN paymnttrnsctentries AS pte\
                                    ON pte.p_paymenttransaction=pt.PK\
                            WHERE elp.LANGPK=8796093349920\
                                AND o.createdTS >(CURDATE() - INTERVAL 20 DAY)\
                                AND o.modifiedTS < CURDATE() - INTERVAL 40 MINUTE\
                                AND p.code='card'\
                                AND pte.p_transactionstatus='REFUND_FOLLOW_ON_ACCEPTED'\
                                AND o.code IN ({orders})")


        for row in iter_row(cursor, 10):
            refund_follow_on_accepted.extend(list(row))

        need_refund = need_refund_all

        for order in refund_follow_on_accepted:
            need_refund.remove(order)

        return need_refund

if __name__ == '__main__':
    sql_courier_refund()