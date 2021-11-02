
CONTACT_ADD_STRING = """
        {
            "name": {
                "first_name": "Sherwood",
                "middle_name": NaN,
                "last_name": "Spoerl"
            },
            "addresses": {
                "home": {
                    "home_address": "2287 Sutteridge Park",
                    "home_city": "Dallas",
                    "home_state": "Texas",
                    "home_zip": 75062.0
                },
                "work": {
                    "work_address": "37 Sommers Hill",
                    "work_city": "Addison",
                    "work_state": "Texas",
                    "work_zip": 75006.0
                }
            },
            "phones": {
                "home_phone": "441-557-2835",
                "cell_phone": "907-913-3698",
                "work_phone": "526-691-3663"
            },
            "dates": {
                "birth_date": "1986-06-07"
            }
        }
    """

CONTACT_NAME_UPDATE = [
    {
        "first_name": "Dennis",
        "middle_name": "Michael",
        "last_name": "Mitchell"
    },
    9
]

NEW_PHONE = (("other_phone", "469-4694691"), 1)
DELETE_PHONE = (("other_phone", "469-4694691"), 1)
UPDATE_PHONE = (("home_phone", "597-896-7953"), ("house_phone", "441-557-2835"), 2)


NEW_ADDRESS = (
    {
        "address": "37 Sommers Hill",
        "city": "Addison",
        "state": "Texas",
        "zip": 75006
    },
    "work",
    1
)

DELETE_ADDRESS = (
    {
        "address": "37 Sommers Hill",
        "city": "Addison",
        "state": "Texas",
        "zip": 75006
    },
    "work",
    1
)

UPDATE_ADDRESS = (
    {
        "address": "38 Shoshone Terrace",
        "city": "Dallas",
        "state": "Texas",
        "zip": 75006
    },
    "work",
    {
        "address": "42 Universe Drive",
        "city": "Richardson",
        "state": "Texas",
        "zip": 75006
    },
    "office",
    2
)

NEW_DATE = (("anniversary_date", "2009-10-10"), 1)
DELETE_DATE = (("birth_date", "1977-08-12"), 7)
UPDATE_DATE = (("anniversary_date", "2009-10-10"), ("divorce_date", "2010-10-10"), 1)
