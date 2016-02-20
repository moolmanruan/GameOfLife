import unittest
from gameOfLife import GameOfLife, OutOfBoundsError


class TestClass(unittest.TestCase):
    def test_set_cell_state(self):
        game = GameOfLife()
        game.set_alive(1, 1)
        self.assertTrue(game.is_alive(1, 1), "Cell is dead but should be alive")
        game.set_dead(1, 1)
        self.assertFalse(game.is_alive(1, 1), "Cell is alive but should be dead")

    def test_out_of_bounds(self):
        width, height = 5, 3
        game = GameOfLife()
        self.assertRaises(OutOfBoundsError, game.set_alive, 0, 0)
        self.assertRaises(OutOfBoundsError, game.set_dead, width + 1, height + 1)
        self.assertFalse(game.is_alive(0, 0), "Out of bounds cells should always return dead")
        self.assertFalse(game.is_alive(width + 1, height + 1), "Out of bounds cells should always return dead")

    def test_cell_dies_with_no_neighbours(self):
        game = GameOfLife()
        game.set_alive(3, 3)
        self.assertTrue(game.is_alive(3, 3), "Cell should be alive before the tick")
        game.tick()
        self.assertFalse(game.is_alive(3, 3), "Cell should die with no neighbours")

    def test_cell_dies_with_one_neighbour(self):
        game = GameOfLife()
        game.set_alive(3, 3)
        game.set_alive(4, 4)
        self.assertTrue(game.is_alive(3, 3), "Cell should be alive before the tick")
        game.tick()
        self.assertFalse(game.is_alive(3, 3), "Cell should die with one neighbour")

    def test_cell_lives_with_two_neighbours(self):
        game = GameOfLife()
        game.set_alive(3, 3)
        game.set_alive(4, 4)
        game.set_alive(2, 3)
        self.assertTrue(game.is_alive(3, 3), "Cell should be alive before the tick")
        game.tick()
        self.assertTrue(game.is_alive(3, 3), "Cell should survive with two neighbours")

    def test_cell_lives_with_three_neighbours(self):
        game = GameOfLife()
        game.set_alive(3, 3)
        game.set_alive(4, 4)
        game.set_alive(2, 3)
        game.set_alive(4, 3)
        self.assertTrue(game.is_alive(3, 3), "Cell should be alive before the tick")
        game.tick()
        self.assertTrue(game.is_alive(3, 3), "Cell should survive with three neighbours")

    def test_cell_dies_with_more_than_three_neighbours(self):
        game = GameOfLife()
        game.set_alive(3, 3)
        game.set_alive(4, 4)
        game.set_alive(2, 3)
        game.set_alive(4, 3)
        game.set_alive(3, 4)
        self.assertTrue(game.is_alive(3, 3), "Cell should be alive before the tick")
        game.tick()
        self.assertFalse(game.is_alive(3, 3), "Cell should die with 3 or more neighbours")

    def test_cell_becomes_alive_with_three_neighbours(self):
        game = GameOfLife()
        game.set_alive(4, 4)
        game.set_alive(2, 3)
        game.set_alive(4, 3)
        self.assertFalse(game.is_alive(3, 3), "Cell should be dead before the tick")
        game.tick()
        self.assertTrue(game.is_alive(3, 3), "Cell should survive with three neighbours")

    def test_cell_stays_dead_with_two_neighbours(self):
        game = GameOfLife()
        game.set_alive(4, 4)
        game.set_alive(2, 3)
        self.assertFalse(game.is_alive(3, 3), "Cell should be dead before the tick")
        game.tick()
        self.assertFalse(game.is_alive(3, 3), "Cell should not become alive with two neighbours")

    def test_cell_stays_dead_with_four_neighbours(self):
        game = GameOfLife()
        game.set_alive(4, 4)
        game.set_alive(2, 3)
        game.set_alive(4, 3)
        game.set_alive(3, 4)
        self.assertFalse(game.is_alive(3, 3), "Cell should be dead before the tick")
        game.tick()
        self.assertFalse(game.is_alive(3, 3), "Cell should not become alive with four neighbours")

    # Any live cell with fewer than two live neighbours dies, as if caused by under-population.
    # Any live cell with two or three live neighbours lives on to the next generation.
    # Any live cell with more than three live neighbours dies, as if by over-population.
    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
