from os.path import exists
from json import dump, load


from shemas.setting import Setting


setting_file = 'setting.json'


if not exists(setting_file):
    with open(setting_file, 'w') as file:
        dump(
            {
                "DATABASE_URL": "mongodb://localhost:27017",
                "SECRET": "SECRET",
                "DATABASE_DB": "stadium",
                "SERVER": {

                },
                "DATABASE": {

                },
                "CORS": {
                    "allow_origins": [
                        "*",
                        "http://localhost",
                        "http://localhost:8080",
                    ],
                    "allow_credentials": True,
                    "allow_methods": ["*"],
                    "allow_headers": ["*"]
                }
            },
            file
        )


with open(setting_file, 'r') as file:
    setting = Setting(**load(file))
