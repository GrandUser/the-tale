# coding: utf-8

from rels import Column
from rels.django import DjangoEnum

from pynames.relations import GENDER as PYNAMES_GENDER

from utg import relations as utg_relations

from the_tale.game.balance.power import  PowerDistribution
from the_tale.game.artifacts.relations import ARTIFACT_POWER_TYPE

from the_tale.game.balance import constants as c
from the_tale.game import technical_words

from the_tale.game.heroes import relations as heroes_relations


class GENDER(DjangoEnum):
    utg_id = Column()
    pynames_id = Column(unique=False)

    records = ( ('MASCULINE', 0, u'мужчина', utg_relations.GENDER.MASCULINE, PYNAMES_GENDER.MALE),
                ('FEMININE', 1, u'женщина', utg_relations.GENDER.FEMININE, PYNAMES_GENDER.FEMALE),
                ('NEUTER', 2, u'оно', utg_relations.GENDER.NEUTER, PYNAMES_GENDER.MALE) )


def _race_linguistics_restrictions(race):
    def _linguistics_restrictions():
        from the_tale.linguistics.relations import TEMPLATE_RESTRICTION_GROUP
        from the_tale.linguistics.storage import restrictions_storage
        return [restrictions_storage.get_restriction(TEMPLATE_RESTRICTION_GROUP.RACE, RACE.index_name[race].value)]
    return _linguistics_restrictions

class RACE(DjangoEnum):
    multiple_text = Column()
    male_text = Column()
    female_text = Column()
    utg_name_form = Column()
    linguistics_restrictions = Column()
    energy_regeneration = Column(related_name='base_race')

    records = ( ('HUMAN', 0, u'человек', u'люди', u'мужчина', u'женщина',
                 technical_words.RACE_HUMANS, _race_linguistics_restrictions('HUMAN'), heroes_relations.ENERGY_REGENERATION.PRAY),
                ('ELF', 1, u'эльф', u'эльфы', u'эльф', u'эльфийка',
                 technical_words.RACE_ELFS, _race_linguistics_restrictions('ELF'), heroes_relations.ENERGY_REGENERATION.INCENSE),
                ('ORC', 2, u'орк',  u'орки', u'орк', u'оркесса',
                 technical_words.RACE_ORCS, _race_linguistics_restrictions('ORC'), heroes_relations.ENERGY_REGENERATION.SACRIFICE),
                ('GOBLIN', 3, u'гоблин', u'гоблины', u'гоблин', u'гоблинша',
                 technical_words.RACE_GOBLINS, _race_linguistics_restrictions('GOBLIN'), heroes_relations.ENERGY_REGENERATION.MEDITATION),
                ('DWARF', 4, u'дварф', u'дварфы', u'дварф', u'дварфийка',
                 technical_words.RACE_DWARFS, _race_linguistics_restrictions('DWARF'), heroes_relations.ENERGY_REGENERATION.SYMBOLS) )


class GAME_STATE(DjangoEnum):

    records = ( ('STOPPED', 0, u'остановлена'),
                ('WORKING', 1, u'запущена')  )



class HABIT_INTERVAL(DjangoEnum):
    female_text = Column()
    neuter_text = Column()
    place_text = Column()
    left_border = Column()
    right_border = Column()


class HABIT_HONOR_INTERVAL(HABIT_INTERVAL):
    records = ( ('LEFT_3', 0, u'бесчестный', u'бесчестная', u'бесчестное', u'криминальная столица', -c.HABITS_BORDER, c.HABITS_RIGHT_BORDERS[0]),
                ('LEFT_2', 1, u'подлый', u'подлая', u'подлое', u'бандитская вотчина', c.HABITS_RIGHT_BORDERS[0], c.HABITS_RIGHT_BORDERS[1]),
                ('LEFT_1', 2, u'порочный', u'порочная', u'порочное', u'неблагополучный город', c.HABITS_RIGHT_BORDERS[1], c.HABITS_RIGHT_BORDERS[2]),
                ('NEUTRAL', 3, u'себе на уме', u'себе на уме', u'себе на уме', u'обычный город', c.HABITS_RIGHT_BORDERS[2], c.HABITS_RIGHT_BORDERS[3]),
                ('RIGHT_1', 4, u'порядочный', u'порядочная', u'порядочное', u'благополучное поселение', c.HABITS_RIGHT_BORDERS[3], c.HABITS_RIGHT_BORDERS[4]),
                ('RIGHT_2', 5, u'благородный', u'благородная', u'благородное', u'честный город', c.HABITS_RIGHT_BORDERS[4], c.HABITS_RIGHT_BORDERS[5]),
                ('RIGHT_3', 6, u'хозяин своего слова', u'хозяйка своего слова', u'хозяин своего слова', u'оплот благородства', c.HABITS_RIGHT_BORDERS[5], c.HABITS_BORDER) )


class HABIT_PEACEFULNESS_INTERVAL(HABIT_INTERVAL):
    records = ( ('LEFT_3', 0, u'скорый на расправу', u'скорая на расправу', u'скорое на расправу', u'территория вендетт', -c.HABITS_BORDER, c.HABITS_RIGHT_BORDERS[0]),
                ('LEFT_2', 1, u'вспыльчивый', u'вспыльчивая', u'вспыльчивое', u'пристанище горячих голов', c.HABITS_RIGHT_BORDERS[0], c.HABITS_RIGHT_BORDERS[1]),
                ('LEFT_1', 2, u'задира', u'задира', u'задира', u'беспокойное место', c.HABITS_RIGHT_BORDERS[1], c.HABITS_RIGHT_BORDERS[2]),
                ('NEUTRAL', 3, u'сдержанный', u'сдержанная', u'сдержаное', u'неприметное поселение', c.HABITS_RIGHT_BORDERS[2], c.HABITS_RIGHT_BORDERS[3]),
                ('RIGHT_1', 4, u'доброхот', u'доброхот', u'доброхот', u'спокойное место', c.HABITS_RIGHT_BORDERS[3], c.HABITS_RIGHT_BORDERS[4]),
                ('RIGHT_2', 5, u'миролюбивый', u'миролюбивая', u'миролюбивое', u'мирное поселение', c.HABITS_RIGHT_BORDERS[4], c.HABITS_RIGHT_BORDERS[5]),
                ('RIGHT_3', 6, u'гуманист', u'гуманист', u'гуманист', u'центр цивилизации', c.HABITS_RIGHT_BORDERS[5], c.HABITS_BORDER) )


class HABIT_TYPE(DjangoEnum):
    intervals = Column()
    plural_accusative = Column()
    verbose_value = Column()

    records = ( ('HONOR', 0, u'честь', HABIT_HONOR_INTERVAL, u'чести', 'honor'),
                ('PEACEFULNESS', 1, u'миролюбие', HABIT_PEACEFULNESS_INTERVAL, u'миролюбия', 'peacefulness') )


class ARCHETYPE(DjangoEnum):
    power_distribution = Column()
    description = Column()
    allowed_power_types = Column(no_index=True, unique=False)

    records = ( (u'MAGICAL', 0, u'маг', PowerDistribution(0.25, 0.75), u'герой предпочитает магию грубой силе', [ARTIFACT_POWER_TYPE.MOST_MAGICAL,
                                                                                                                 ARTIFACT_POWER_TYPE.MAGICAL,
                                                                                                                 ARTIFACT_POWER_TYPE.NEUTRAL]),
                (u'NEUTRAL', 1, u'авантюрист', PowerDistribution(0.5, 0.5), u'герой соблюдает баланс между мечом и магией', [ARTIFACT_POWER_TYPE.MAGICAL,
                                                                                                                             ARTIFACT_POWER_TYPE.NEUTRAL,
                                                                                                                             ARTIFACT_POWER_TYPE.PHYSICAL]),
                (u'PHYSICAL', 2, u'воин', PowerDistribution(0.75, 0.25), u'герой полагается на воинские умения', [ARTIFACT_POWER_TYPE.NEUTRAL,
                                                                                                                  ARTIFACT_POWER_TYPE.PHYSICAL,
                                                                                                                  ARTIFACT_POWER_TYPE.MOST_PHYSICAL]) )


class SUPERVISOR_TASK_TYPE(DjangoEnum):
    records = (('ARENA_PVP_1X1', 0, u'создать pvp бой на арене'),)

class SUPERVISOR_TASK_STATE(DjangoEnum):
    records = ( ('WAITING', 0, u'ожидает ресурсы'),
                ('PROCESSED', 1, u'обработана'),
                ('ERROR', 2, u'ошибка при обработке'), )

class COMMUNICATION_VERBAL(DjangoEnum):
    records = ( ('CAN_NOT', 0, u'не может'),
                ('CAN', 1, u'может'), )

class COMMUNICATION_GESTURES(DjangoEnum):
    records = ( ('CAN_NOT', 0, u'не может'),
                ('CAN', 1, u'может'), )

class COMMUNICATION_TELEPATHIC(DjangoEnum):
    records = ( ('CAN_NOT', 0, u'не может'),
                ('CAN', 1, u'может'), )

class INTELLECT_LEVEL(DjangoEnum):
    records = ( ('NONE', 0, u'отсутствует'),
                ('REFLEXES', 1, u'рефлексы'),
                ('INSTINCTS', 2, u'инстинкты'),
                ('LOW', 3, u'низкий'),
                ('NORMAL', 4, u'нормальный'),
                ('HIGHT', 5, u'гений') )

class ACTOR(DjangoEnum):
    records = ( ('HERO', 0, u'герой'),
                ('MOB', 1, u'монстр'),
                ('PERSON', 2, u'Мастер'),
                ('COMPANION', 3, u'спутник')  )


class BEING_TYPE(DjangoEnum):
    companion_heal_modifier = Column(unique=False)
    companion_coherence_modifier = Column(unique=False)

    records = ( (u'PLANT', 0, u'растения', heroes_relations.MODIFIERS.COMPANION_LIVING_HEAL, heroes_relations.MODIFIERS.COMPANION_LIVING_COHERENCE_SPEED),
                (u'ANIMAL', 1, u'животные', heroes_relations.MODIFIERS.COMPANION_LIVING_HEAL, heroes_relations.MODIFIERS.COMPANION_LIVING_COHERENCE_SPEED),
                (u'SUPERNATURAL', 2, u'стихийные существа', heroes_relations.MODIFIERS.COMPANION_UNUSUAL_HEAL, heroes_relations.MODIFIERS.COMPANION_UNUSUAL_COHERENCE_SPEED),
                (u'MECHANICAL', 3, u'конструкты', heroes_relations.MODIFIERS.COMPANION_CONSTRUCT_HEAL, heroes_relations.MODIFIERS.COMPANION_CONSTRUCT_COHERENCE_SPEED),
                # (u'BARBARIAN', 4, u'дикари', heroes_relations.MODIFIERS.COMPANION_LIVING_HEAL, heroes_relations.MODIFIERS.COMPANION_LIVING_COHERENCE_SPEED),
                (u'CIVILIZED', 5, u'разумные двуногие', heroes_relations.MODIFIERS.COMPANION_LIVING_HEAL, heroes_relations.MODIFIERS.COMPANION_LIVING_COHERENCE_SPEED),
                (u'COLDBLOODED', 6, u'хладнокровные гады', heroes_relations.MODIFIERS.COMPANION_LIVING_HEAL, heroes_relations.MODIFIERS.COMPANION_LIVING_COHERENCE_SPEED),
                (u'INSECT', 7, u'насекомые', heroes_relations.MODIFIERS.COMPANION_LIVING_HEAL, heroes_relations.MODIFIERS.COMPANION_LIVING_COHERENCE_SPEED),
                (u'DEMON', 8, u'демоны', heroes_relations.MODIFIERS.COMPANION_UNUSUAL_HEAL, heroes_relations.MODIFIERS.COMPANION_UNUSUAL_COHERENCE_SPEED),
                (u'UNDEAD', 9, u'нежить', heroes_relations.MODIFIERS.COMPANION_UNUSUAL_HEAL, heroes_relations.MODIFIERS.COMPANION_UNUSUAL_COHERENCE_SPEED),
                (u'MONSTER', 10, u'чудовища', heroes_relations.MODIFIERS.COMPANION_UNUSUAL_HEAL, heroes_relations.MODIFIERS.COMPANION_UNUSUAL_COHERENCE_SPEED),
                (u'CHIMERA', 11, u'химеры', heroes_relations.MODIFIERS.COMPANION_UNUSUAL_HEAL, heroes_relations.MODIFIERS.COMPANION_UNUSUAL_COHERENCE_SPEED) )
