import json
import time
from datetime import datetime

from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import sessionmaker

from src.config import DATABASE_LOC
from src.database.schema_def import Phone, Contact, Date, Address
from src.database.sql_edit_testcases import (CONTACT_ADD_STRING, CONTACT_NAME_UPDATE,
                                             NEW_PHONE, NEW_ADDRESS, NEW_DATE,
                                             UPDATE_PHONE, UPDATE_ADDRESS, UPDATE_DATE,
                                             DELETE_DATE, DELETE_ADDRESS, DELETE_PHONE)


class TableChanges:

    def __init__(self, engine=create_engine(DATABASE_LOC, echo=False, future=True)):
        self.engine = engine
        self.session_maker = sessionmaker(engine, expire_on_commit=True, autocommit=True)

    def add_contact(self, entry):
        entry_row = Contact.from_dict(entry["name"])
        with self.session_maker.begin() as session:
            entry_row.addresses.extend(
                [Address.from_dict(add_dict, add_type) for add_type, add_dict in entry["addresses"].items()]
            )
            entry_row.dates.extend(
                [Date.from_pair(dtype, dval) for dtype, dval in entry["dates"].items()]
            )
            entry_row.phones.extend(
                [Phone.from_pair(ptype, pval) for ptype, pval in entry["phones"].items()]
            )
            session.add(entry_row)
            session.flush()
            cid = entry_row.contact_id

        return cid

    def update_contact_name(self, name_dict, cid):
        with self.session_maker.begin() as session:
            session.execute(update(Contact).
                            where(Contact.contact_id == cid).
                            values(**name_dict))

    def delete_contact(self, cid):
        with self.session_maker.begin() as session:
            session.query(Date).filter_by(contact_id=cid).delete()
            session.query(Phone).filter_by(contact_id=cid).delete()
            session.query(Address).filter_by(contact_id=cid).delete()
            session.execute(delete(Contact).
                            where(Contact.contact_id == cid))

    def add_phone_for_cid(self, phone_pair, cid):
        with self.session_maker.begin() as session:
            phone_entry = Phone.from_pair(*phone_pair)
            phone_entry.contact_id = cid
            session.add(phone_entry)

    def add_address_for_cid(self, address_dict, address_type, cid):
        with self.session_maker.begin() as session:
            ls_keys = list(address_dict.keys())
            for key in ls_keys:
                address_dict[f"{address_type}_{key}"] = address_dict[key]
                del address_dict[key]

            address_entry = Address.from_dict(address_dict, address_type)
            address_entry.contact_id = cid
            session.add(address_entry)

    def add_date_for_cid(self, date_pair, cid):
        with self.session_maker.begin() as session:
            date_entry = Date.from_pair(*date_pair)
            date_entry.contact_id = cid
            session.add(date_entry)

    def update_phone_for_cid(self, old_phone_pair, new_phone_pair, cid):
        optype, opval = old_phone_pair
        ptype, pval = new_phone_pair
        split_pval = pval.split("-")
        split_opval = opval.split("-")
        area = split_pval[0]
        number = "".join(split_pval[1:])
        oarea = split_opval[0]
        onumber = "".join(split_opval[1:])
        with self.session_maker.begin() as session:
            session.execute(update(Phone).
                            where(Phone.contact_id == cid,
                                  Phone.phone_type == optype,
                                  Phone.area_code == oarea,
                                  Phone.number == onumber).
                            values(phone_type=ptype, area_code=area, number=number))

    def update_address_for_cid(self, old_address_dict, old_address_type,
                               new_address_dict, new_address_type, cid):
        self.delete_address_for_cid(old_address_dict, old_address_type, cid)
        self.add_address_for_cid(new_address_dict, new_address_type, cid)

    def update_date_for_cid(self, old_date_pair, new_date_pair, cid):
        dtype, dval = old_date_pair
        ndtype, ndval = new_date_pair
        with self.session_maker.begin() as session:
            session.execute(
                update(Date).
                    where(
                    Date.contact_id == cid,
                    Date.date_type == dtype,
                    Date.date == dval
                ).
                    values(
                    date_type=ndtype,
                    date=datetime.strptime(ndval, "%Y-%m-%d").date()
                )
            )

    def delete_phone_for_cid(self, phone_pair, cid):
        ptype, pval = phone_pair
        split_pval = pval.split("-")
        area = split_pval[0]
        number = "".join(split_pval[1:])
        with self.session_maker.begin() as session:
            session.query(Phone).filter_by(
                contact_id=cid,
                area_code=area,
                number=number,
                phone_type=ptype
            ).delete()

    def delete_address_for_cid(self, address_dict, address_type, cid):
        with self.session_maker.begin() as session:
            session.query(Address).filter_by(
                contact_id=cid,
                address_type=address_type,
                **address_dict
            ).delete()

    def delete_date_for_cid(self, date_pair, cid):
        with self.session_maker.begin() as session:
            session.query(Date).filter_by(
                date_type=date_pair[0],
                contact_id=cid,
                date=date_pair[1]
            ).delete()


if __name__ == "__main__":

    CHECK_CASES = {5}
    x = TableChanges()

    if 1 in CHECK_CASES:
        cid_ = x.add_contact(json.loads(CONTACT_ADD_STRING))
        print(cid_)
        time.sleep(1)

    if 2 in CHECK_CASES:
        x.update_contact_name(*CONTACT_NAME_UPDATE)

    if 3 in CHECK_CASES:
        x.delete_contact(1)

    if 4 in CHECK_CASES:
        x.add_phone_for_cid(*NEW_PHONE)
        x.add_address_for_cid(*NEW_ADDRESS)
        x.add_date_for_cid(*NEW_DATE)

    if 5 in CHECK_CASES:
        x.update_phone_for_cid(*UPDATE_PHONE)
        x.update_address_for_cid(*UPDATE_ADDRESS)
        x.add_date_for_cid(*NEW_DATE)
        x.update_date_for_cid(*UPDATE_DATE)

    if 6 in CHECK_CASES:
        x.delete_date_for_cid(*DELETE_DATE)
        x.delete_address_for_cid(*DELETE_ADDRESS)
        x.delete_phone_for_cid(*DELETE_PHONE)
