import typing
from typing import Optional
import strawberry
from pymongo import MongoClient
from datetime import datetime
import os

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

connect_string = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.z4vhaxi.mongodb.net/Cluster0?retryWrites=true&w=majority"

client = MongoClient(connect_string)
db = client.get_database("ResourceManager")

def datetime_valid(dt_str):
    try:
        datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except:
        return False
    return True


@strawberry.type
class Status:
    training_uptodate: bool
    last_account_activity: str


@strawberry.type
class Account:
    uid: str
    gecos: str
    uidNumber: int
    eppns: typing.List[str]
    status: 'Status'


def get_accounts() -> typing.List[Account]:
    accounts = db["account_collection"].find()
    return [
        Account(uid, gecos, uidNumber, epons, Status(status["training_uptodate"], status["last_account_activity"]))
        for(id, uid, gecos, uidNumber, epons, status) in (
            account.values() for account in accounts
        )
    ]


@strawberry.type
class Query:
    accounts: Account = strawberry.field(resolver=get_accounts)


@strawberry.type
class UpdateAccountSuccess:
    account: Account


@strawberry.type
class UpdateAccountError:
    error_message: str


Response = strawberry.union(
    "UpdateAccountResponse",
    [UpdateAccountSuccess, UpdateAccountError]
)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_account(self, selected_uid: str, updated_uid: Optional[str] = None, gecos: Optional[str] = None, uidNumber: Optional[int] = None, eppns: Optional[typing.List[str]] = None, training_uptodate: Optional[bool] = None, last_account_activity: Optional[str] = None) -> Response:
        if db["account_collection"].find_one({"uid": selected_uid}) is None:
            return UpdateAccountError(
                error_message = f"Selected uid {selected_uid} not found in account collection"
            )
        if selected_uid != updated_uid and db["account_collection"].find_one({"uid": updated_uid}):
            return UpdateAccountError(
                error_message = f"Updated uid {updated_uid} already exists in collection. Duplicate uids are not allowed."
            )
        if db["account_collection"].find_one({"uid": {"$ne": selected_uid}, "uidNumber": uidNumber}):
            return UpdateAccountError(
                error_message=f"Updated uidNumber {uidNumber} already exists in collection. Duplicate uidNumbers are not allowed."
            )
        if last_account_activity is not None and datetime_valid(last_account_activity) == False:
            return UpdateAccountError(
                error_message=f"Invalid datetime iso format string, {last_account_activity}"
            )

        accountToUpdate = {}
        if updated_uid: accountToUpdate["uid"] = updated_uid
        if gecos: accountToUpdate["gecos"] = gecos
        if uidNumber: accountToUpdate["uidNumber"] = uidNumber
        if eppns: accountToUpdate["eppns"] = eppns
        if training_uptodate is not None: accountToUpdate["status.training_uptodate"] = training_uptodate
        if last_account_activity: accountToUpdate["status.last_account_activity"] = last_account_activity

        db["account_collection"].update_one({'uid': selected_uid}, {"$set": accountToUpdate})
        updatedAccount = db["account_collection"].find_one({"uid": updated_uid if updated_uid else selected_uid})

        return UpdateAccountSuccess(account = Account(uid=updatedAccount["uid"],
                       gecos=updatedAccount["gecos"],
                       uidNumber=updatedAccount["uidNumber"],
                       eppns=updatedAccount["eppns"],
                       status=Status(
                           training_uptodate=updatedAccount["status"]["training_uptodate"],
                           last_account_activity=updatedAccount["status"]["last_account_activity"])
                       ))

    @strawberry.mutation
    def update_account_activity(self, uid: str) -> Response:
        if db["account_collection"].find_one({"uid": uid}) is None:
            return UpdateAccountError(
                error_message = f"Selected uid {uid} not found in account collection"
            )
        db["account_collection"].update_one({'uid': uid}, {"$set": {"status.last_account_activity": datetime.now().isoformat()}})
        updatedAccount = db["account_collection"].find_one({"uid": uid})
        return UpdateAccountSuccess(account=Account(uid=updatedAccount["uid"],
                                                    gecos=updatedAccount["gecos"],
                                                    uidNumber=updatedAccount["uidNumber"],
                                                    eppns=updatedAccount["eppns"],
                                                    status=Status(
                                                        training_uptodate=updatedAccount["status"]["training_uptodate"],
                                                        last_account_activity=updatedAccount["status"]["last_account_activity"])
                                                    ))


schema = strawberry.Schema(query=Query, mutation=Mutation)