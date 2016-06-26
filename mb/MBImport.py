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
    def __init__(self, oldsite, newsite):
        self.MBC_old = MBClients.MBClients(oldsite)
        self.MBC_new = MBClients.MBClients(newsite)

    def import_client(self, client_id):
        client = self.MBC_old.get_client(client_id)

        new_client = {}
        fields = self.MBC_new.get_client_fields()
        for field in fields:
            if field in client:
                new_client[field] = client[field]

        # TESTING
        new_client["FirstName"] = 'Test_' + client["FirstName"]
        new_client["LastName"] = 'zzz_' + client["LastName"]
        if 'Username' in client:
            new_client["Username"] = 'z' + client["Username"]
        # Field data overwrites
            new_client["Password"] = client["FirstName"] + client["PostalCode"]
        new_client["Notes"] = self.MBC_old.get_class_history(client_id) + client["Notes"]
        result = self.MBC_new.add_client(new_client)
        return result


if __name__ == "__main__":
    # MBI = MBImport(-99, -99)
    MBI = MBImport(41095, 293010)
    # print MBI.MBC_old.get_class_history('356')
    # logs = MBI.MBC_old.get_contact_logs('004')
    # logs = MBI.MBC_old.get_contact_logs('100011834')
    # logs = MBI.MBC_old.get_contact_logs('100012186')
    # print MBI.MBC_new.add_contact_logs('100012186', logs)
    # for log in logs:
    #     print log, logs[log]
    # print MBI.MBC_new.get_contactlog_mbtransfer_typeid()

    # custom_fields = MBI.MBC_old.get_client_custom_fields('100012186')
    # MBI.MBC_new.add_custom_fields('100011834', custom_fields)
    # TESTING
    # MBI.MBC_old.update_custom_field('100012186','Referral','100011834')
    # MBI.MBC_new.update_custom_field('100011834','Referral','100012186')
    # MBI.MBC_old.update_custom_field('100012186','New ID','100011834')
    # MBI.MBC_new.update_custom_field('100011834','Original ID','100012186')

    # client = MBI.MBC.get_client('004')
    # client = MBI.MBC_old.get_client_indexes('100011834')
    client = MBI.MBC_old.get_client_interests('100009387')
    print client
    # client = MBI.MBC_old.get_classes('004')
    client = MBI.MBC_old.get_class_codes('100009387')
    print sorted(client)
    client = MBI.MBC_old.get_class_history('100009387')
    print client
    # client = MBI.import_client('100014533')
    # client = MBI.import_client('100011834')

    # client = MBI.import_client('100012186')
    # new_client_id = client.Clients.Client[0].ID
    # logs = MBI.MBC_old.get_contact_logs('100012186')
    # MBI.MBC_new.add_contact_logs(new_client_id, logs)
    # print new_client_id
