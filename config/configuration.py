from configparser import ConfigParser

config = ConfigParser()

config["DEFAULT"] = {
    "DB_CON": "",
    "CONF_DIR": ""
}

with open("walletconfig.ini", "r") as f:
    config.write(f)