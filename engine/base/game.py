"""
    This file is part of tolyn.

    tolyn is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

class GameState:
    def __init__(self):
        self.players = []
        self.encounter_deck = []
        self.act_deck = []
        self.scenario_deck = []
        self.round_ = 0

    def play(self):
        while True:
            self.round_ += 1
            if self.round_ > 1:
                ...








if __name__ == "__name__":
    raise NotImplementedError()

