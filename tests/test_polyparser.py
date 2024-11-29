import pytest
from polyparser import parseChallenge

class TestParserChallenge:

    def test_parser_path_access(self):
        parseChallenge('challenges/a_example.in')
        parseChallenge('challenges/b_small.in')
        parseChallenge('challenges/c_medium.in')
        parseChallenge('challenges/d_final.in')
        with pytest.raises(AssertionError):
            parseChallenge('challenges/azertyui.in')

    def test_parser_data_a(self):
        data = parseChallenge('challenges/a_example.in')
        assert data.rows == 3 and data.columns == 5 and data.altitudes == 3
        assert data.targets_number == 2 and data.radius == 1 and data.balloons == 1 and data.turns == 5
        assert data.starting_cell == (1,2)
        assert len(list(data.targets_pos)) == 2
        assert (0,2) in data.targets_pos
        assert len(data.winds) == 3 and len(data.winds[0]) == 5 and len(data.winds[0][0]) == 4
        assert data.winds[0][0][1] == (0,1)

    def test_parser_data_b(self):
        data = parseChallenge('challenges/b_small.in')
        assert data.rows == 10 and data.columns == 20 and data.altitudes == 2
        assert data.targets_number == 10 and data.radius == 2 and data.balloons == 2 and data.turns == 20
        assert data.starting_cell == (5,10)
        assert len(list(data.targets_pos)) == 10
        assert (9,0) in data.targets_pos
        assert len(data.winds) == 10 and len(data.winds[0]) == 20 and len(data.winds[0][0]) == 3
        assert data.winds[0][0][1] == (2,1)

    def test_parser_data_c(self):
        data = parseChallenge('challenges/c_medium.in')
        assert data.rows == 40 and data.columns == 80 and data.altitudes == 4
        assert data.targets_number == 20 and data.radius == 4 and data.balloons == 10 and data.turns == 40
        assert data.starting_cell == (20,40)
        assert len(list(data.targets_pos)) == 20
        assert (30,54) in data.targets_pos
        assert len(data.winds) == 40 and len(data.winds[0]) == 80 and len(data.winds[0][0]) == 5
        assert data.winds[0][0][1] == (2,-2)

    def test_parser_data_d(self):
        data = parseChallenge('challenges/d_final.in')
        assert data.rows == 75 and data.columns == 300 and data.altitudes == 8
        assert data.targets_number == 2250 and data.radius == 7 and data.balloons == 53 and data.turns == 400
        assert data.starting_cell == (24,167)
        assert len(list(data.targets_pos)) == 2250
        assert (4,113) in data.targets_pos
        assert len(data.winds) == 75 and len(data.winds[0]) == 300 and len(data.winds[0][0]) == 9
        assert data.winds[0][0][1] == (-1,2)