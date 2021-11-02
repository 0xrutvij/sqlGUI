from datetime import datetime

import pandas as pd
from sqlalchemy import Column, Integer, String, ForeignKey, Date as Dt
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import create_engine
import json

from src.config import IMPORT_SOURCE, DATABASE_LOC, IMPORT_TEST_SOURCE
from src.database.import_data import csv_to_json

Base = declarative_base()
FOREIGN_KEY = "contact.contact_id"


class Contact(Base):
    __tablename__ = "contact"

    contact_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30))
    middle_name = Column(String(30))
    last_name = Column(String(30))

    addresses = relationship("Address", back_populates="contact")
    phones = relationship("Phone", back_populates="contact")
    dates = relationship("Date", back_populates="contact")

    def __repr__(self):
        return json.dumps({
            "name": {
                'contact_id': self.contact_id,
                'first_name': self.first_name,
                'middle_name': self.middle_name,
                'last_name': self.last_name
            }
        })

    @classmethod
    def from_dict(cls, entry_name):
        return cls(**{k: v for k, v in entry_name.items() if pd.notna(v)})


class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey(FOREIGN_KEY))
    address_type = Column(String(30))
    address = Column(String(100))
    city = Column(String(30))
    state = Column(String(30))
    zip = Column(String(5))

    contact = relationship("Contact", back_populates="addresses")

    def __repr__(self):
        return json.dumps({
            f"{self.address_type}": {
                "address": self.address,
                "city": self.city,
                "state": self.state,
                "zip": self.zip
            }
        })

    @classmethod
    def from_dict(cls, typed_dict, type_address):

        zip_val = typed_dict.get(
            f"{type_address}_zip",
            typed_dict.get(
                "zip",
                None
            )
        )

        zip_inferred = str(int(zip_val)) if pd.notna(zip_val) else None

        x = cls(
            address_type=type_address or None,
            address=typed_dict.get(
                f"{type_address}_address",
                typed_dict.get(
                    "address",
                    None
                )
            ),
            city=typed_dict.get(
                f"{type_address}_city",
                typed_dict.get(
                    "city",
                    None
                )
            ),
            state=typed_dict.get(
                f"{type_address}_state",
                typed_dict.get(
                    "state",
                    None
                )
            ),
            zip=zip_inferred
        )

        if all(map(lambda z: z is None, (v for k, v in x.__dict__.items() if k != "address_type"))):
            return None
        else:
            return x


class Phone(Base):
    __tablename__ = "phone"

    phone_id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey(FOREIGN_KEY))
    phone_type = Column(String(30))
    area_code = Column(String(3))
    number = Column(String(7))

    contact = relationship("Contact", back_populates="phones")

    def __repr__(self):
        return json.dumps({
            f"{self.phone_type}": {
                "area_code": self.area_code,
                "number": self.number
            }
        })

    @classmethod
    def from_pair(cls, key, val):
        if val:
            ph_split = val.split(sep="-")
            return cls(
                phone_type=key,
                area_code=ph_split[0],
                number="".join(ph_split[1:])
            )
        else:
            return None


class Date(Base):
    __tablename__ = "date"

    date_id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey(FOREIGN_KEY))
    date_type = Column(String(30))
    date = Column(Dt())

    contact = relationship("Contact", back_populates="dates")

    def __repr__(self):
        return json.dumps({
            f"{self.date_type}": self.date.strftime("%Y-%m-%d")
        })

    @classmethod
    def from_pair(cls, key, value):
        if value:
            return cls(
                date_type=key,
                date=datetime.strptime(value, "%Y-%m-%d").date()
            )
        else:
            return None


if __name__ == "__main__":
    engine = create_engine(DATABASE_LOC, echo=False, future=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    table_vals = csv_to_json(IMPORT_TEST_SOURCE)

    for i, entry in table_vals.items():
        row = Contact.from_dict(entry["name"])
        for field, data in entry.items():
            if field == "addresses":
                for add_type, add_data in data.items():
                    # print(add_type, add_data)
                    row.addresses.append(Address.from_dict(add_data, add_type))
            elif field == "phones":
                for ph_type, ph_no in data.items():
                    # print(ph_type, ph_no)
                    row.phones.append(Phone.from_pair(ph_type, ph_no))
            elif field == "dates" and data:
                for dtype, date in data.items():
                    # print(dtype, date)
                    row.dates.append(Date.from_pair(dtype, date))

        session.add(row)

    session.commit()
