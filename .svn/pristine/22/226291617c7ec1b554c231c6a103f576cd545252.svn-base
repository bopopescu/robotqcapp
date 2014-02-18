# -*- coding: utf-8 -*-
import xlwt
from cStringIO import StringIO
from kioskApp.models import *
from datable.web.table import Table
def serializeCustomers(customers):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Total Balance for all customers')
    curRow = 0
    curCol = 0
    sheet.write(curRow, curCol,'total debt for all customers')
    curRow+=1
    totalDebt=0
    for customer in customers:
        totalDebt += customer.totalBalance
    sheet.write(curRow, curCol,str(totalDebt))
    for customer in customers:
        sheet = book.add_sheet(customer.firstName+'_'+customer.lastName)
        transactions = Transaction.objects.filter(customer=customer)
        header = ['שעה','תאריך', 'זכות','חובה','סכום','תיאור']
        totalDebt =customer.totalBalance
        curRow = 0
        curCol = 0
        sheet.write(curRow, curCol,customer.firstName+' '+customer.lastName)
        curRow+=1
        sheet.write(curRow, curCol, 'total debt')
        curRow+=1
        sheet.write(curRow, curCol,str(totalDebt))
        curRow+=1
        for field in header:
            sheet.write(curRow, curCol, field)
            curCol+=1
        curRow+=1
        for t in transactions:
            curCol = 0
            sheet.write(curRow, curCol, str(t.time))
            curCol+=1
            sheet.write(curRow, curCol, str(t.date))
            curCol+=1
            sheet.write(curRow, curCol, str(t.amount_payed))
            curCol+=1
            sheet.write(curRow, curCol, str(t.amount_registered))
            curCol+=1
            sheet.write(curRow, curCol, str(t.amount_obligo))
            #if t.transactionDescription:
             #   curCol+=1
             #   sheet.write(curRow, curCol, str(t.transactionDescription.decode("cp1255").encode("utf-8")))
            curRow+=1

    output = StringIO()
    book.save(output)
    output.seek(0)
    return output