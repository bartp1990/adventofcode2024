import logging
import numpy as np
from bidict import bidict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

instr_to_dir = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}

class Grid:
    def __init__(self, lines):
        self.grid = np.full((len(lines), len(lines[0])), ".", dtype="<U1")
        self.walls = set()
        self.boxes = []

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                self.grid[y, x] = char
                if char == "@":
                    self.robot_pos = np.array([x, y])
                elif char == "#":
                    self.walls.add((x, y))

    def move(self, instruction):
        direction = instr_to_dir[instruction]

        def move_if_possible(x, y, direction) -> bool:
            swap = False
            next_pos = (x + direction[0], y + direction[1])

            if next_pos[0] < 0 or next_pos[0] >= self.grid.shape[1] or next_pos[1] < 0 or next_pos[1] >= self.grid.shape[0]:
                return False

            next_char = self.grid[next_pos[1], next_pos[0]]
            if next_char == "#":
                return False
            elif next_char in ("[", "]"):
                if direction in ((1,0), (-1, 0)):
                    if move_if_possible(*next_pos, direction):
                        swap = True
                if direction in ((0,1),(0,-1)):
                    if next_char == "[":
                        linked_box_pos = (x + 1 + direction[0], y + direction[1])
                    elif next_char == "]":
                        linked_box_pos = (x - 1 + direction[0], y + direction[1])
                    if move_if_possible(*next_pos, direction) + move_if_possible(*linked_box_pos, direction):
                        swap == True
            elif next_char == ".":
                swap = True

            if swap:
                self.grid[y, x], self.grid[next_pos[1], next_pos[0]] = (
                    self.grid[next_pos[1], next_pos[0]],
                    self.grid[y, x],
                )
                self.robot_pos = np.array([next_pos[0], next_pos[1]])
                return True
            return False

        move_if_possible(self.robot_pos[0], self.robot_pos[1], direction)

    def print(self):
        result = ""
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                result += self.grid[y, x]
            result += "\n"
        result += "\n"
        print(result)


if __name__ == "__main__":
    with open("input.txt") as f:
        file = f.read()

    grid_original, instructions = file.split("\n\n")
    grid_original = grid_original.split("\n")
    instructions = [instr for instr in list(instructions) if instr != "\n"]

    new_grid_map = {
        "#": "##",
        ".": "..",
        "O": "[]",
        "@": "@.",
    }

    grid = []
    for row in grid_original:
        new_row = ""
        for char in row:
            new_row += new_grid_map[char]
        grid.append(new_row)

    grid = Grid(grid)

    grid.print()

    for instruction in instructions:
        print(instruction)
        grid.move(instruction)
        grid.print()

        input()

    sum = 0
    for y in range(0, grid.grid.shape[1]):
        for x in range(0, grid.grid.shape[0]):
            if grid.grid[y, x] == "O":
                sum += 100 * y + x

    part_1 = sum

    assert part_1 == 1436690
    part_2 = None

    logger.info("Advent of Code 2024 | Day 15")
    logger.info(f"Answer part 1: {part_1}")
    logger.info(f"Answer part 2: {part_2}")