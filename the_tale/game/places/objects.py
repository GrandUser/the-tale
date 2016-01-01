# coding: utf-8
import random
import datetime

from the_tale import amqp_environment

from the_tale.common.utils import bbcode

from the_tale.game import names

from the_tale.game.balance import constants as c
from the_tale.game.balance import formulas as f

from the_tale.game.prototypes import TimePrototype, GameTime

from . import signals
from . import effects
from . import relations


class Place(names.ManageNameMixin2):
    __slots__ = ('id',
                 'x', 'y',
                 'heroes_number',
                 'updated_at',
                 'updated_at_turn',
                 'created_at',
                 'created_at_turn',
                 'habit_honor',
                 'habit_honor_positive',
                 'habit_honor_negative',
                 'habit_peacefulness',
                 'habit_peacefulness_positive',
                 'habit_peacefulness_negative',
                 'is_frontier',
                 'description',
                 'race',
                 'persons_changed_at_turn',
                 'power',
                 'attrs',
                 'utg_name',
                 'races',
                 'nearest_cells',
                 'effects',
                 '_modifier',

                 # mames mixin
                 '_utg_name_form__lazy',
                 '_name__lazy')

    def __init__(self,
                 id,
                 x, y,
                 heroes_number,
                 updated_at,
                 updated_at_turn,
                 created_at,
                 created_at_turn,
                 habit_honor,
                 habit_honor_positive,
                 habit_honor_negative,
                 habit_peacefulness,
                 habit_peacefulness_positive,
                 habit_peacefulness_negative,
                 is_frontier,
                 description,
                 race,
                 persons_changed_at_turn,
                 power,
                 attrs,
                 utg_name,
                 races,
                 nearest_cells,
                 effects,
                 modifier):
        self.id = id
        self.x = x
        self.y = y
        self.heroes_number = heroes_number
        self.updated_at = updated_at
        self.updated_at_turn = updated_at_turn
        self.created_at = created_at
        self.created_at_turn = created_at_turn
        self.habit_honor = habit_honor
        self.habit_honor_positive = habit_honor_positive
        self.habit_honor_negative = habit_honor_negative
        self.habit_peacefulness = habit_peacefulness
        self.habit_peacefulness_positive = habit_peacefulness_positive
        self.habit_peacefulness_negative = habit_peacefulness_negative
        self.is_frontier = is_frontier
        self.description = description
        self.race = race
        self.persons_changed_at_turn = persons_changed_at_turn
        self.power = power
        self.attrs = attrs
        self.utg_name = utg_name
        self.races = races
        self.nearest_cells = nearest_cells
        self.effects = effects
        self._modifier = modifier

    @property
    def updated_at_game_time(self): return GameTime(*f.turns_to_game_time(self.updated_at_turn))

    @property
    def is_new(self):
        return (datetime.datetime.now() - self.created_at).total_seconds() < c.PLACE_NEW_PLACE_LIVETIME

    @property
    def new_for(self):
        return self.created_at + datetime.timedelta(seconds=c.PLACE_NEW_PLACE_LIVETIME)

    def shift(self, dx, dy):
        self.x += dx
        self.y += dy

    @property
    def description_html(self): return bbcode.render(self.description)

    def linguistics_restrictions(self):
        from the_tale.linguistics.relations import TEMPLATE_RESTRICTION_GROUP
        from the_tale.linguistics.storage import restrictions_storage

        restrictions = [restrictions_storage.get_restriction(TEMPLATE_RESTRICTION_GROUP.RACE, self.race.value).id,
                        restrictions_storage.get_restriction(TEMPLATE_RESTRICTION_GROUP.HABIT_HONOR, self.habit_honor.interval.value).id,
                        restrictions_storage.get_restriction(TEMPLATE_RESTRICTION_GROUP.HABIT_PEACEFULNESS, self.habit_honor.interval.value).id,
                        restrictions_storage.get_restriction(TEMPLATE_RESTRICTION_GROUP.TERRAIN, self.terrain.value).id]

        restrictions.extend(self._modifier.linguistics_restrictions())

        return tuple(restrictions)

    @property
    def depends_from_all_heroes(self):
        return self.is_frontier

    def update_heroes_number(self):
        from the_tale.game.heroes.preferences import HeroPreferences
        self.heroes_number = HeroPreferences.count_citizens_of(self, all=self.depends_from_all_heroes)

    def update_heroes_habits(self):
        from the_tale.game.heroes.preferences import HeroPreferences

        habits_values = HeroPreferences.count_habit_values(self, all=self.depends_from_all_heroes)

        self.habit_honor_positive = habits_values[0][0]
        self.habit_honor_negative = habits_values[0][1]
        self.habit_peacefulness_positive = habits_values[1][0]
        self.habit_peacefulness_negative = habits_values[1][1]

    @classmethod
    def _habit_change_speed(cls, current_value, positive, negative):
        positive = abs(positive)
        negative = abs(negative)

        if positive < negative:
            if positive < 0.0001:
                result = -c.PLACE_HABITS_CHANGE_SPEED_MAXIMUM
            else:
                result = -min(c.PLACE_HABITS_CHANGE_SPEED_MAXIMUM, negative / positive)
        elif positive > negative:
            if negative < 0.0001:
                result = c.PLACE_HABITS_CHANGE_SPEED_MAXIMUM
            else:
                result = min(c.PLACE_HABITS_CHANGE_SPEED_MAXIMUM, positive / negative)
        else:
            result = 0

        return result - c.PLACE_HABITS_CHANGE_SPEED_MAXIMUM_PENALTY * (float(current_value) / c.HABITS_BORDER)

    @property
    def habit_honor_change_speed(self):
        return self._habit_change_speed(self.habit_honor.raw_value, self.habit_honor_positive, self.habit_honor_negative)

    @property
    def habit_peacefulness_change_speed(self):
        return self._habit_change_speed(self.habit_peacefulness.raw_value, self.habit_peacefulness_positive, self.habit_peacefulness_negative)

    def sync_habits(self):
        self.habit_honor.change(self.habit_honor_change_speed)
        self.habit_peacefulness.change(self.habit_peacefulness_change_speed)

    def can_habit_event(self):
        return random.uniform(0, 1) < c.PLACE_HABITS_EVENT_PROBABILITY

    @property
    def persons(self):
        from the_tale.game.persons import storage as persons_storage
        return sorted((person for person in persons_storage.persons.all() if person.place_id == self.id),
                      key=lambda p: p.created_at_turn) # fix persons order

    @property
    def total_persons_power(self): return sum([person.power for person in self.persons])

    # @property
    # def modifiers(self):
    #     return sorted([modifier(self) for modifier in modifiers.MODIFIERS.values()], key=lambda m: -m.power)

    def mark_as_updated(self): self.updated_at_turn = TimePrototype.get_current_turn_number()


    @property
    def terrains(self):
        from the_tale.game.map.storage import map_info_storage
        map_info = map_info_storage.item
        terrains = set()
        for cell in self.nearest_cells:
            terrains.add(map_info.terrain[cell[1]][cell[0]])
        return terrains


    @property
    def terrain(self):
        from the_tale.game.map.storage import map_info_storage
        map_info = map_info_storage.item
        return map_info.terrain[self.y][self.x]


    def sync_race(self):
        self.races.update(persons=self.persons)

        dominant_race = self.races.dominant_race

        if dominant_race and self.race != dominant_race:
            old_race = self.race
            self.race = dominant_race
            signals.place_race_changed.send(self.__class__, place=self, old_race=old_race, new_race=self.race)

    def _effects_generator(self):
        from . import storage

        yield effects.Effect(name=u'город', attribute=relations.ATTRIBUTE.TAX, value=0.0)

        yield effects.Effect(name=u'город', attribute=relations.ATTRIBUTE.STABILITY, value=1.0)

        yield effects.Effect(name=u'город', attribute=relations.ATTRIBUTE.ECONOMIC, value=self.attrs.power_economic)

        yield effects.Effect(name=u'город', attribute=relations.ATTRIBUTE.STABILITY_RENEWING_SPEED, value=c.PLACE_STABILITY_RECOVER_SPEED)
        yield effects.Effect(name=u'город', attribute=relations.ATTRIBUTE.POLITIC_RADIUS, value=self.attrs.size*1.25)
        yield effects.Effect(name=u'город', attribute=relations.ATTRIBUTE.TERRAIN_RADIUS, value=self.attrs.size)

        for effect in self.effects.effects:
            yield effect

        for effect in self._modifier.effects:
            yield effect

        for exchange in storage.resource_exchanges.get_exchanges_for_place(self):
            resource_1, resource_2, place_2 = exchange.get_resources_for_place(self)
            if resource_1.parameter is not None:
                yield effects.Effect(name=place_2.name if place_2 is not None else resource_2.text,
                                     attribute=resource_1.parameter,
                                     value=-resource_1.amount * resource_1.direction)
            if resource_2.parameter is not None:
                yield effects.Effect(name=place_2.name if place_2 is not None else resource_1.text,
                                     attribute=resource_2.parameter,
                                     value=resource_2.amount * resource_2.direction)

        # economic
        yield effects.Effect(name=u'экономика', attribute=relations.ATTRIBUTE.PRODUCTION, value=f.place_goods_production(self.attrs.economic))
        yield effects.Effect(name=u'потребление', attribute=relations.ATTRIBUTE.PRODUCTION, value=-f.place_goods_consumption(self.attrs.size))
        yield effects.Effect(name=u'стабильность', attribute=relations.ATTRIBUTE.PRODUCTION, value=(1.0-self.attrs.stability) * c.PLACE_STABILITY_MAX_PRODUCTION_PENALTY)

        if self.attrs.get_next_keepers_goods_spend_amount():
            yield effects.Effect(name=u'дары Хранителей', attribute=relations.ATTRIBUTE.PRODUCTION, value=self.attrs.get_next_keepers_goods_spend_amount())

        # safety
        yield effects.Effect(name=u'город', attribute=relations.ATTRIBUTE.SAFETY, value=1.0)
        yield effects.Effect(name=u'монстры', attribute=relations.ATTRIBUTE.SAFETY, value=-c.BATTLES_PER_TURN)
        yield effects.Effect(name=u'стабильность', attribute=relations.ATTRIBUTE.SAFETY, value=(1.0-self.attrs.stability) * c.PLACE_STABILITY_MAX_SAFETY_PENALTY)

        if self.is_frontier:
            yield effects.Effect(name=u'дикие земли', attribute=relations.ATTRIBUTE.SAFETY, value=-c.WHILD_BATTLES_PER_TURN_BONUS)

        # transport
        yield effects.Effect(name=u'дороги', attribute=relations.ATTRIBUTE.TRANSPORT, value=1.0)
        yield effects.Effect(name=u'трафик', attribute=relations.ATTRIBUTE.TRANSPORT, value=-c.TRANSPORT_FROM_PLACE_SIZE_PENALTY * self.attrs.size)

        if self.is_frontier:
            yield effects.Effect(name=u'бездорожье', attribute=relations.ATTRIBUTE.TRANSPORT, value=-c.WHILD_TRANSPORT_PENALTY)

        yield effects.Effect(name=u'стабильность', attribute=relations.ATTRIBUTE.TRANSPORT, value=(1.0-self.attrs.stability) * c.PLACE_STABILITY_MAX_TRANSPORT_PENALTY)

        # freedom
        yield effects.Effect(name=u'город', attribute=relations.ATTRIBUTE.FREEDOM, value=1.0)
        yield effects.Effect(name=u'стабильность', attribute=relations.ATTRIBUTE.FREEDOM, value=(1.0-self.attrs.stability) * c.PLACE_STABILITY_MAX_FREEDOM_PENALTY)


    def effects_generator(self, order):
        # TODO: do something with postchecks
        safety = 0
        transport = 0
        stability = 0

        for effect in self._effects_generator():
            if effect.attribute.order != order:
                continue
            if effect.attribute.is_SAFETY:
                safety += effect.value
            if effect.attribute.is_TRANSPORT:
                transport += effect.value
            if effect.attribute.is_STABILITY:
                stability += effect.value
            yield effect

        if relations.ATTRIBUTE.SAFETY.order == order:
            if safety < c.PLACE_MIN_SAFETY:
                yield effects.Effect(name=u'Серый Орден', attribute=relations.ATTRIBUTE.SAFETY, value=c.PLACE_MIN_SAFETY - safety)
        if relations.ATTRIBUTE.TRANSPORT.order == order:
            if transport < c.PLACE_MIN_TRANSPORT:
                yield effects.Effect(name=u'Серый Орден', attribute=relations.ATTRIBUTE.TRANSPORT, value=c.PLACE_MIN_TRANSPORT - transport)
        if relations.ATTRIBUTE.STABILITY.order == order:
            if stability < c.PLACE_MIN_STABILITY:
                yield effects.Effect(name=u'Серый Орден', attribute=relations.ATTRIBUTE.STABILITY, value=c.PLACE_MIN_STABILITY - stability)
            if stability > 1:
                yield effects.Effect(name=u'демоны', attribute=relations.ATTRIBUTE.STABILITY, value=1 - stability)

    def all_effects(self):
        for order in relations.ATTRIBUTE.EFFECTS_ORDER:
            for effect in self.effects_generator(order):
                yield effect

    def refresh_attributes(self):
        # self.effects.update_step(self) # TODO: move in highlevel
        self.attrs.reset()

        for effect in self.all_effects():
            effect.apply_to(self)


    def set_modifier(self, modifier):
        self._modifier = modifier
        self.refresh_attributes()


    def cmd_change_power(self, power):
        if amqp_environment.environment.workers.highlevel is None:
            return
        amqp_environment.environment.workers.highlevel.cmd_change_power(power_delta=power,
                                                                        person_id=None,
                                                                        place_id=self.id)


    def map_info(self):
        return {'id': self.id,
                'pos': {'x': self.x, 'y': self.y},
                'race': self.race.value,
                'name': self.name,
                'size': self.size}