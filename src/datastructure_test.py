import unittest

import datastructure

class TestPatient(unittest.TestCase):

    def test_create_patient(self):
        obj = datastructure.Patient('David Herzig')
        self.assertTrue(len(obj.id) > 0)

        id = obj.id

        ds = datastructure.DataStorage()
        ds.add_patient(obj)

        patient = ds.get_patient(id)
        self.assertTrue(obj.name == patient.name)

if __name__ == '__main__':
    unittest.main()