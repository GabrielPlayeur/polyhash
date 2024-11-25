from objects import Wind

class TestWind:

    def test_wind_init(self):
        dx,dy = 0,0
        wind = Wind(dx,dy)
        assert type(wind) == Wind
        assert wind.dx==dx and wind.dy==dy and wind.vec==(dx,dy)