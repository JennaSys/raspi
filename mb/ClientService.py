from suds.client import Client
import BasicRequestHelper
from datetime import datetime


class ClientServiceCalls:

    """This class contains examples of consumer methods for each ClassService method."""

    def GetSoapMethods(self):
        url = BasicRequestHelper.BuildWsdlUrl('Client')
        return Client(url)

    """AddArrival Methods"""

    def AddArrival(self, clientId, locationId):
        result = ClientServiceMethods().AddArrival(clientId, locationId)
        # print str(result.Message)
        return result

    """AddClientFormulaNote Methods"""

    def AddFormulaNoteToClientWithAppointment(self, clientId, appointmentId, note):
        result = ClientServiceMethods().AddClientFormulaNote(clientId, appointmentId, note)
        print str(result)

    def AddFormulaNoteToClient(self, clientId, note):
        self.AddFormulaNoteToClientWithAppointment(clientId, None, note)

    """AddOrUpdateClient Methods"""

    def AddOrUpdateClients(self, updateAction="Fail", test=False, clients=None):
        result = ClientServiceMethods().AddOrUpdateClients(updateAction, test, clients)
        print str(result)

    def AddCreditCardToClient(self, clientId, cc):
        """A consumer method for adding a credit card to a client's information.
           Note that adding a credit card in particular requires a secure connection 
           (https url) when setting up your service."""
        result = ClientServiceMethods().AddCreditCardToClient(clientId, cc)
        print str(result)

    def AddNewCreditCardToClient(self, clientId,
                                 cardType,
                                 lastFour,
                                 cardNumber,
                                 holderName,
                                 expMonth,
                                 expYear,
                                 address,
                                 city,
                                 state,
                                 postalCode):
        """A consumer method for adding a new or default credit card
           to a client's information. Note that adding a credit card 
           in particular requires a secure connection (https url) when 
           setting up your service."""
        result = ClientServiceMethods().CreateAndAddCreditCardToClient(clientId,
                                                                       cardType,
                                                                       lastFour,
                                                                       cardNumber,
                                                                       holderName,
                                                                       expMonth,
                                                                       expYear,
                                                                       address,
                                                                       city,
                                                                       state,
                                                                       postalCode)
        print str(result)

    """AddOrUpdateContactLogs Methods"""

    def UpdateContactLogText(self, clientId, text):
        result = ClientServiceMethods().UpdateContactLogText(clientId, text)
        print str(result)

    """DeleteClientFormulaNote Methods"""

    def DeleteFormulaNote(self, clientId, formulaNoteId):
        result = ClientServiceMethods().DeleteFormulaNote(clientId, formulaNoteId)
        print str(result)

    """GetActiveClientMemberships Methods"""

    def GetActiveClientMemberships(self, clientId, locationId=None):
        result = ClientServiceMethods().GetActiveClientMemberships(clientId, locationId)
        print str(result)

    """GetClientAccountBalances Methods"""

    def GetRelativeClientAccountBalances(self, clientIds, balanceDate=None, classId=None):
        result = ClientServiceMethods().GetClientAccountBalances(clientIds, balanceDate, classId)
        print str(result)

    def GetCurrentClientAccountBalances(self, clientIds, classId=None):
        self.GetRelativeClientAccountBalances(clientIds, classId=classId)

    """GetClientContactLogs Methods"""

    def GetClientContactLogs(self, clientId,
                             startDate=datetime.today(),
                             endDate=datetime.today(),
                             staffIds=None,
                             systemGenerated=False,
                             typeIds=None,
                             subtypeIds=None):
        result = ClientServiceMethods().GetClientContactLogs(clientId,
                                                             startDate,
                                                             endDate,
                                                             staffIds,
                                                             systemGenerated,
                                                             typeIds,
                                                             subtypeIds)
        print str(result)

    """GetClientContracts Methods"""

    def GetClientContracts(self, clientId=None):
        result = ClientServiceMethods().GetClientContracts(clientId)
        print str(result)

    """GetClientFormulaNotes Methods"""

    def GetClientFormulaNotes(self, clientId, appointmentId=None):
        result = ClientServiceMethods().GetClientFormulaNotes(clientId, appointmentId)
        print str(result)

    """GetClientIndexes Methods"""

    def GetClientIndexes(self):
        result = ClientServiceMethods().GetClientIndexes()
        # print str(result)
        return result

    """GetClientPurchases Methods"""

    def GetClientPurchases(self, clientId, startDate=datetime.today(), endDate=datetime.today()):
        result = ClientServiceMethods().GetClientPurchases(clientId, startDate, endDate)
        print str(result)

    """GetClientReferralTypes Methods"""

    def GetClientReferralTypes(self):
        result = ClientServiceMethods().GetClientReferralTypes()
        print str(result)

    """GetClients Methods"""

    def GetClientsBySingleId(self, id):
        result = ClientServiceMethods().GetClientsBySingleId(id)
        # print str(result)
        return result

    def GetClientsByMultipleIds(self, ids):
        result = ClientServiceMethods().GetClientsByMultipleIds(ids)
        print str(result)

    def GetAllClients(self):
        result = ClientServiceMethods().GetAllClients()
        print str(result)

    def GetClientsByString(self, searchStr):
        result = ClientServiceMethods().GetClientsByString(searchStr)
        print str(result)

    """GetClientSchedule Methods"""

    def GetClientSchedule(self, clientId, startDate=datetime.today(), endDate=datetime.today()):
        result = ClientServiceMethods().GetClientSchedule(clientId, startDate, endDate)
        print str(result)

    """GetClientServices Methods"""

    def GetClientServices(self, clientId,
                          classId=0,
                          programIds=None,
                          sessionTypeIds=None,
                          locationIds=None,
                          visitCount=0,
                          startDate=None,
                          endDate=None,
                          showActiveOnly=False):
        result = ClientServiceMethods().GetClientServices(clientId,
                                                          classId,
                                                          programIds,
                                                          sessionTypeIds,
                                                          locationIds,
                                                          visitCount,
                                                          startDate,
                                                          endDate,
                                                          showActiveOnly)
        print str(result)

    def GetClientServicesForPastYear(self, clientId,
                                     classId=0,
                                     programIds=None,
                                     sessionTypeIds=None,
                                     locationIds=None,
                                     visitCount=0,
                                     showActiveOnly=False):
        self.GetClientServices(clientId,
                               classId,
                               programIds,
                               sessionTypeIds,
                               locationIds,
                               visitCount,
                               BasicRequestHelper.oneYearAgo,
                               datetime.today(),
                               showActiveOnly)

    """GetClientVisits Methods"""

    def GetClientVisits(self, clientId,
                        startDate=datetime.today(),
                        endDate=datetime.today(),
                        unpaidsOnly=False):
        result = ClientServiceMethods().GetClientVisits(clientId,
                                                        startDate,
                                                        endDate,
                                                        unpaidsOnly)
        print str(result)

    """GetContactLogTypes Methods"""

    def GetContactLogTypes(self):
        result = ClientServiceMethods().GetContactLogTypes()
        print str(result)

    """GetCustomClientFields Methods"""

    def GetCustomClientFields(self):
        """A consumer method for retrieving all custom client fields. This contains
           an example of parsing a result to print fields out in an easier-to-read
           format than the returned XML."""
        result = ClientServiceMethods().GetCustomClientFields()

        print "ID - Name"
        print "------------------------------"
        for field in result.CustomClientFields.CustomClientField:
            print "%2d - %s" % (field.ID, field.Name)

    """GetRequiredClientFields Methods"""

    def GetRequiredClientFields(self):
        result = ClientServiceMethods().GetRequiredClientFields()
        print str(result)

    """SendUserNewPassword methods"""

    def SendUserNewPassword(self, userEmail, userFirstName, userLastName):
        result = ClientServiceMethods().SendUserNewPassword(userEmail, userFirstName, userLastName)
        if hasattr(result, "Message"):
            print result.Message
        else:
            print "No error message returned. Success!"

    """UpdateClientServices Methods"""

    def UpdateClientServices(self, clientServices, test=False):
        result = ClientServiceMethods().UpdateClientServices(clientServices, test)
        print str(result)

    """UploadClientDocument Methods"""

    def UploadClientDocument(self, clientId, fileName, fileSize):
        result = ClientServiceMethods().UploadClientDocument(clientId, fileName, fileSize)
        print str(result)

    """ValidateLogin Methods"""

    def ValidateLogin(self, username, password):
        result = ClientServiceMethods().ValidateLogin(username, password)
        print str(result)


class ClientServiceMethods:

    """This class contains producer methods for all ClientService methods."""
    wsdl = BasicRequestHelper.BuildWsdlUrl("Client")
    """We manually set the SoapAction field here by specifying location. Specifically,
       we need an https connection (for things such as modifying billing information
       and by default, this gets set to http."""
    service = Client(wsdl, location="https://api.mindbodyonline.com/0_5/ClientService.asmx")

    def CreateBasicRequest(self, requestName):
        return BasicRequestHelper.CreateBasicRequest(self.service, requestName)

    """AddArrival methods"""

    def AddArrival(self, clientId, locationId):
        request = self.CreateBasicRequest("AddArrivalRequest")

        request.ClientID = clientId
        request.LocationID = locationId

        return self.service.service.AddArrival(request)

    """AddClientFormulaNote methods"""

    def AddClientFormulaNote(self, clientId, appointmentId, note):
        request = self.CreateBasicRequest("AddClientFormulaNote")

        request.ClientID = clientId
        request.AppointmentID = appointmentId
        request.Note = note

        return self.service.service.AddClientFormulaNote(request)

    """AddOrUpdateClient methods"""

    def AddOrUpdateClients(self, updateAction, test, clients):
        request = self.CreateBasicRequest("AddOrUpdateClients")

        request.UpdateAction = updateAction
        request.Test = test
        request.Clients = clients

        return self.service.service.AddOrUpdateClients(request)

    def AddCreditCardToClient(self, clientId, cc):

        # Call GetClientBySingleID, then grab the first client off the list.
        clientToEdit = self.GetClientsBySingleId(clientId).Clients.Client[0]
        clientToEdit.ClientCreditCard = cc
        Clients = BasicRequestHelper.FillArrayType(self.service, [clientToEdit], "Client", "Client")

        return self.AddOrUpdateClients("Fail", False, Clients)

    def CreateAndAddCreditCardToClient(self, clientId,
                                       cardType,
                                       lastFour,
                                       number,
                                       holderName,
                                       expMonth,
                                       expYear,
                                       address,
                                       city,
                                       state,
                                       postalCode):
        """This method shows how to create a credit card item from given simple types."""
        cc = self.service.factory.create("ClientCreditCard")
        cc.CardType = cardType
        cc.LastFour = lastFour
        cc.CardNumber = number
        cc.CardHolder = holderName
        cc.ExpMonth = expMonth
        cc.ExpYear = expYear
        cc.Address = address
        cc.City = city
        cc.State = state
        cc.PostalCode = postalCode

        return self.AddCreditCardToClient(clientId, cc)

    """AddOrUpdateContactLogs methods"""

    def UpdateContactLogText(self, clientId, text):
        """This method will change the text of every contact log 
           applied to clientId in the past year to text."""
        request = self.CreateBasicRequest("AddOrUpdateContactLogs")

        contactLogs = self.GetClientContactLogsByClient(clientId, True)
        for log in contactLogs.ContactLogs.ContactLog:
            log.Text = text

        request.UpdateAction = "Fail"
        request.Test = False
        request.ContactLogs = contactLogs

        return self.service.service.AddOrUpdateContactLogs(request)

    """DeleteClientFormulaNote methods"""

    def DeleteFormulaNote(self, clientId, formulaNoteId):
        request = self.CreateBasicRequest("DeleteClientFormulaNote")

        request.ClientID = clientId
        request.FormulaNoteID = formulaNoteId

        return self.service.service.DeleteClientFormulaNote(request)

    """GetActiveClientMemberships Methods"""

    def GetActiveClientMemberships(self, clientId, locationId):
        request = self.CreateBasicRequest("GetActiveClientMemberships")

        request.ClientID = clientId
        request.LocationID = locationId

        return self.service.service.GetActiveClientMemberships(request)

    """GetClientAccountBalances methods"""

    def GetClientAccountBalances(self, clientIds, balanceDate, classId):
        request = self.CreateBasicRequest("GetClientAccountBalances")

        ClientIDs = self.service.factory.create("ArrayOfString")
        ClientIDs.string = clientIds

        request.ClientIDs = ClientIDs
        request.BalanceDate = balanceDate
        request.ClassID = classId

        return self.service.service.GetClientAccountBalances(request)

    """GetClientContactLogs methods"""

    def GetClientContactLogs(self, clientId,
                             startDate,
                             endDate,
                             staffIds,
                             systemGenerated,
                             typeIds,
                             subtypeIds):
        request = self.CreateBasicRequest("GetClientContactLogsRequest")

        request.ClientID = clientId
        request.StartDate = startDate
        request.EndDate = endDate
        request.StaffIDs = BasicRequestHelper.FillArrayType(self.service, staffIds, "Long")
        request.ShowSystemGenerated = systemGenerated
        request.TypeIDs = typeIds
        request.SubtypeIDs = subtypeIds

        return self.service.service.GetClientContactLogs(request)

    def GetClientContactLogsByClient(self, clientId, systemGenerated):
        """Convenience method to find all contact logs for a given client within the past year."""
        return self.GetClientContactLogs(clientId,
                                         BasicRequestHelper.oneYearAgo,
                                         datetime.today(),
                                         None,
                                         systemGenerated,
                                         None,
                                         None)

    """GetClientContracts methods"""

    def GetClientContracts(self, clientId):
        request = self.CreateBasicRequest("GetClientContracts")

        request.ClientID = clientId

        return self.service.service.GetClientContracts(request)

    """GetClientFormulaNotes methods"""

    def GetClientFormulaNotes(self, clientId, appointmentId):
        request = self.CreateBasicRequest("GetClientFormulaNotes")

        request.ClientID = clientId
        request.AppointmentID = appointmentId

        return self.service.service.GetClientFormulaNotes(request)

    """GetClientIndexes methods"""

    def GetClientIndexes(self):
        request = self.CreateBasicRequest("GetClientIndexesRequest")

        return self.service.service.GetClientIndexes(request)

    """GetClientPurchases methods"""

    def GetClientPurchases(self, clientId, startDate, endDate):
        request = self.CreateBasicRequest("GetClientPurchases")

        request.ClientID = clientId
        request.StartDate = startDate
        request.EndDate = endDate

        return self.service.service.GetClientPurchases(request)

    """GetClientReferralTypes methods"""

    def GetClientReferralTypes(self):
        request = self.CreateBasicRequest("GetClientReferralTypes")

        return self.service.service.GetClientReferralTypes(request)

    """GetClientVisits methods"""

    def GetClientVisits(self, clientId, startDate, endDate, unpaidsOnly):
        request = self.CreateBasicRequest("GetClientVisits")

        request.ClientID = clientId
        request.StartDate = startDate
        request.EndDate = endDate
        request.UnpaidsOnly = unpaidsOnly

        return self.service.service.GetClientVisits(request)

    """GetClients methods"""

    def GetAllClients(self):
        return self.GetClientsByString(" ")

    def GetClientsBySingleId(self, id):
        return self.GetClientsByMultipleIds([id])

    def GetClientsByString(self, searchStr):
        """Convenience method to find clients containing searchStr in their name or e-mail."""
        request = self.CreateBasicRequest("GetClientsRequest")

        # Since SearchText is just a string, we can assign it directly.
        request.SearchText = searchStr

        return self.service.service.GetClients(request)

    def GetClientsByMultipleIds(self, ids):
        request = self.CreateBasicRequest("GetClientsRequest")

        """Here, we create an instance of ArrayOfString (the type of ClientIDs in
           the request) and fill it with our ids before assigning it to our request."""
        clientIDs = self.service.factory.create("ArrayOfString")
        clientIDs.string = ids
        request.ClientIDs = clientIDs

        return self.service.service.GetClients(request)

    """GetClientSchedule methods"""

    def GetClientSchedule(self, clientId, startDate, endDate):
        request = self.CreateBasicRequest("GetClientSchedule")

        request.ClientID = clientId
        request.StartDate = startDate
        request.EndDate = endDate

        return self.service.service.GetClientSchedule(request)

    """GetClientServices methods"""

    def GetClientServices(self, clientId,
                          classId,
                          programIds,
                          sessionTypeIds,
                          locationIds,
                          visitCount,
                          startDate,
                          endDate,
                          showActiveOnly):
        """A few notes about GetClientServices:
            1. If you don't want to pass a Class ID in, pass 0. This acts as you would expect None to.
            2. ProgramIDs is a required field."""
        request = self.CreateBasicRequest("GetClientServices")

        request.ClientID = clientId
        request.ClassID = classId
        request.ProgramIDs = BasicRequestHelper.FillArrayType(self.service, programIds, "Int")
        request.SessionTypeIDs = BasicRequestHelper.FillArrayType(
            self.service, sessionTypeIds, "Int")
        request.LocationIDs = BasicRequestHelper.FillArrayType(self.service, locationIds, "Int")
        request.VisitCount = visitCount
        request.StartDate = startDate
        request.EndDate = endDate
        request.ShowActiveOnly = showActiveOnly

        return self.service.service.GetClientServices(request)

    """GetContactLogTypes methods"""

    def GetContactLogTypes(self):
        request = self.CreateBasicRequest("GetContactLogTypes")

        return self.service.service.GetContactLogTypes(request)

    """GetCustomClientFields methods"""

    def GetCustomClientFields(self):
        request = self.CreateBasicRequest("GetCustomClientFieldsRequest")

        return self.service.service.GetCustomClientFields(request)

    """GetRequiredClientFields methods"""

    def GetRequiredClientFields(self):
        request = self.CreateBasicRequest("GetRequiredClientFields")

        return self.service.service.GetRequiredClientFields(request)

    """SendUserNewPassword methods"""

    def SendUserNewPassword(self, userEmail, userFirstName, userLastName):
        request = self.CreateBasicRequest("SendUserNewPassword")

        request.UserEmail = userEmail
        request.UserFirstName = userFirstName
        request.UserLastName = userLastName

        return self.service.service.SendUserNewPassword(request)

    """UpdateClientServices methods"""

    def UpdateClientServices(self, clientServices, test):
        request = self.CreateBasicRequest("UpdateClientServices")

        ServiceList = self.service.factory.create("ArrayOfClientService")
        ServiceList.ClientService = clientServices

        request.ClientServices = ServiceList
        request.Test = test

        return self.service.service.UpdateClientServices(request)

    """UploadClientDocument methods"""

    def UploadClientDocument(self, clientId, fileName, fileSize):
        request = self.CreateBasicRequest("UploadClientDocument")

        request.ClientID = clientId
        request.FileName = fileName
        request.Bytes = fileSize

        return self.service.service.UploadClientDocument(request)

    """ValidateLogin methods"""

    def ValidateLogin(self, username, password):
        request = self.CreateBasicRequest("ValidateLogin")

        request.Username = username
        request.Password = password

        return self.service.service.ValidateLogin(request)
