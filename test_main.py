import unittest
from unittest.mock import patch, mock_open
import numpy as np
from main import load_file, initialize_maze, bfs, is_valid, reconstruct_path

class TestMazeSolver(unittest.TestCase):

    def setUp(self):
        self.maze_str = [
            "#####\n",
            "#E..#\n",
            "#.#.#\n",
            "#..S#\n",
            "#####\n"
        ]
        self.maze, self.start, self.end = initialize_maze(self.maze_str)

    @patch("builtins.open", new_callable=mock_open, read_data="#####\n#E..#\n#.#.#\n#..S#\n#####\n")
    def test_load_file(self, mock_file):
        file_path = "dummy_path.txt"
        lines = load_file(file_path)
        self.assertEqual(lines, self.maze_str)

    def test_initialize_maze(self):
        expected_maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        self.assertEqual(self.maze, expected_maze)
        self.assertEqual(self.start, (1, 1))
        self.assertEqual(self.end, (3, 3))

    def test_bfs(self):
        path = bfs(self.maze, self.start, self.end)
        expected_path = [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]
        self.assertEqual(path, expected_path)

    def test_is_valid(self):
        self.assertTrue(is_valid(self.maze, 1, 1))
        self.assertFalse(is_valid(self.maze, 0, 0))
        self.assertFalse(is_valid(self.maze, 2, 2))

    def test_reconstruct_path(self):
        visited = {
            (3, 3): (3, 2),
            (3, 2): (3, 1),
            (3, 1): (2, 1),
            (2, 1): (1, 1),
            (1, 1): None
        }
        path = reconstruct_path(visited, self.start, self.end)
        expected_path = [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]
        self.assertEqual(path, expected_path)

if __name__ == "__main__":
    unittest.main()