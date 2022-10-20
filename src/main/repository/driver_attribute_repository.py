from typing import Optional

from injector import inject

from entity import DriverAttribute
from sqlmodel import Session


class DriverAttributeRepositoryImp:
    session: Session

    @inject
    def __init__(self, session: Session):
        self.session = session

    def save(self, driver_attribute: DriverAttribute) -> Optional[DriverAttribute]:
        self.session.add(driver_attribute)
        self.session.commit()
        self.session.refresh(driver_attribute)
        return driver_attribute
