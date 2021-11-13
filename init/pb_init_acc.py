import json
import pandas as pd
import requests
from utils import api_utils as au


def load_banking_accounts(config_file):
    api_config = au.load_config_file(config_file, config_section="api")
    destination_config = au.load_config_file(config_file, config_section="destination")
    df = get_accounts(**api_config)
    write_accounts(df, **destination_config)


def get_accounts(url, endpoint, headers) -> pd.DataFrame:
    try:
        response = requests.get(url=url + endpoint, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

    response_json = json.loads(response.text)

    df = pd.DataFrame(response_json['balances'])
    df = df[['acc', 'nameACC', 'currency']]
    return df


def write_accounts(df, db_connection_string, schema, table):
    df.to_sql(name=table, con=db_connection_string, schema=schema, if_exists="replace", method="multi", index=False)


if __name__ == '__main__':
    load_banking_accounts("pb_init_acc.json")
