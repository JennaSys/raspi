import ClientService
# import DebugPrinting

def GetClients():
    csc=ClientService.ClientServiceCalls()
    # result=csc.GetClientsBySingleId('100012249')
    # result=csc.GetClientsBySingleId('100015575')
    result=csc.GetClientsBySingleId('100014568')
    print result
    # print result.Status
    # print result.Clients.Client[0].FirstName
    # visits=csc.GetClientVisits('100015575')
    # print visits

    # indexes=csc.GetClientIndexes()
    # print indexes

    # cfields=csc.GetCustomClientFields()

    # memberships=csc.GetActiveClientMemberships('100014568')

    # result=csc.GetAllClients()

def AddArrival():
    result=ClientService.ClientServiceCalls().AddArrival('100014568', 1)
    print result.Message
    # Message = "Client does not have an active arrival client service."

def GetMemberships():
    result=ClientService.ClientServiceCalls().GetActiveClientMemberships('100014568')


if __name__ =="__main__":
    GetClients()
    # AddArrival()
    GetMemberships()


