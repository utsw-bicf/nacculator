import unittest
from nacc.uds3.dict.dictionary import getDict
from nacc.uds3.dict.dictionary import getTypes

class Test_dictionary(unittest.TestCase):
    def test_getDict(self):
        self.assertEqual({}, getDict("test"))
        header = {'ptid': {},
            'redcap_event_name': {},
            'formver': {},
            'adcid': {
                '2': 'Boston University',
                '3': 'Case Western University',
                '4': 'Columbia University',
                '5': 'Duke University',
                '6': 'Emory University',
                '7': 'Massachusetts ADRC',
                '8': 'Indiana University',
                '9': 'Johns Hopkins University',
                '10': 'Mayo Clinic',
                '11': 'Mount Sinai',
                '12': 'New York University',
                '13': 'Northwestern University',
                '14': 'Oregon Health & Science University',
                '15': 'Rush University',
                '16': 'University of California, Davis',
                '17': 'University of California, Los Angeles',
                '18': 'University of California, San Diego',
                '19': 'University of Kentucky',
                '20': 'University of Michigan',
                '21': 'University of Pennsylvania',
                '22': 'University of Pittsburgh',
                '25': 'University of Texas Southwestern',
                '26': 'University of Washington',
                '27': 'Washington University in Saint Louis',
                '28': 'University of Alabama',
                '30': 'University of Southern California',
                '31': 'University of California, Irvine',
                '32': 'Stanford University',
                '33': 'Arizona ADC',
                '34': 'University of Arkansas',
                '35': 'University of California, San Francisco',
                '36': 'Florida ADC',
                '37': 'University of Wisconsin',
                '38': 'University of Kansas',
                '39': 'Stanford University #2',
                '40': 'Yale University',
                '41': 'Florida ADRC',
                '42': 'Wake Forest University',
                '43': 'Univeristy of Michigan ADC'
            },
            'visitmo': {},
            'visitday': {},
            'visityr': {},
            'visitnum': {},
            'initials': {},
            'header_complete': {'0': 'incomplete', '1': 'unverified', '2': 'complete'}}
        self.assertEqual(header, getDict("header"))
        fvp_a1 = {'ptid': {},
            'redcap_event_name': {},
            'initials17': {},
            'fu_birthmo': {},
            'fu_birthyr': {},
            'fu_maristat': {'1': 'Married',
            '2': 'Widowed',
            '3': 'Divorced',
            '4': 'Separated',
            '5': 'Never married (or marriage was annulled)',
            '6': 'Living as married/domestic partner',
            '8': 'Other',
            '9': 'Unknown'},
            'fu_sex': {'1': 'Male', '2': 'Female'},
            'fu_livsitua': {'1': 'Lives alone',
            '2': 'Lives with one other person: a spouse or partner',
            '3': 'Lives with one other person: a relative, friend, or roomate',
            '4': 'Lives with caregiver who is not spouse/partner, relative or friend',
            '5': 'Lives with a group (related or not related) in a private residence)',
            '6': 'Lives in a group home (e.g., assisted living, nursing home, or convent)',
            '9': 'Unknown'},
            'fu_independ': {'1': 'Able to live independently',
            '2': 'Requires some assistance with complex activities',
            '3': 'Requires some assistance with basic activities',
            '4': 'Completely dependent',
            '9': 'Unknown'},
            'fu_residenc': {'1': 'Single-, or multi-family private residence (apartment, condo, house)',
            '2': 'Retirement community or independent group living',
            '3': 'Assisted living, adult family home, or boarding home',
            '4': 'Skilled nursing facility, nursing home, hospital, or hospice',
            '5': 'Other',
            '9': 'Unknown'},
            'fu_zip': {},
            'fvp_a1_complete': {'0': 'incomplete', '1': 'unverified', '2': 'complete'}
        }

        self.assertEqual(fvp_a1, getDict("fvp_a1"))
    
    def test_getTypes(self):
        self.assertEqual({}, getTypes("test"))
        types = {'ptid': {'type': 'string'},
            'formver': {'type': 'string'},
            'redcap_event_name': {'type': 'string'},
            'adcid': {'type': 'string'},
            'visitmo': {'type': 'integer'},
            'visitday': {'type': 'integer'},
            'visityr': {'type': 'integer'},
            'visitnum': {'type': 'string'},
            'initials': {'type': 'string'},
            'header_complete': {'type': 'string'}
        }
        self.assertEqual(types, getTypes("header"))
if __name__ == "__main__":
    unittest.main()