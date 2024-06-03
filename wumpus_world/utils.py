from collections import namedtuple

class Point(namedtuple('Point', 'row col')):
    def move_north(self):
        return Point(self.row - 1, self.col)

    def move_south(self):
        return Point(self.row + 1, self.col)

    def move_west(self):
        return Point(self.row, self.col - 1)

    def move_east(self):
        return Point(self.row, self.col + 1)

    def neighbors(self):
        #상하좌우순
        return [
            self.move_north(),
            self.move_south(),
            self.move_west(),
            self.move_east()
            #Point(self.row - 1, self.col),
            #Point(self.row + 1, self.col),
            #Point(self.row, self.col - 1),
            #Point(self.row, self.col + 1)
        ]