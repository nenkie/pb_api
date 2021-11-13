from utils import api_utils as au
import pandas as pd
import requests
import json
import sqlalchemy
import logging

logger = logging.getLogger()


class PBAPI:

    def __init__(self, config_file):
        config_content = au.load_config_file(config_file)
        self._api_config = config_content["api"]
        self._destination_config = config_content["destination"]
        self._acc_config = config_content["acc"]
        self._engine = sqlalchemy.create_engine(self._destination_config['db_connection_string'])

        self._is_interim = True if "interim" in self._api_config["endpoint"] else False

        if not self._is_interim:
            self._sql_lastdate = config_content["sql"]["lastdate"]

    def write_data(self, df, table, db_connection_string, schema):
        logger.debug(f"writing data to sql server")
        df.to_sql(name=table, con=db_connection_string, schema=schema, method="multi", if_exists="append", index=False,
                  chunksize=60)

    def run_request(self, url, endpoint, headers, params, response_section) -> pd.DataFrame:

        return_df = pd.DataFrame()

        while True:

            logger.debug(f"requesting HTTP API data")

            try:
                response = requests.get(url=url + endpoint, headers=headers, params=params)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)

            response_json = json.loads(response.text)

            frame = pd.DataFrame(response_json[response_section])
            return_df = return_df.append(frame)

            if not response_json['exist_next_page']:
                break

            logger.debug(f"exist_next_page = True")
            params["followId"] = response_json["next_page_id"]

        return return_df

    def run_sql(self, query):
        return pd.read_sql_query(sql=query, con=self._engine)

    def get_dates(self, acc, sql):
        logger.debug(f"getting last dates from dwh")
        df = self.run_sql(sql.format(acc))
        start_date = (df.iloc[0]['start_date']).strftime("%d-%m-%Y")
        return start_date

    def load(self):

        logger.debug(f"extracting {self._response_section} from {self._api_config['endpoint']}")

        for account in self._acc_config.values():

            logger.debug(f"started running for account = {account}")

            params = {
                "acc": account,
                "followId": "",
                "limit": 100
            }

            if not self._is_interim:
                logger.debug(f"_is_interim = {self._is_interim}")
                start_date = self.get_dates(account, sql=self._sql_lastdate)
                params["startDate"] = start_date
                logger.debug(f"start date = {start_date}")

            api_config = self._api_config
            api_config["params"] = params

            df = self.run_request(**api_config, response_section=self._response_section)
            if not df.empty:
                self.write_data(df, **self._destination_config)
