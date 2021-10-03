import json


class Config(object):

    # def get_config_data(self):
    #     try:
    #         with open('config.json', 'r') as f:
    #             json.load(f)
    #     except FileNotFoundError:
    #         with open('config.json', 'w') as f:
    #             data = {
    #                 "api_id": "",
    #                 "api_hash": "",
    #                 "banned_keywords": [],
    #                 "ids_origin": [],
    #                 "link_destinations": []
    #             }
    #             json.dump(data, f)
    #
    # def define_config_data(self, api_id: int, api_hash: str, banned_keywords: list,
    #                        ids_origin: list, link_destinations: list):
    #     with open('config.json', 'w') as f:
    #         data = {
    #             "api_id": int(api_id),
    #             "api_hash": str(api_hash),
    #             "banned_keywords": banned_keywords,
    #             "ids_origin": ids_origin,
    #             "link_destinations": link_destinations
    #         }
    #         json.dump(data, f)
    #     self.get_config_data()

    @staticmethod
    def create_json_config():
        with open('config.json', 'w') as f:
            data = {
                "api_id": 0,
                "api_hash": '',
                "banned_keywords": [],
                "ids_origin": [],
                "link_destinations": []
            }
            json.dump(data, f)

    @staticmethod
    def define_config_var(api_id: int = 0, api_hash: str = '', banned_keywords: tuple = (),
                          ids_origin: tuple = (), link_destinations: tuple = ()):
        with open('config.json', 'r') as f:
            data = json.load(f)

        if api_id != 0:
            data['api_id'] = int(api_id)

        if api_hash != '':
            data['api_hash'] = api_hash

        if len(banned_keywords) != 0:
            data['banned_keywords'] = list(banned_keywords)

        if len(ids_origin) != 0:
            data['ids_origin'] = list(ids_origin)

        if len(link_destinations) != 0:
            data['link_destinations'] = list(link_destinations)

        with open('config.json', 'w') as f:
            json.dump(data, f)

    @staticmethod
    def get_json_config_data():
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError as err:
            print(err)
