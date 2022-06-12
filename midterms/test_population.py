from collections import namedtuple
import unittest
from unittest.mock import patch, Mock

import random

from population import Population


class EvolutionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.population_size = random.randint(100, 1000)
        self.gene_count = random.randint(1, 10)
        self.population = Population.generate_for(size=self.population_size, gene_count=self.gene_count)

    def test_class_exists(self):
        self.assertIsNotNone(Population)

    def test_class_creatures_match_viable_creatures(self):
        self.assertEqual(len(self.viable_creatures), len(self.population.creatures))

    @patch("creature.Creature")
    def test_report_creature_movement_keeps_record_of_first_and_last_positions(self, mock_creature: Mock):
        distances_walked = [(random.random(), random.random(), random.random()) for _ in range(random.randint(1, 10))]
        [self.population.report_movement(mock_creature, dist) for dist in distances_walked]
        actual = self.population.tracker_for(mock_creature)
        self.assertEqual(distances_walked[0], actual.initial)
        self.assertEqual(distances_walked[-1], actual.last)

    def test_elite_duo_shows_creatures_who_travelled_furtest(self):
        creatures = sorted(self.population.creatures)[0:3]
        creature1, creature2, creature3 = creatures
        self.population.report_movement(creature1, (0.1, 0.2, 0.3))
        self.population.report_movement(creature2, (1., 2., 3.))
        self.population.report_movement(creature3, (10., 20., 30.))
        top1, top2 = self.population.elite_duo
        self.assertEqual(top1, creature3)
        self.assertEqual(top2, creature2)
