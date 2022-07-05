import pytest
from src.assignment07.main import months, date_to_doy, date_verify


def test_date_verify():
    dates_list = [(9, False), ('10/10/10', False), ('12/31/202', False), ('13/31/2022', False), ('01/32/2022', False),
                  ('12/31/2022', True), ('01/31/1989', True), (11/31/2022, False), ('2/31/2022', False),
                  ('1I/31/2022', False), ('-01/31/2022', False), ('12/31/-2022', False)]
    for date in dates_list:
        assert date_verify(date[0]) == date[1]


def test_date_to_doy():
    dates_list = [('01/23/1898', 23, 1898), ('02/10/2020', 41, 2020), ('03/20/2020', 79, 2020),
                  ('04/20/1999', 110, 1999), ('05/20/2020', 140, 2020), ('06/20/2020', 171, 2020),
                  ('07/20/2021', 201, 2021), ('08/31/2023', 243, 2023), ('09/30/2030', 273, 2030),
                  ('10/20/1999', 293, 1999), ('11/20/2020', 324, 2020), ('12/31/2022', 365, 2022)]

    dates_list_bad = [('10/20/1999', 270, 1999), ('11/20/2020', 304, 1220)]

    for date in dates_list:
        assert date_to_doy(date[0]) == (date[1], date[2])

    for date_bad in dates_list_bad:
        assert not date_to_doy(date_bad[0]) == (date_bad[1], date_bad[2])
