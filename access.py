from enum import Enum


class UserState(Enum):
    Admin = 1
    User = 2
    Banned = 3


class Validator:
    admins = ['245913861']
    allowed = []  # make this list empty if you don't want to restrict users
    banned = []

    def get_type(self, user_id) -> UserState:
        if user_id in self.admins:
            return UserState.Admin

        if user_id in self.banned:
            return UserState.Banned

        return UserState.User

    def validate_access(self, user_id) -> bool:
        if user_id in self.admins:
            return True

        if user_id in self.banned:
            return False

        if len(self.allowed) == 0:
            return True

        return user_id in self.allowed
