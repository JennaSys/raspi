import MBClients

import ssl
import logging
# import DebugPrinting

# logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
# log = logging.getLogger('MBImport')
log = logging.getLogger("__main__")
# log.setLevel(logging.DEBUG)
# logging.getLogger('suds.transport').setLevel(logging.INFO)


class MBImport:
    def __init__(self, oldsite, newsite):
        self.MBC_old = MBClients.MBClients(oldsite)
        self.MBC_new = MBClients.MBClients(newsite)

    def import_client(self, client_id):
        try:
            if len(client_id) == 0:
                log.info("Old client ID can not be empty!")
            else:
                log.info("Checking transfer status for ID: {}".format(client_id))
                id_check = self.verify_is_new_id(client_id)
                if id_check is not None:
                    log.info("Old ID {0} has already been transferred to new ID: {1}".format(client_id, id_check))
                    return -1
                else:
                    log.info("Transferring main profile for ID: {}".format(client_id))
                    new_client_id = self.import_profile(client_id)

                    if new_client_id is None:
                        log.info("Client ID '{}' was not transferred!".format(client_id))
                    else:
                        log.info("...Transferring custom fields...")
                        custom_fields = self.MBC_old.get_client_custom_fields(client_id)
                        self.MBC_new.add_custom_fields(new_client_id, custom_fields)

                        log.info("...Updating record ID references...")
                        self.MBC_old.update_custom_field(client_id, 'Referral', new_client_id) # TESTING
                        self.MBC_new.update_custom_field(new_client_id,'Referral',client_id)   # TESTING
                        # MBI.MBC_old.update_custom_field(client_id,'New ID',new_client_id)
                        # MBI.MBC_new.update_custom_field(new_client_id,'Original ID',client_id)

                        log.info("...Transferring contact logs...")
                        contact_logs = self.MBC_old.get_contact_logs(client_id)
                        self.MBC_new.add_contact_logs(new_client_id, contact_logs)

                        log.info("...Retrieving client interests for client types...")
                        interests = self.MBC_old.get_client_interests(client_id)
                        log.info("...Retrieving class history for client types...")
                        class_history = self.MBC_old.get_class_codes(client_id)

                        log.info("...Updating client types...")
                        client_types = ['Bootcamp Only', 'Pool Only', 'Student', 'Blah']  # TESTING
                        # client_types = interests + class_history
                        if len(client_types) > 0:
                            self.MBC_new.set_client_types(new_client_id, client_types)

                        log.info("Client transfer is complete: Old client ID {0} has been imported as new ID: {1}".format(client_id, new_client_id))
                    return new_client_id

        except ssl.SSLError:
            log.error("SSLError: The read operation timed out")
        except Exception as e:
            log.error("ERROR ERROR ERROR!!!")


    def import_profile(self, client_id):
        client = self.MBC_old.get_client(client_id)
        if client is None:
            log.warn("No client record available for ID: {}".format(client_id))
            return None
        else:
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
            try:
                new_client["Notes"] = self.MBC_old.get_class_history(client_id) + client["Notes"]
            except AttributeError:
                new_client["Notes"] = self.MBC_old.get_class_history(client_id)

            result = self.MBC_new.add_client(new_client)
            if result.Status == 'Success' and len(result.Clients) > 0:
                log.debug("Created new profile ID: {}".format(result.Clients.Client[0].ID))
                return result.Clients.Client[0].ID
            else:
                try:
                    log.error("Error transferring main profile: {}".format(result.Clients.Client[0].Messages[0]))
                except AttributeError:
                    log.error("Error transferring main profile: {}".format(result.Message))

                return None

    def verify_is_new_id(self, client_id):
        id_key = 'Referral'  #TESTING
        # id_key = 'New ID'

        id_field = self.MBC_old.read_custom_fields(client_id, [id_key])
        if id_field is not None:
            if id_key in id_field.keys():
                new_id = id_field[id_key]
                if new_id is not None:
                    if len(new_id) > 0:
                        return new_id

        return None


if __name__ == "__main__":
    MBI = MBImport(-99, -99)  # TESTING
    # MBI = MBImport(41095, 293010)

    # print MBI.MBC_old.get_class_history('356')
    # logs = MBI.MBC_old.get_contact_logs('004')
    # logs = MBI.MBC_old.get_contact_logs('100011834')
    # logs = MBI.MBC_old.get_contact_logs('100012186')
    # print MBI.MBC_new.add_contact_logs('100012186', logs)
    # for log in logs:
    #     print log, logs[log]
    # print MBI.MBC_new.get_contactlog_mbtransfer_typeid()

    # custom_fields = MBI.MBC_old.read_custom_fields('100011834', ['Employer', 'Occupation', 'Referral'])
    # print custom_fields
    # MBI.MBC_new.add_custom_fields('100011834', custom_fields)
    # TESTING
    # MBI.MBC_old.update_custom_field('100012186','Referral','100011834')
    # MBI.MBC_new.update_custom_field('100011834','Referral','100012186')
    # MBI.MBC_old.update_custom_field('100012186','New ID','100011834')
    # MBI.MBC_new.update_custom_field('100011834','Original ID','100012186')

    # client = MBI.MBC.get_client('004')
    # client = MBI.MBC_old.get_client_indexes('100011834')
    # client = MBI.MBC_old.get_client_interests('100009387')
    # print client
    # client = MBI.MBC_old.get_classes('004')
    # client = MBI.MBC_old.get_class_codes('100009387')
    # print sorted(client)
    # client = MBI.MBC_old.get_class_history('100009387')
    # print client

    # client = MBI.import_client('100014533')
    # client = MBI.import_client('100011834')

    # client = MBI.import_client('100012186')
    # new_client_id = client.Clients.Client[0].ID
    # logs = MBI.MBC_old.get_contact_logs('100012186')
    # MBI.MBC_new.add_contact_logs(new_client_id, logs)
    # print new_client_id

    client = MBI.import_client('100015083')
    print client