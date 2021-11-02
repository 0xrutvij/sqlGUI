from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config import DATABASE_LOC, IMPORT_SOURCE
from src.database.import_data import csv_to_json
from src.database.schema_def import Base, Contact, Address, Phone, Date

if __name__ == "__main__":
    engine = create_engine(DATABASE_LOC, echo=False, future=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    table_vals = csv_to_json(IMPORT_SOURCE)

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
