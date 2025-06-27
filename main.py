from simplelogin import Client
from toml import load
from datetime import datetime
import random
import string

config = load("config.toml")
API_KEY = config.get("API_KEY")
FORWARD_TO = config.get("FORWARD_TO")
HOSTNAME = config.get("HOSTNAME")
MODE = config.get("MODE")
NOTE = config.get("NOTE")
DOMAIN = config.get("DOMAIN")
PREMIUM_ONLY = config.get("PREMIUM_ONLY")
FREE_ONLY = config.get("FREE_ONLY")

RESET = "\u001b[0m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"
GREY = "\u001b[90m"

def log(message, type="inf"):
    colors = {
        "inf": BLUE,
        "suc": GREEN,
        "dbg": YELLOW,
        "err": RED
    }

    print(f"{GREY}{datetime.now().strftime('%H:%M:%S')} {colors.get(type.lower(), WHITE)}{type.upper()} {WHITE}{message}{RESET}")

def main():
    client = Client()
    client.set_key(API_KEY)

    mailboxes = client.get_mailboxes()
    mailbox_ids = []

    for mail in mailboxes:
        if mail["email"] in FORWARD_TO:
            if not mail["verified"]:
                log(f"Mailbox {mail['email']} is not verified.", "err")
                continue
            mailbox_ids.append(mail["id"])

    suffixes = client.get_suffixes(DOMAIN, no_custom_only=True, premium_only=PREMIUM_ONLY, free_only=FREE_ONLY)

    prefix = "".join(random.choice(string.ascii_lowercase) for i in range(15))
    
    alias = client.create_custom_alias(prefix, random.choice(suffixes)["signed_suffix"], HOSTNAME, mailbox_ids, NOTE)
    log(f"Created alias: {alias['alias']}", "suc")

main()