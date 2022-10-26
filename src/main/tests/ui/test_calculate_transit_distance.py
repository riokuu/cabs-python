from datetime import datetime
from unittest import TestCase

from geolocation.distance import Distance
from geolocation.address.address_dto import AddressDTO
from dto.client_dto import ClientDTO
from dto.transit_dto import TransitDTO
from entity import Transit
from money import Money
from transitdetails.transit_details_dto import TransitDetailsDTO


class TestCalculateTransitDistance(TestCase):
    def test_should_not_work_with_invalid_unit(self):
        with self.assertRaises(AttributeError):
            self.transit_for_distance(2.00).get_distance("invalid")

    def test_should_represent_as_km(self):
        self.assertEqual("10km", self.transit_for_distance(10).get_distance("km"))
        self.assertEqual("10.123km", self.transit_for_distance(10.123).get_distance("km"))
        self.assertEqual("10.123km", self.transit_for_distance(10.12345).get_distance("km"))
        self.assertEqual("0km", self.transit_for_distance(0).get_distance("km"))

    def test_should_represent_as_meters(self):
        self.assertEqual("10000m", self.transit_for_distance(10).get_distance("m"))
        self.assertEqual("10123m", self.transit_for_distance(10.123).get_distance("m"))
        self.assertEqual("10123m", self.transit_for_distance(10.12345).get_distance("m"))
        self.assertEqual("0m", self.transit_for_distance(0).get_distance("m"))

    def test_should_represent_as_miles(self):
        self.assertEqual("6.214miles", self.transit_for_distance(10).get_distance("miles"))
        self.assertEqual("6.290miles", self.transit_for_distance(10.123).get_distance("miles"))
        self.assertEqual("6.290miles", self.transit_for_distance(10.12345).get_distance("miles"))
        self.assertEqual("0miles", self.transit_for_distance(0).get_distance("miles"))

    def transit_for_distance(self, km: float) -> TransitDTO:
        distance: Distance = Distance.of_km(km)
        transit: Transit = Transit(when=datetime.now(), distance=distance);
        transit.set_price(Money(10))
        transit_details: TransitDetailsDTO = TransitDetailsDTO(
            transit_id=1,
            date_time=datetime.now(),
            completed_at=datetime.now(),
            client=ClientDTO(),
            car_type=None,
            address_from=AddressDTO(),
            address_to=AddressDTO(),
            started=datetime.now(),
            accepted_at=datetime.now(),
            distance=distance,
            tariff=transit.get_tariff(),
        )
        return TransitDTO(transit=transit, transit_details=transit_details)
