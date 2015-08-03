import ClientService
import logging
# import DebugPrinting

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('MindBody')
log.setLevel(logging.DEBUG)


class MindBody:
    def GetClients(self, memberId):
        csc = ClientService.ClientServiceCalls()
        # result=csc.GetClientsBySingleId('100012249')
        # result=csc.GetClientsBySingleId('100015575')
        # result = csc.GetClientsBySingleId('100014568')
        result = csc.GetClientsBySingleId(memberId)
        return result
        # print result.Status
        # print result.Clients.Client[0].FirstName
        # visits=csc.GetClientVisits('100015575')
        # print visits

        # indexes=csc.GetClientIndexes()
        # print indexes

        # cfields=csc.GetCustomClientFields()

        # memberships=csc.GetActiveClientMemberships('100014568')

        # result=csc.GetAllClients()

    def AddArrival(self, memberId, locationId=1, test=False):
        result = ClientService.ClientServiceCalls().AddArrival(memberId, locationId)
        if result.ArrivalAdded == True:
            log.info('Client {}: Check-in Location {}'.format(memberId, locationId))
        else:
            log.info('Client {}: Check-in FAILED Location {} [{}]'.format(memberId, locationId, result.Message))

        return result
        # print result.Message
        # Message = "Client does not have an active arrival client service."

    def GetMemberships(self, memberId):
        result = ClientService.ClientServiceCalls().GetActiveClientMemberships(memberId)
        return result

if __name__ == "__main__":
    mb = MindBody()
    # client = mb.GetClients('100014568')
    # print client
    # ci = mb.AddArrival('100014568')
    # print ci
    # ci = mb.AddArrival('100015512')
    # ci = mb.AddArrival('100011642')
    # ci = mb.AddArrival('2811862964')
    # print ci
    # ci = mb.AddArrival('100012249')
    # print ci
    # cm = mb.GetMemberships('100014568')
    # print cm
    print ClientService.ClientServiceCalls().GetSoapMethods()
