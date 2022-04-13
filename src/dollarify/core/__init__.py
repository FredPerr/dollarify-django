from math import floor
from dollarify.models import User, Account
from dollarify.db import Database


class Profile:


    def __init__(self, user_uuid: str):
        self.user = User.get(User, user_uuid)
        self._accounts = None


    @property
    def accounts(self):
        uuids = []
        if self._accounts is None:
            Database.query(f"SELECT uuid, owners FROM {Account.table_name};")
            account_uuids_owners = Database.CURSOR.fetchall()
            for uuid, owners in account_uuids_owners:
                for i in range(floor(len(owners) / User.uuid.max_length) * User.uuid.max_length):
                    if owners[i*32:i*32 + 32] == self.user.uuid:
                        uuids.append(uuid)
                        break
        return uuids

        # TODO: move that into the User model.