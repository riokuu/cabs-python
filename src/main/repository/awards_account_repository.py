from typing import Optional, List

from injector import inject

from core.database import get_session
from entity import Client, AwardedMiles
from entity.miles.awards_account import AwardsAccount
from sqlmodel import Session


class AwardsAccountRepositoryImp:
    session: Session

    @inject
    def __init__(self, session: Session):
        self.session = session

    def find_by_client_id(self, client_id: int) -> AwardsAccount:
        statement = self.session.query(AwardsAccount).where(AwardsAccount.client_id == client_id)
        results = self.session.exec(statement)
        return results.scalar_one_or_none()

    def find_all_miles_by(self, client: Client) -> List[AwardedMiles]:
        return self.find_by_client_id(client.id).get_miles()

    def save(self, awards_account: AwardsAccount) -> Optional[AwardsAccount]:
        self.session.add(awards_account)
        self.session.commit()
        self.session.refresh(awards_account)
        return awards_account
