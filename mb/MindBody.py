
import ClientService
import SiteService
import SaleService
import ClassService
import BasicRequestHelper

from collections import namedtuple

import logging
# import DebugPrinting

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('MindBody')
log.setLevel(logging.DEBUG)
# logging.getLogger('suds.transport').setLevel(logging.DEBUG)


class MindBody:
    def get_clients(self, memberId, site_id):
        csc = ClientService.ClientServiceCalls(site_id)
        # result=csc.GetClientsBySingleId('100012249')
        # result=csc.GetClientsBySingleId('100015575')
        # result = csc.GetClientsBySingleId('100014568')
        result = csc.GetClientsBySingleId(memberId)
        # result = csc.GetClientsByMultipleIds([memberId], ['Clients.FirstName','Clients.LastName'])
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

    def add_arrival(self, memberId, locationId=1, test=False):
        result = ClientService.ClientServiceCalls().AddArrival(memberId, locationId)
        if result.ArrivalAdded == True:
            log.info('Client {}: Check-in Location {}'.format(memberId, locationId))
        else:
            log.info('Client {}: Check-in FAILED Location {} [{}]'.format(memberId, locationId, result.Message))

        return result
        # print result.Message
        # Message = "Client does not have an active arrival client service."

    def get_memberships(self, memberId):
        result = ClientService.ClientServiceCalls().GetActiveClientMemberships(memberId)
        return result

    def make_clients(self, ln, fn, em, g, bd):
        # client = BasicRequestHelper.FillAbstractObject(ClientService.ClientServiceMethods.service, "Client", {"LastName":ln, "FirstName":fn, "Email":em})

        # client = ClientService.ClientServiceMethods.service.factory.create("Client")
        # client.LastName=ln
        # client.FirstName=fn
        # client.Email=em
        # client.Action="None"
        # client.Gender="Male"
        # client.BirthDate="1970-01-01"

        client = {}
        client['LastName']=ln
        client['FirstName']=fn
        client['Email']=em
        client['Action']="None"
        client['Gender']=g
        client['BirthDate']=bd
        loc = BasicRequestHelper.FillAbstractObject(ClientService.ClientServiceMethods.service, "Location", {"ID":1, "Action":"None"})
        client['HomeLocation']=loc

        # Client = type('Client', (object,), {'LastName': None, 'FirstName': None, 'Email': None, 'Gender' : None, 'BirthDate' : None})
        # client = Client()
        # client.LastName=ln
        # client.FirstName=fn
        # client.Email=em
        # client.Gender=g
        # client.BirthDate=bd

        clients = BasicRequestHelper.FillArrayType(ClientService.ClientServiceMethods.service, [client], "Client", "Client")
        return clients

    def get_programs(self):
        ssc = SiteService.SiteServiceCalls()
        progs_raw = ssc.GetPrograms()
        progs = {}
        for p in progs_raw.Programs[0]:
            progs[p.ID] = p.Name
        return progs

    def get_class_list(self):
        # ssc = SiteService.SiteServiceCalls()
        # progs_raw = ssc.GetPrograms()
        # progs = {}
        # for p in progs_raw.Programs[0]:
        #     progs[p.ID] = p.Name

        csc = ClassService.ClassServiceCalls()
        classes_raw = csc.GetClassDescriptions(startClassDateTime='2010-01-01', endClassDateTime='2020-01-01', fields=['ID', 'Name', 'Program'])
        classes = {}
        for c in classes_raw.ClassDescriptions[0]:
            # classes[c.ID] = (c.Name, progs[c.Program.ID])
            classes[c.ID] = c.Name

        return classes

    def get_classes(self, mID, site_id):

        # classes = self.get_class_list()

        csc = ClientService.ClientServiceCalls(site_id)
        visits_raw = csc.GetClientVisits(mID, '2010-01-01')

        visits = {}
        if visits_raw.ResultCount > 0:
            for v in visits_raw.Visits[0]:
                if v.SignedIn and v.ClassID != 0 and v.Name not in ["Member's Social"]:
                    # class_instance = ClassService.ClassServiceCalls().GetClassVisits(v.ClassID)
                    visits[v.Name] = (v.StartDateTime, self.get_class_code_from_name(v.Name))

        return visits

    def get_class_code_from_name(self, name):
        if name[:9].find(" - ") > 0:
            return name[:name.find(" - ")]
        elif name[:9].find(u' \u2013 ') > 0:
            return name[:name.find(u' \u2013 ')]
        # elif name[:9].find(' ') > 0:
        #     return name[:name.find(' ')]
        else:
            return ''

    def get_contact_logs(self, mID, site_id):
        csc = ClientService.ClientServiceCalls(site_id)
        logs_raw = csc.GetClientContactLogs(clientId=mID, startDate='2010-01-01', endDate='2020-01-01')

        logs = {}
        Log = namedtuple('Log','ContactMethod ContactName Text')
        for log in logs_raw.ContactLogs[0]:
            if log.CreatedBy.Name not in ["System Generated"]:
                # class_instance = ClassService.ClassServiceCalls().GetClassVisits(v.ClassID)
                logs[log.CreatedDateTime] = Log(log.ContactMethod, log.ContactName, log.Text)

        return logs


if __name__ == "__main__":
    mb = MindBody()
    # client = mb.get_clients('100014568')
    # print client
    # ci = mb.add_arrival('100014568')
    # print ci
    # ci = mb.add_arrival('100015512')
    # ci = mb.add_arrival('100011642')
    # ci = mb.add_arrival('2811862964')
    # print ci
    # ci = mb.add_arrival('100012249')
    # print ci
    # cm = mb.get_memberships('100014568')
    # print cm
    # print ClientService.ClientServiceCalls().GetSoapMethods()
    # SiteService.SiteServiceCalls().GetActivationCode()
    # client = ClientService.ClientServiceCalls().GetClientsByMultipleIds(['100013027'])
    # client = ClientService.ClientServiceCalls().GetClientsByMultipleIds(['100015431'])
    # client = ClientService.ClientServiceCalls().GetClientsByMultipleIds(['100015655'], ['Clients.FirstName','Clients.LastName'])
    # client = ClientService.ClientServiceCalls().GetClientsByMultipleIds(['100015431'], ['Clients.CustomClientFields','Clients.ClientCreditCard','Clients.ClientIndexes','Clients.EmergencyContactInfoName','Clients.RedAlert'])
    # client = ClientService.ClientServiceCalls().GetClientsByString('Shee')
    # client = ClientService.ClientServiceCalls().GetClientIndexes()
    # client = ClientService.ClientServiceCalls().GetAllClients(2, 10)
    # client = mb.get_clients('004',41095)
    # client = mb.get_clients('100011834',)
    # client = mb.get_clients('1545',)
    # client = mb.get_clients('100015655')
    # client = ClientService.ClientServiceCalls().AddFormulaNoteToClient('004', 'This is a test Formula Note added via the API')
    # print client
    # print sales
    # c = mb.make_clients("Brown", "Chuckie", "cbrown@peanuts.com","Male", "1970-01-01")
    # print c
    # r = ClientService.ClientServiceCalls().AddOrUpdateClients('AddNew', False, c)
    # print r
    # SiteService.SiteServiceCalls().GetLocations()

    # classes = mb.get_class_list()
    # print len(classes)
    # # for c in sorted(classes.itervalues()):
    # for id, c in sorted(classes.iteritems(), key=lambda x: x[1]):
    #     print u"{0}|{1}|{2}".format(id,c, mb.get_class_code_from_name(c))

    # classes = ClientService.ClientServiceCalls().GetClientVisits('004','2010-01-01')
    # classes = mb.get_classes('356', 41095)
    # for c in sorted(classes):
    #     print "{0} ({1:%Y-%m-%d}) [{2}]".format(c, classes[c][0], classes[c][1])

    # logs = mb.get_contact_logs('004', 41095)
    # for log in sorted(logs):
    #     print "{0:%Y-%m-%d} {1}".format(log, logs[log])

    # ClientService.ClientServiceCalls().GetClientServices(clientId='356', programIds=mb.get_programs().keys())

    # programs = mb.get_programs()
    # for p in programs:
    #     print p, programs[p]

    # referrals=ClientService.ClientServiceCalls().GetClientReferralTypes()
    # for r in referrals.ReferralTypes[0]:
    #     print r

    # print SiteService.SiteServiceCalls().GetMobileProviders()
    # log_types = ClientService.ClientServiceCalls(293010).GetContactLogTypes()
    log_types = ClientService.ClientServiceCalls(-99).GetContactLogTypes()
    print log_types