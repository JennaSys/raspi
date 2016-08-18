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
                if len(row[0]) > 0:
                    client_list.append(row[0])

    except IOError as e:
        log.error("get_client_list(): {0} --> {1}".format(e.filename, e.strerror))
    except Exception as e:
        log.error("get_client_list() --> {}".format(e.message))
    return client_list


def import_clients(oldsite, newsite):
    MBI = MBImport.MBImport(oldsite, newsite)
    clients = get_client_list()
    for client in clients:
        log.info("Transferring ID: {}".format(client))
        new_id = MBI.import_client(client)
        if new_id is not None:
            log.info("New ID added: {}".format(new_id))


if __name__ == "__main__":
    import_clients(-99, -99)  # TESTING
    # import_clients(41095, 293010)
