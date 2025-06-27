from typing import Optional, Literal
from .exceptions import ERROR_MAP

import requests

class Client:
    def __init__(self, timeout: float = 120.0) -> None:
        self.BASE_URL = "https://app.simplelogin.io"
        self.API_KEY = None
        self.timeout = timeout

    def set_key(self, key: str) -> None:
        self.API_KEY = key
    
    def __handle_error(self, res: requests.Response) -> None:
        data = res.json()
        if str(res.status_code).startswith("4"):
            raise ERROR_MAP.get(data.get("error", "Unknown error"), ERROR_MAP["Unknown error"])
    
    def __req(self, _type: str = "GET", endpoint: str = "", data: dict = {}, params: dict = {}) -> dict:
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {"Authentication": self.API_KEY, "Content-Type": "application/json"}

        if _type == "GET": res = requests.get(url, headers=headers, json=data, params=params, timeout=self.timeout)
        elif _type == "POST": res = requests.post(url, headers=headers, json=data, params=params, timeout=self.timeout)

        self.__handle_error(res)
        data = res.json()
        return data
    
    def get_mailboxes(self) -> list:
        return self.__req("GET", "api/mailboxes").get("mailboxes", [])
    
    def get_alias_options(self) -> dict:
        return self.__req("GET", "api/v5/alias/options")
    
    def get_suffixes(self, deomain: str = "", custom_only: bool = False, no_custom_only: bool = False, premium_only: bool = False, free_only: bool = False) -> dict:
        data = self.get_alias_options()
        suffixes = data.get("suffixes", [])
        authorized_suffixes = []
        
        for suffix in suffixes:
            if premium_only and suffix["is_premium"] is not True: continue
            if free_only and suffix["is_premium"] is not False: continue

            if custom_only and suffix["is_custom"] is not True: continue
            if no_custom_only and suffix["is_custom"] is not False: continue

            if deomain in suffix["suffix"]: authorized_suffixes.append(suffix)
        
        return authorized_suffixes
    
    def create_random_alias(self, hostname: Optional[str], mode: Literal["uuid", "word"] = "", note: Optional[str] = "") -> dict:
        params = {}
        if hostname: params["hostname"] = hostname
        if mode:
            if mode not in ("uuid", "word"):
                raise ValueError("Mode must be either 'uuid' or 'word'.")
            params["mode"] = mode
        
        data = {}
        if note: data["note"] = note
        return self.__req("POST", "api/alias/random/new", data=data, params=params)
    
    def create_custom_alias(self, alias_prefix: str, signed_suffix: str, hostname: Optional[str], mailbox_ids: list = None, note: Optional[str] = "", name: Optional[str] = "") -> dict:
        params = {}
        if hostname: params["hostname"] = hostname
        
        data = {}
        data["alias_prefix"] = alias_prefix.lower()
        data["signed_suffix"] = signed_suffix

        if mailbox_ids is not None: data["mailbox_ids"] = mailbox_ids
        if note: data["note"] = note
        if name: data["name"] = name
        return self.__req("POST", "api/v3/alias/custom/new", data=data, params=params)