from api.pb_api import PBAPI


class Accounts(PBAPI):

    def __init__(self, config_file):
        PBAPI.__init__(self, config_file)

        self._response_section = "balances"


class Transactions(PBAPI):

    def __init__(self, config_file):
        PBAPI.__init__(self, config_file)

        self._response_section = "transactions"
