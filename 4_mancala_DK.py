# Author: Daniel Kim
# GitHub Username: danielkimGH

class Player:
    """Class definition for Player"""
    def __init__(self, name):
        self._name = name

    def get_name(self):
        """Returns player name"""
        return self._name

class Mancala:
    """Class definition for Mancala"""
    def __init__(self):
        self._board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self._is_game_over = False
        self._player_list = []
        self._p1_opposite_dictionary = {0: 12, 1: 11, 2: 10, 3: 9, 4: 8, 5: 7}
        self._p2_opposite_dictionary = {12: 0, 11: 1, 10: 2, 9: 3, 8: 4, 7: 5}

    def create_player(self, name):
        """Creates player with input string for name"""
        self._player_list.append(Player(name))

    def get_p1_store(self):
        """Returns store for player 1"""
        return self._board[6]

    def get_p2_store(self):
        """Returns store for player 2"""
        return self._board[13]

    def get_p1_pits(self):
        """Returns pits for player 1"""
        return self._board[0:6]

    def get_p2_pits(self):
        """Returns pits for player 2"""
        return self._board[7:13]

    def is_pit_empty(self, player_pit):
        """Returns True if player's pits are all zero, False otherwise"""
        return len(set(player_pit)) == 1 and 0 in set(player_pit)

    def return_winner(self):
        """Returns winner if game is ended"""
        if self._is_game_over is False:
            return "Game has not ended"
        if self.get_p1_store() == self.get_p2_store():
            return "It's a tie"
        elif self.get_p1_store() > self.get_p2_store():
            player_1_name = self._player_list[0].get_name()
            return f"Winner is player 1: {player_1_name}"
        else:
            player_2_name = self._player_list[1].get_name()
            return f"Winner is player 2: {player_2_name}"

    def print_board(self):
        """Prints current board information"""
        print(f"player1:\nstore: {self._board[6]}\n{self._board[0:6]}")
        print(f"player2:\nstore: {self._board[13]}\n{self._board[7:13]}")

    def p1_play_game(self, pit_index):
        """Updates board from player 1 turn"""
        sow = self._board[pit_index - 1]
        self._board[pit_index - 1] = 0
        shifter = 0
        count = sow

        while shifter < sow:
            idx = (pit_index + shifter) % 14
            if idx == 13:       # Lands on opponent's store, skip to next pit
                idx = 0
                shifter += 1
                sow += 1
            self._board[idx] += 1
            shifter += 1
            count -= 1
            if count == 0 and idx == 6:     # special case 1
                print("player 1 take another turn")
            elif count == 0 and idx in [0, 1, 2, 3, 4, 5] and (self._board[idx] - 1 == 0):      # special case 2
                p2_index = self._p1_opposite_dictionary[idx]
                self._board[6] += self._board[p2_index]
                self._board[6] += 1
                self._board[p2_index] = 0
                self._board[idx] = 0

    def p2_play_game(self, pit_index):
        """Updates board from player 2 turn"""
        sow = self._board[pit_index + 6]
        self._board[pit_index + 6] = 0
        shifter = 0
        count = sow

        while shifter < sow:
            shifter += 1
            idx = ((pit_index + 6) + shifter) % 14
            if idx == 6:        # Lands on opponent's store, skip to next pit
                idx = 7
                shifter += 1
                sow += 1
            self._board[idx] += 1
            count -= 1
            if count == 0 and idx == 13:    # special case 1
                print("player 2 take another turn")
            elif count == 0 and idx in [7, 8, 9, 10, 11, 12] and (self._board[idx] - 1 == 0):   # special case 2
                p1_index = self._p2_opposite_dictionary[idx]
                self._board[13] += self._board[p1_index]
                self._board[13] += 1
                self._board[p1_index] = 0
                self._board[idx] = 0

    def check_game_status(self):
        """Sets condition to True if game is over"""
        if self.is_pit_empty(self.get_p1_pits()) is True:
            remaining_total = sum(self.get_p2_pits())
            self._board[13] += remaining_total
            self._board[7:13] = [0] * 6
            self._is_game_over = True

        elif self.is_pit_empty(self.get_p2_pits()) is True:
            remaining_total = sum(self.get_p1_pits())
            self._board[6] += remaining_total
            self._board[0:6] = [0] * 6
            self._is_game_over = True

    def play_game(self, player_number, pit_index):
        """Updates the seeds in the pit & store and checks game status"""
        if pit_index > 6 or pit_index <= 0:
            return "Invalid number for pit index"
        elif self._is_game_over is True:
            return "Game is ended"
        else:
            if player_number == 1:
                self.p1_play_game(pit_index)
            elif player_number == 2:
                self.p2_play_game(pit_index)
            self.check_game_status()
            return self._board
