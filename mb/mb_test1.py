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
    result = ClientService.ClientServiceCalls().AddArrival('100014568', 1)  # works
    # result = ClientService.ClientServiceCalls().AddArrival('100012249', 1)  # fails
    print result
    # print result.Message
    # Message = "Client does not have an active arrival client service."

"""
(AddArrivalResult){
   Status = "Success"
   ErrorCode = 200
   XMLDetail = "Full"
   ResultCount = 0
   CurrentPageIndex = 0
   TotalPageCount = 0
   ArrivalAdded = True
   ClientService =
      (ClientService){
         Current = True
         Count = 1000
         Remaining = 996
         ID = 100244255
         Name = "Corporate Couple Membership"
         PaymentDate = 2015-07-05 00:00:00
         ActiveDate = 2015-07-05 00:00:00
         ExpirationDate = 2015-08-04 00:00:00
         Program =
            (Program){
               ID = 21
               Name = "Gym Membership"
               ScheduleType = "Arrival"
               CancelOffset = 0
            }
      }
 }
 """

"""
(AddArrivalResult){
   Status = "Success"
   ErrorCode = 200
   Message = "Client does not have an active arrival client service."
   XMLDetail = "Full"
   ResultCount = 0
   CurrentPageIndex = 0
   TotalPageCount = 0
   ArrivalAdded = False
 }
 """


def GetMemberships():
    result = ClientService.ClientServiceCalls().GetActiveClientMemberships('100014568')


if __name__ == "__main__":
    # GetClients()
    AddArrival()
    # GetMemberships()


