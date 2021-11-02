import json
from collections import defaultdict

from sqlalchemy import select, func, create_engine, text

from src.database.helpers import phone_dict_from_str, address_dict_from_str, name_dict_from_list, date_dict_from_str
from src.database.schema_def import Phone, Contact, Date, Address
from src.config import DATABASE_LOC


class Queries:

    def __init__(self, engine=create_engine(DATABASE_LOC, echo=False, future=True)):
        self.engine = engine

    def _get_addresses(self):
        with self.engine.connect() as conn:
            address_join = select(
                Contact,
                func.group_concat(
                    (func.upper(Address.address_type) + ": "
                     + Address.address + ", "
                     + Address.city + ", "
                     + Address.state + ", "
                     + Address.zip),
                    "; "
                )
            ).join_from(
                Contact,
                Address,
                isouter=True
            ).group_by(
                Address.contact_id
            )
            results = conn.execute(address_join)
            return [res for res in results]

    def _get_phones(self):
        with self.engine.connect() as conn:
            phone_join = select(
                Contact.contact_id,
                func.group_concat(
                    (func.upper(Phone.phone_type)
                     + ": " + Phone.area_code
                     + "-" + Phone.number),
                    "; "
                )
            ).join_from(
                Contact,
                Phone,
                isouter=True
            ).group_by(
                Phone.contact_id
            )
            results = conn.execute(phone_join)
            return [res for res in results]

    def _get_dates(self):
        with self.engine.connect() as conn:
            date_join = select(
                Contact.contact_id,
                func.group_concat(
                    func.upper(Date.date_type)
                    + ": " + func.strftime('%Y-%m-%d', Date.date),
                    ";")
            ).join(
                Date,
                isouter=True
            ).group_by(
                Date.contact_id
            )

            result = conn.execute(date_join)
            return [res for res in result]

    @classmethod
    def test_private_methods(cls):
        test_obj = cls()
        yield test_obj._get_addresses()
        yield test_obj._get_phones()
        yield test_obj._get_dates()

    def get_combined_contact_info(self):
        contact_cons_dict = defaultdict(list)
        all_cids = set()
        for addr in self._get_addresses():
            cid, info = addr[0], addr[1:]
            contact_cons_dict[cid] += info
            all_cids.add(cid)

        phone_cids = all_cids.copy()
        for phone in self._get_phones():
            cid, info = phone[0], phone[1:]
            if None in info:
                info = [""]
            contact_cons_dict[cid] += info
            phone_cids.remove(cid)

        for cid_left in phone_cids:
            contact_cons_dict[cid_left] += [""]

        date_cids = all_cids.copy()
        for date in self._get_dates():
            cid, info = date[0], date[1:]
            if None in info:
                info = [""]
            contact_cons_dict[cid] += info
            date_cids.remove(cid)

        for cid_left in date_cids:
            contact_cons_dict[cid_left] += [""]

        return contact_cons_dict

    def get_contacts_json(self):
        con_json = {}

        for cid, info in self.get_combined_contact_info().items():
            n_list = info[:3]
            ph_string, add_string, date_string = "", "", ""
            for string in info[3:]:
                if string and "PHONE" in string:
                    ph_string = string
                elif string and "DATE" in string:
                    date_string = string
                elif string:
                    add_string = string

            name_ = name_dict_from_list(n_list)
            adds_ = address_dict_from_str(add_string)
            phs_ = phone_dict_from_str(ph_string)
            dts_ = date_dict_from_str(date_string)
            con_json[cid] = {**name_, **adds_, **phs_, **dts_}

        return con_json

    def search_database(self, search_string):
        with self.engine.connect() as conn:
            search_string = search_string.replace(";", " AND")
            search_string = search_string.replace(",", " OR")
            try:
                res = conn.execute(text(
                    f"""
                        select distinct contact_id
                        from simplified_text_search
                        where simplified_text_search
                        match '{search_string}'
                        """
                ))
            except Exception as e:
                print(e.args)
                return self.get_combined_contact_info(), self.get_contacts_json()

            cids = [r[0] for r in res]
            res_v_cids = conn.execute(text("select contact_id from contact"))
            valid_cids = [r[0] for r in res_v_cids]
            list_dict = Queries().get_combined_contact_info()
            filtered_combined_contact_info = {key: list_dict.get(key, [""]*6) for key in cids if key in valid_cids}
            dict_dict = Queries().get_contacts_json()
            filtered_contacts_json = {key: dict_dict.get(key, {}) for key in cids if key in valid_cids}
            return filtered_combined_contact_info, filtered_contacts_json


if __name__ == "__main__":

    # print(json.dumps(Queries().get_contacts_json(), indent="\t"))
    # print(Queries().get_contacts_json()[1])
    # print(Queries().get_combined_contact_info())
    a, b = Queries().search_database("Dallas; Texas")
    print(a)
    print(b)
