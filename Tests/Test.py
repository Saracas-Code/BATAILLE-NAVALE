import unittest

from TestCombinatoire import TestCombinatoire
from TestAleatoire import TestSimulationAleatoire
from TestHeuristique import TestSimulationHeuristique
from TestProbabiliste import TestSimulationProbabilisteSimplifiee
from TestRechercheObjetPerdu import TestRechercheObjetPerdu


if __name__ == "__main__":

    # Lancer les tests unitaires de TestAleatoire
    suite = unittest.TestSuite()
    
    # Ajouter les tests aléatoires et heuristiques à la suite
     # Créer une suite de tests
    suite = unittest.TestSuite()

    # Ajouter les tests aléatoires, heuristiques et probabilistes à la suite
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCombinatoire))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimulationAleatoire))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimulationHeuristique))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimulationProbabilisteSimplifiee))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRechercheObjetPerdu))

    # Exécuter la suite de tests
    runner = unittest.TextTestRunner()
    runner.run(suite)