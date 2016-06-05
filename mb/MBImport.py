import ClientService
import SiteService
import ClassService
import BasicRequestHelper

import MBClients
import MBClientTypes

import logging
# import DebugPrinting

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('MBImport')
log.setLevel(logging.DEBUG)
# logging.getLogger('suds.transport').setLevel(logging.DEBUG)


class MBImport:
    def __init__(self):
        self.MBC = MBClients.MBClients()

    def import_client(self, client_id):
        client = self.MBC.get_client(client_id)

        new_client = {}
        fields = self.MBC.get_client_fields()
        for field in fields:
            if field in client:
                new_client[field] = client[field]

        new_client["FirstName"] = 'Test_' + client["FirstName"]
        new_client["LastName"] = 'zzz_' + client["LastName"]
        new_client["Username"] = 'z' + client["Username"]
        new_client["Password"] = client["FirstName"] + client["PostalCode"]
        result = self.MBC.add_client(new_client)
        return result


if __name__ == "__main__":
    MBI = MBImport()
    # client = MBI.MBC.get_client('004')
    # client = MBI.import_client('100014533')
    client = MBI.import_client('100011834')
    print client
