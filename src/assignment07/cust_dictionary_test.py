import pytest
from src.assignment07.main import KEY_PACKAGE_VOLUME, KEY_PACKAGE_WEIGHT, KEY_INTERNATIONAL_DESTINATION as KEY_ID, \
    KEY_DANGEROUS_CONTENTS as KEY_DC, KEY_URGENT
from src.assignment07.main import verified_dictionary, isfloat


def test_isfloat():
    test_cases = [(2, True), (2.88, True), (29999999, True), (-2, True), ('2L', False), ('L', False)]
    for case in test_cases:
        assert isfloat(case[0]) == case[1]


def test_customer_dicts():
    test_cases = [({KEY_PACKAGE_WEIGHT: 3, KEY_PACKAGE_VOLUME: 1, KEY_DC: 'Y', KEY_URGENT: 'Y', KEY_ID: 'Y'}, True),
                  ({KEY_PACKAGE_WEIGHT: 10, KEY_PACKAGE_VOLUME: 2, KEY_DC: 'Y', KEY_URGENT: 'n', KEY_ID: 'Y'}, True),
                  ({KEY_PACKAGE_WEIGHT: 9.9, KEY_PACKAGE_VOLUME: 125, KEY_DC: 'Y', KEY_URGENT: 'y', KEY_ID: 'Y'}, True),
                  ({KEY_PACKAGE_WEIGHT: 8.5, KEY_PACKAGE_VOLUME: 125, KEY_DC: 'Y', KEY_URGENT: 3, KEY_ID: 'Y'}, False),
                  ({KEY_PACKAGE_WEIGHT: 3, KEY_PACKAGE_VOLUME: 125, KEY_DC: 'Y', KEY_URGENT: '0', KEY_ID: 'Y'}, False),
                  ({KEY_PACKAGE_WEIGHT: 26, KEY_PACKAGE_VOLUME: 6, KEY_DC: 'Y', KEY_URGENT: 'n', KEY_ID: 'Y'}, False),
                  ({KEY_PACKAGE_WEIGHT: 3, KEY_PACKAGE_VOLUME: 126, KEY_DC: 'Y', KEY_URGENT: 'n', KEY_ID: 'Y'}, False),
                  ({KEY_PACKAGE_WEIGHT: 5, KEY_PACKAGE_VOLUME: 88, KEY_DC: 'o', KEY_URGENT: 'y', KEY_ID: 'Y'}, False),
                  ({KEY_PACKAGE_WEIGHT: 3, KEY_PACKAGE_VOLUME: 7, KEY_DC: 'Y', KEY_URGENT: 'n', KEY_ID: '!'}, False),
                  ({KEY_PACKAGE_WEIGHT: 1, KEY_PACKAGE_VOLUME: 777, KEY_DC: 9, KEY_URGENT: 'n', KEY_ID: 'Y'}, False),
                  ({KEY_PACKAGE_WEIGHT: -3, KEY_PACKAGE_VOLUME: 75, KEY_DC: 'Y', KEY_URGENT: 56, KEY_ID: 'Y'}, False),
                  ({KEY_PACKAGE_WEIGHT: 2, KEY_PACKAGE_VOLUME: 75, KEY_DC: 'Y', KEY_URGENT: 56, KEY_ID: 'Y'}, False)]
    for case in test_cases:
        assert verified_dictionary(case[0]) == case[1]
