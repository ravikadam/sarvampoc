from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    location: Optional[str] = None
    building_name: Optional[str] = None
    house_number: Optional[str] = None

class Profile(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    address: Address = Address()
    mobile_number: Optional[str] = None
    email: Optional[str] = None

    def is_complete(self) -> bool:
        return all([
            self.name,
            self.gender,
            self.age,
            self.address.state,
            self.address.city,
            self.address.zipcode,
            self.address.location,
            self.address.building_name,
            self.address.house_number,
            self.mobile_number,
            self.email
        ]) 