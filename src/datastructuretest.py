"""
Unit tests for the backend service data structures.
Fulfils Task 8 of the exercise.
"""

import unittest
import datastructure

class TestDataStructure(unittest.TestCase):
    """Test suite for checking Experiment, Patient, and DataStorage behavior."""

    def setUp(self):
        """Setup a clean DataStorage instance before each test."""
        self.ds = datastructure.DataStorage()
        # Setzt den flüchtigen Speicher für saubere Testbedingungen zurück
        self.ds.patients = []
        self.ds.experiments = []
        self.ds.data_points = []

    def test_create_patient(self):
        """Test if a patient is created correctly with a name and generated ID."""
        patient = datastructure.Patient("Max Mustermann")
        self.assertEqual(patient.name, "Max Mustermann")
        self.assertIsNotNone(patient.id)

    def test_add_and_get_patient(self):
        """Test adding a patient to storage and retrieving them by ID."""
        patient = datastructure.Patient("Anna Müller")
        self.ds.add_patient(patient)
        
        retrieved = self.ds.get_patient(patient.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Anna Müller")

    def test_create_experiment(self):
        """Test if an experiment is created correctly with a name."""
        experiment = datastructure.Experiment("Lungenfunktionstest")
        self.assertEqual(experiment.name, "Lungenfunktionstest")
        self.assertIsNotNone(experiment.id)

    def test_add_and_get_experiment(self):
        """Test adding an experiment and retrieving it."""
        experiment = datastructure.Experiment("Gehtest v1")
        self.ds.add_experiment(experiment)
        
        retrieved = self.ds.get_experiment(experiment.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Gehtest v1")

    def test_get_non_existent_returns_none(self):
        """Test that searching for invalid IDs returns None without crashing."""
        self.assertIsNone(self.ds.get_patient("invalid-id"))
        self.assertIsNone(self.ds.get_experiment("invalid-id"))

if __name__ == '__main__':
    unittest.main()