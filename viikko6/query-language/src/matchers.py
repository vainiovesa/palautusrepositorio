class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False

        return True


class Or:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if matcher.test(player):
                return True

        return False


class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value


class All:
    def test(self, player):
        return True


class Not:
    def __init__(self, matcher):
        self.matcher = matcher

    def test(self, player):
        return False if self.matcher.test(player) else True


class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value < self._value


class QueryBuilder:
    def __init__(self, query = All()):
        self.query_object = query

    def all(self):
        return QueryBuilder(All(self.query_object))

    def plays_in(self, team):
        return QueryBuilder(And(self.query_object, PlaysIn(team)))

    def has_at_least(self, value, attr):
        return QueryBuilder(And(self.query_object, HasAtLeast(value, attr)))

    def has_fewer_than(self, value, attr):
        return QueryBuilder(And(self.query_object, HasFewerThan(value, attr)))

    def build(self):
        return self.query_object
