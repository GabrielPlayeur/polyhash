from objects import Wind

class TestWind:

    def test_wind_init(self):
        dRow,dCol = 0,0
        wind = Wind(dRow,dCol)
        assert type(wind) == Wind
        assert wind.dRow==dRow and wind.dCol==dCol and wind.vec==(dRow,dCol)