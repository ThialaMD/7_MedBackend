import unittest
import datastructure

class TestDataStructure(unittest.TestCase):

    def test_data_storage_initialization(self):
        ds = datastructure.DataStorage()
        self.assertIsNotNone(ds)

    def test_add_and_get_patient(self):
        ds = datastructure.DataStorage()
        name = "John Doe"
        patient = datastructure.Patient(name)
        ds.add_patient(patient)
        retrieved_patient = ds.get_patient(patient.id)
        self.assertEqual(name, retrieved_patient.name)
        self.assertEqual(patient.id, retrieved_patient.id)

if __name__ == '__main__':
    unittest.main()