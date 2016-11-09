import logging
import MBImport

import csv


logging.basicConfig(format='%(asctime)s %(levelname)s: %(funcName)s() --> %(message)s')
log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)

suds_logging_level = logging.INFO
logging.getLogger('suds.transport').setLevel(suds_logging_level)
logging.getLogger('suds.resolver').setLevel(suds_logging_level)
logging.getLogger('suds').setLevel(suds_logging_level)

hdlr = logging.FileHandler('mb_client_transfer.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(funcName)s() --> %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)


def get_client_list():
    fn = 'mb_clients.csv'
    client_list = []
    try:
        with open(fn, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row[3]) > 0:
                    # if len(row[7]) > 0 or len(row[9]) > 0:  # Verify client has a phone or email listed
                    if len(row[4]) > 0 or len(row[5]) > 0 or len(row[6]) > 0 or len(row[7]) > 0:  # Verify client has a phone or email listed
                        client_list.append(row[3])
                    else:
                        # log.warn("*** Client {0} ({1}) has no contact information and will NOT be transferred.".format(row[3], row[2]))
                        log.warn("*** Client {0} ({1},{2}) has no contact information and will NOT be transferred.".format(row[3], row[0], row[1]))

    except IOError as e:
        log.error("get_client_list(): {0} --> {1}".format(e.filename, e.strerror))
    except Exception as e:
        log.error("get_client_list() --> {}".format(e.message))

    return client_list


def import_clients(oldsite, newsite):
    MBI = MBImport.MBImport(oldsite, newsite)
    clients = get_client_list()
    log.info("Beginning BATCH processing of {} records".format(len(clients)))
    for client in clients:
        log.info("Transferring ID: {}".format(client))
        new_id = MBI.import_client(client)
        if new_id is not None:
            log.info("New ID added: {}".format(new_id))


if __name__ == "__main__":
    # import_clients(-99, -99)  # TESTING
    import_clients(41095, 293010)
