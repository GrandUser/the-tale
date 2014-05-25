# coding: utf-8
import time
import datetime

import rels

from django.db import models

from the_tale.common.utils.prototypes import BasePrototype

from the_tale.game.balance import enums as e

from the_tale.game.mobs.storage import mobs_storage

from the_tale.game.map.places.storage import places_storage

from the_tale.game.persons.storage import persons_storage

from the_tale.game.heroes import relations
from the_tale.game.heroes.prototypes import HeroPrototype, HeroPreferencesPrototype


class _PreferencesMetaclass(type):

    @classmethod
    def create_preference_getter(cls, preference):

        def getter(self):
            return self._get(preference)
        getter.__name__ = preference.base_name

        return getter

    @classmethod
    def create_preference_setter(cls, preference):

        def setter(self, value, change_time=None):
            return self._set(preference, value, change_time=change_time)
        setter.__name__ = 'set_%s' % preference.base_name

        return setter

    @classmethod
    def create_preference_reseter(cls, preference):

        def reseter(self):
            return self._reset(preference)
        reseter.__name__ = 'reset_%s' % preference.base_name

        return reseter


    @classmethod
    def create_preference_changed_at_getter(cls, preference):

        def getter(self):
            return self._get_changed_at(preference)
        getter.__name__ = '%s_changed_at' % preference.base_name

        return getter


    def __new__(mcs, name, bases, attributes):

        for preference in relations.PREFERENCE_TYPE.records:
            getter = mcs.create_preference_getter(preference)
            attributes[getter.__name__] = property(getter)

            getter = mcs.create_preference_changed_at_getter(preference)
            attributes[getter.__name__] = property(getter)

            setter = mcs.create_preference_setter(preference)
            attributes[setter.__name__] = setter

            reseter = mcs.create_preference_reseter(preference)
            attributes[reseter.__name__] = reseter

        return super(_PreferencesMetaclass, mcs).__new__(mcs, name, bases, attributes)


class HeroPreferences(object):

    __metaclass__ = _PreferencesMetaclass
    __slots__ = ('data', 'updated', 'hero')

    def __init__(self, hero):
        self.data = {}
        self.updated = False
        self.hero = hero

    def serialize(self):
        return self.data

    @classmethod
    def deserialize(cls, hero, data):
        obj = cls(hero=hero)
        obj.data = data
        return obj

    def can_update(self, preferences_type, current_time):
        return self.time_before_update(preferences_type, current_time).total_seconds() == 0

    def _time_before_update(self, changed_at, current_time):
        return max(datetime.timedelta(seconds=0), (changed_at + datetime.timedelta(seconds=self.hero.preferences_change_delay) - current_time))

    def time_before_update(self, preferences_type, current_time):
        return self._time_before_update(self._get_changed_at(preferences_type), current_time)

    def value_to_set(self, value):
        if isinstance(value, BasePrototype):
            return value.id if value is not None else None
        if isinstance(value, rels.Record):
            return value.value if value is not None else None
        return value

    def _set(self, preferences_type, value, change_time=None):
        self.updated = True

        if change_time is None:
            change_time = datetime.datetime.now()

        value = self.value_to_set(value)

        self.data[preferences_type.base_name] = {'value': value,
                                                 'changed_at': time.mktime(change_time.timetuple())}
        HeroPreferencesPrototype.update(self.hero.id, preferences_type.base_name, value)

    def _reset(self, preferences_type):
        self._set(preferences_type, None, change_time=datetime.datetime.fromtimestamp(0))

    def _prepair_value(self, value):
        return value

    def _prepair_mob(self, mob_id):
        mob = mobs_storage.get(mob_id)

        if mob and not mob.state.is_ENABLED:
            self.set_mob(None, change_time=datetime.datetime.fromtimestamp(0))
            return None

        return mob

    def _prepair_place(self, place_id): return places_storage.get(place_id)

    def _prepair_person(self, person_id): return persons_storage.get(person_id)

    def _prepair_equipment_slot(self, slot_id):
        if slot_id is None: return None
        return relations.EQUIPMENT_SLOT.index_value.get(int(slot_id))

    def _prepair_risk_level(self, risk_id):
        if risk_id is None: return None
        return relations.RISK_LEVEL.index_value.get(int(risk_id))

    def _prepair_archetype(self, archetype_id):
        if archetype_id is None: return None
        return relations.ARCHETYPE.index_value.get(int(archetype_id))

    def _get(self, preferences_type):
        if preferences_type.base_name not in self.data:
            return None

        value = self.data[preferences_type.base_name]['value']

        return getattr(self, preferences_type.prepair_method)(value)

    def _get_changed_at(self, preferences_type, default=datetime.datetime.fromtimestamp(0)):
        if preferences_type.base_name not in self.data:
            return default
        return datetime.datetime.fromtimestamp(self.data[preferences_type.base_name]['changed_at'])

    @property
    def energy_regeneration_type_name(self):
        return e.ANGEL_ENERGY_REGENERATION_TYPES._ID_TO_TEXT[self.energy_regeneration_type]


    # helpers

    @classmethod
    def _preferences_query(cls):
        current_time = datetime.datetime.now()
        return HeroPreferencesPrototype._model_class.objects.filter(hero__ban_state_end_at__lt=current_time, hero__premium_state_end_at__gte=current_time)

    @classmethod
    def _heroes_query(cls):
        current_time = datetime.datetime.now()
        return HeroPrototype._model_class.objects.filter(ban_state_end_at__lt=current_time, premium_state_end_at__gte=current_time)

    @classmethod
    def _place_heroes_query(cls, place):
        persons_ids = [person.id for person in place.persons]

        db_filter = models.Q(place_id=place.id)
        db_filter |= models.Q(friend_id__in=persons_ids)
        db_filter |= models.Q(enemy_id__in=persons_ids)

        return cls._preferences_query().filter(db_filter)

    @classmethod
    def count_friends_of(cls, person):
        return cls._preferences_query().filter(friend_id=person.id).count()

    @classmethod
    def count_enemies_of(cls, person):
        return cls._preferences_query().filter(enemy_id=person.id).count()

    @classmethod
    def count_citizens_of(cls, place):
        return cls._preferences_query().filter(place_id=place.id).count()

    @classmethod
    def get_friends_of(cls, person):
        return [HeroPrototype(model=record) for record in cls._heroes_query().filter(heropreferences__friend_id=person.id)]

    @classmethod
    def get_enemies_of(cls, person):
        return [HeroPrototype(model=record) for record in cls._heroes_query().filter(heropreferences__enemy_id=person.id)]

    @classmethod
    def get_citizens_of(cls, place):
        return [HeroPrototype(model=record) for record in cls._heroes_query().filter(heropreferences__place_id=place.id)]

    @classmethod
    def count_habit_values(cls, place):

        honor_positive = 0
        honor_negative = 0
        peacefulness_positive = 0
        peacefulness_negative = 0

        for honor, peacefulness in cls._place_heroes_query(place).values_list('hero__habit_honor', 'hero__habit_peacefulness'):
            if honor > 0:
                honor_positive += honor
            elif honor < 0:
                honor_negative += honor

            if peacefulness > 0:
                peacefulness_positive += peacefulness
            elif peacefulness < 0:
                peacefulness_negative += peacefulness

        return ( (honor_positive, honor_negative),
                 (peacefulness_positive, peacefulness_negative) )
