from api.pb_load_data import Accounts, Transactions
import utils.log as lg
import logging.config
import json
import sys
import os.path as p

logger = logging.getLogger()
root = p.dirname(sys.argv[0])

if __name__ == "__main__":
    logging.config.dictConfig(json.loads(lg.LOGGING))

    logger.debug("application started")

    # execute truncates

    obj = [Accounts(config_file=p.join(root, "configs/pb_load_acc_snapshots.json")),
           Transactions(config_file=p.join(root, "configs/pb_load_acc_transactions.json")),
           Transactions(config_file=p.join(root, "configs/pb_load_acc_transactions_interim.json"))]

    [o.load() for o in obj]

    # execute merge

    logger.debug("application completed")
