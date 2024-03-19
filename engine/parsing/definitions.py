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

"""
 ON_PLAY: ADD X DOOM TO CURRENT AGENDA.   game.agenda.card    counter(Tag.DOOM)+=1
 ON_END_OF_TURN: if current_player.hand.contains(self):   current_player.counter(Tag.HORROR) +=2
 ON_ACTION: self.counter(Tag.charge) -=1    pick_enemy()  fight(picked_enemy, current.player.counter(Tag.WILLPOWER), damage_add=1, on_skull="current.player.counter(Tag.WILLPOWER) 
 ON_FAST_ACTION: self.exhaust()  current_player.counter(Tag.HORROR) +=1 self.counter(Tag.Secrets) -=1    if self.counter(Tag.Secrets) == 0:  self.discard(current_player.discard_pile
 ON_SKILL_TEST: skill.result(Tag.WILLPOWER) +=1  
 
  
"""

if __name__ == "__name__":
    raise NotImplementedError()
