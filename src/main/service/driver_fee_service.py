from entity import DriverFee
from fastapi import Depends
from repository.driver_fee_repository import DriverFeeRepositoryImp
from repository.transit_repository import TransitRepositoryImp


class DriverFeeService:
    driver_fee_repository: DriverFeeRepositoryImp
    transit_repository: TransitRepositoryImp

    def __init__(
            self,
            driver_fee_repository: DriverFeeRepositoryImp = Depends(DriverFeeRepositoryImp),
            transit_repository: TransitRepositoryImp = Depends(TransitRepositoryImp),
    ):
        self.driver_fee_repository = driver_fee_repository
        self.transit_repository = transit_repository

    def calculate_driver_fee(self, transit_id: int) -> int:
        transit = self.transit_repository.get_one(transit_id)
        if transit is None:
            raise AttributeError("transit does not exist, id = " + str(transit_id))
        if transit.drivers_fee is not None:
            return transit.drivers_fee
        transit_price = transit.price
        driver_fee = self.driver_fee_repository.find_by_driver(transit.driver)
        if driver_fee is None:
            raise AttributeError("driver Fees not defined for driver, driver id = " + str(transit.driver.id))
        final_fee = None
        if driver_fee.fee_type == DriverFee.FeeType.FLAT:
            final_fee = transit_price - driver_fee.amount
        else:
            final_fee = transit_price * driver_fee.amount / 100

        return max(final_fee, 0 if driver_fee.min else driver_fee.min)
