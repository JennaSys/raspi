import ClientService
import BasicRequestHelper


class MBClients:
    def get_client(self, client_id):
        client =  ClientService.ClientServiceCalls().GetClientsBySingleId(client_id)
        if len(client.Clients.Client) > 0:
            return client.Clients.Client[0]
        else:
            return None

    def add_client(self, client):
        client['Action'] = "None"
        loc = BasicRequestHelper.FillAbstractObject(ClientService.ClientServiceMethods.service, "Location", {"ID": 1, "Action": "None"})
        client['HomeLocation'] = loc
        clients = BasicRequestHelper.FillArrayType(ClientService.ClientServiceMethods.service, [client], "Client", "Client")
        result = ClientService.ClientServiceCalls().AddOrUpdateClients('AddNew', False, clients)
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
