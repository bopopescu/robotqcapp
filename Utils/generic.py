from kioskApp.models import *
import datetime

def getTotalBalance(_customer):
    transactions = Transaction.objects.filter(customer = _customer)
    paid = 0
    registered = 0
    for transaction in transactions:
        paid+=int(transaction.amount_payed)
        registered+=int(transaction.amount_registered)
    res = paid-registered
    return res
def indextotext96(index): #calculate alphanumeric well coordinates by numeric index TODO: consider moving to a more general location.
    col = index/8
    row = index%8
    return chr(row+ord('A'))+str(col+1)

def texttoindex96(text): #calculate numeric well coordinates by alphanumeric index TODO: consider moving to a more general location.
    if len(text) > 1:
        row = ord(text[:1])-ord('A')
        col = int(text[1:]) - 1
        return col*8 + row
    return 0

def getFileName(file):
    res = None
    lastDirIndex = str(file).rfind('/')
    if lastDirIndex == -1:
        res = str(file)
    else:
        res = str(file)[lastDirIndex+1:len(str(file))]
    return res

def getsec_(reagentstring): #Get the index of the second '_' in reagentstring. If non exists, returns last index.
    if reagentstring.find('_',reagentstring.find('_')+1) > 0:
        return reagentstring.find('_',reagentstring.find('_')+1)
    return len(reagentstring)

def reagentname(reagentstring):
    return reagentstring[:getsec_(reagentstring)] #get the reagent name (up to second '_')

def reagentsuffix(reagentstring):
    return reagentstring[getsec_(reagentstring):] #get the reagent name (from second '_' and on)

#def step(proj):
#    wettingtype = StepType.objects.get(description = 'Wet') #Wet code = 14. we use description for readablity but TODO: change to PK.
#    watermix = Mix.objects.get(code=1) #water mix
#    steps = []
#    for y in Y.objects.filter(project=proj):
#        steps.append(Step.objects.get_or_create(y = y,
#            step = 0,#wetting...
#            notes = 'Wet',
#            final_step = False,
#            lastupdate = datetime.datetime.now().date(),
#            lastuser = '',#TODO: hook this up to a real user.
#            step_type = wettingtype,
#            run_result = '', #TODO: FIll this later
#            script_approval_result = '', #TODO: FIll this later
#            compilationnew = '', #TODO: FIll this later
#            compilationold = '', #TODO: FIll this later
#            notebooklink = '', #TODO: Fill this later
#            output = '', #TODO: Fill this later (always null in legacy)
#            mix = watermix
#        )
#        )
#    tstatinprocess = TaskStatus.objects.get(description = 'In Process')#'In Process' code = 1. we use description for readablity but TODO: change to PK.
#    TaskType
#    Task.objects.create()