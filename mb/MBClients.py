import ClientService
import BasicRequestHelper

from collections import namedtuple

class MBClients:
    def __init__(self, site_id):
        self.site_id = site_id

    def get_client(self, client_id):
        client =  ClientService.ClientServiceCalls(self.site_id).GetClientsBySingleId(client_id)
        if len(client.Clients.Client) > 0:
            return client.Clients.Client[0]
        else:
            return None

    def add_client(self, client):
        client['Action'] = "None"
        loc = BasicRequestHelper.FillAbstractObject(ClientService.ClientServiceMethods.service, "Location", {"ID": 1, "Action": "None"})
        client['HomeLocation'] = loc
        clients = BasicRequestHelper.FillArrayType(ClientService.ClientServiceMethods.service, [client], "Client", "Client")
        result = ClientService.ClientServiceCalls(self.site_id).AddOrUpdateClients('AddNew', False, clients)
        return result

    def get_client_fields(self):
        fields = [
                  # "NewID",
                  # "AccountBalance",
                  "ClientIndexes",  #map list
                  "Username",
                  "Password",
                  "Notes",  #add prior class list
                  "MobileProvider",
                  "ClientCreditCard",
                  # "LastFormulaNotes",
                  "AppointmentGenderPreference",
                  "Gender",
                  "IsCompany",
                  "Inactive",
                  # "ClientRelationships", #add in 2nd pass
                  # "Reps",
                  # "SaleReps",
                  "CustomClientFields",
                  "LiabilityRelease", #uncheck if < 1/1/16 or so?
                  "EmergencyContactInfoName",
                  "EmergencyContactInfoRelationship",
                  "EmergencyContactInfoPhone",
                  "EmergencyContactInfoEmail",
                  "PromotionalEmailOptIn",
                  "CreationDate",
                  "Liability", #save releases > 1/1/16 or so?
                  # "ProspectStage",
                  # "UniqueID",
                  "Action",
                  # "ID",
                  "FirstName",
                  "MiddleName",
                  "LastName",
                  "Email",
                  "EmailOptIn",
                  "AddressLine1",
                  "AddressLine2",
                  "City",
                  "State",
                  "PostalCode",
                  "Country",
                  "MobilePhone",
                  "HomePhone",
                  "WorkPhone",
                  "WorkExtension",
                  "BirthDate",
                  "FirstAppointmentDate",
                  "ReferredBy",
                  "HomeLocation",
                  "YellowAlert",
                  "RedAlert",
                  "PhotoURL",
                  "IsProspect",
                  "Status",
                  "ContactMethod"]

        return fields


    def get_classes(self, client_id):
        visits_raw = ClientService.ClientServiceCalls(self.site_id).GetClientVisits(client_id,  '2010-01-01')

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

    def get_class_history(self, client_id):
        classes = self.get_classes(client_id)
        class_list = ''
        for c in sorted(classes):
            # print "{0} ({1:%Y-%m-%d}) [{2}]".format(c, classes[c][0], classes[c][1])
            class_list += "{0} ({1:%Y-%m-%d})\n".format(c, classes[c][0])
        if len(class_list) == 0:
            class_list = 'None'
        return 'CLASS HISTORY\n--------------------------\n' + class_list + '\n\n'


    def get_contact_logs(self, client_id):
        logs_raw = ClientService.ClientServiceCalls(self.site_id).GetClientContactLogs(clientId=client_id, startDate='2010-01-01', endDate='2020-01-01')

        logs = {}
        Log = namedtuple('Log','ContactMethod ContactName Text CreatedDateTime CreatedBy FollowupByDate AssignedTo')
        for log in logs_raw.ContactLogs[0]:
            if log.CreatedBy.Name not in ["System Generated"]:
                # class_instance = ClassService.ClassServiceCalls().GetClassVisits(v.ClassID)
                if 'AssignedTo' in log:
                    assigned_to = log.AssignedTo.FirstName + " " + log.AssignedTo.LastName
                else:
                    assigned_to = None
                logs[log.CreatedDateTime] = Log(log.ContactMethod, log.ContactName, log.Text, log.CreatedDateTime, log.CreatedBy.FirstName + " " + log.CreatedBy.LastName, log.FollowupByDate, assigned_to)

        return logs

    def add_contact_logs(self, client_id, logs):
        log_type = BasicRequestHelper.FillAbstractObject(ClientService.ClientServiceMethods.service, "ContactLogType", {"ID": self.get_contactlog_mbtransfer_typeid()})
        log_types = BasicRequestHelper.FillArrayType(ClientService.ClientServiceMethods.service, log_type, "ContactLogType", "ContactLogType")
        client = {}
        client['ID'] = client_id
        new_logs = []
        for log in sorted(logs):
            new_log = {}
            new_log['Client'] = client
            new_log['ContactMethod'] = logs[log].ContactMethod
            new_log['ContactName'] = logs[log].ContactName
            header = "Created: {0:%Y-%m-%d} by {1}<br>".format(logs[log].CreatedDateTime, logs[log].CreatedBy)
            if logs[log].FollowupByDate is not None:
                header += "Follow Up: {0:%Y-%m-%d}".format(logs[log].FollowupByDate)
                if logs[log].AssignedTo is not None:
                    header += " for {}".format(logs[log].AssignedTo)
                header += "<br>"
            new_log['Text'] = header + logs[log].Text
            new_log['CreatedDateTime'] = logs[log].CreatedDateTime
            new_log['IsSystemGenerated'] = False
            new_log['Types'] = log_types
            new_logs.append(new_log)
        log_array = BasicRequestHelper.FillArrayType(ClientService.ClientServiceMethods.service, new_logs, "ContactLog", "ContactLog")

        result = ClientService.ClientServiceCalls(self.site_id).AddContactLogs(client_id, log_array)
        return result


    def get_contactlog_mbtransfer_typeid(self):
        log_types = ClientService.ClientServiceCalls(self.site_id).GetContactLogTypes()
        # TESTING
        return [t for t in log_types.ContatctLogTypes[0] if 'Fitness Assessment' in t[1]][0]['ID']
        # return [t for t in log_types.ContatctLogTypes[0] if 'MB TRANSFER' in t[1]][0]['ID']


    def get_custom_field_id(self, field_name):
        fields = ClientService.ClientServiceCalls(self.site_id).GetCustomClientFields()
        return [f for f in fields.CustomClientFields[0] if field_name in f['Name']][0]['ID']

    def get_client_custom_fields(self, client_id):
        client =  ClientService.ClientServiceCalls(self.site_id).GetClientsBySingleId(client_id, ['Clients.CustomClientFields'])
        if len(client.Clients.Client[0].CustomClientFields) > 0:
            return client.Clients.Client[0].CustomClientFields[0]
        else:
            return None

    def add_custom_fields(self, client_id, custom_fields):
        if custom_fields is not None:
            new_field_list = []
            for field_name in ['Employer', 'Occupation', 'Referral']:
                # for field_name in ['Company', 'Position']:
                # print self.get_custom_field_id(field_name)
                if field_name in [field['Name'] for field in custom_fields]:
                    # print "{0}={1}".format(field_name, [f for f in custom_fields if field_name in f['Name']][0]['Value'])
                    field_id = self.get_custom_field_id(field_name)
                    custom_field = {'ID':field_id, 'Value':[f for f in custom_fields if field_name in f['Name']][0]['Value']}
                    new_field_list.append(custom_field)

            if len(new_field_list) > 0:
                new_fields = BasicRequestHelper.FillArrayType(ClientService.ClientServiceMethods.service, new_field_list, "CustomClientField", "CustomClientField")
                client = {}
                client['ID'] = client_id
                client['Action'] = "None"
                client['CustomClientFields'] = new_fields
                clients = BasicRequestHelper.FillArrayType(ClientService.ClientServiceMethods.service, [client], "Client", "Client")
                result = ClientService.ClientServiceCalls(self.site_id).AddOrUpdateClients('Update', False, clients)
                return result
            else:
                return None


