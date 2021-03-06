# coding: utf-8

import mock

from the_tale.amqp_environment import environment

from the_tale.common.utils import testcase

from the_tale.game.logic_storage import LogicStorage

from the_tale.game.logic import create_test_map

from the_tale.game.cards import effects
from the_tale.game.cards.tests.helpers import CardsTestMixin

from the_tale.game.postponed_tasks import ComplexChangeTask


class AddPlacePowerMixin(CardsTestMixin):
    CARD = None

    def setUp(self):
        super(AddPlacePowerMixin, self).setUp()
        self.place_1, self.place_2, self.place_3 = create_test_map()

        self.account_1 = self.accounts_factory.create_account()

        self.storage = LogicStorage()
        self.storage.load_account_data(self.account_1)

        self.hero = self.storage.accounts_to_heroes[self.account_1.id]

        self.card = self.CARD()

        environment.deinitialize()
        environment.initialize()

        self.highlevel = environment.workers.highlevel
        self.highlevel.process_initialize(0, 'highlevel')


    def test_use(self):
        result, step, postsave_actions = self.card.use(**self.use_attributes(hero=self.hero, storage=self.storage, place_id=self.place_1.id))

        self.assertEqual((result, step), (ComplexChangeTask.RESULT.CONTINUE, ComplexChangeTask.STEP.HIGHLEVEL))
        self.assertEqual(len(postsave_actions), 1)

        with mock.patch('the_tale.game.workers.highlevel.Worker.cmd_logic_task') as highlevel_logic_task_counter:
            postsave_actions[0]()

        self.assertEqual(highlevel_logic_task_counter.call_count, 1)

        with mock.patch('the_tale.game.places.logic.PlacePoliticPower.change_power') as change_power:
            result, step, postsave_actions = self.card.use(**self.use_attributes(hero=self.hero,
                                                                                 step=step,
                                                                                 highlevel=self.highlevel,
                                                                                 place_id=self.place_1.id))
        self.assertEqual(change_power.call_args_list,
                         [mock.call(hero_id=self.hero.id, place=self.place_1, power=self.CARD.BONUS, has_in_preferences=True)])

        self.assertEqual((result, step, postsave_actions), (ComplexChangeTask.RESULT.SUCCESSED, ComplexChangeTask.STEP.SUCCESS, ()))


    def test_no_place(self):
        self.assertEqual(self.card.use(**self.use_attributes(hero=self.hero, place_id=666, storage=self.storage)),
                        (ComplexChangeTask.RESULT.FAILED, ComplexChangeTask.STEP.ERROR, ()))


class AddPlacePowerPositiveCommonTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerPositiveCommon

class AddPlacePowerPositiveUncommonTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerPositiveUncommon

class AddPlacePowerPositiveRareTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerPositiveRare

class AddPlacePowerPositiveEpicTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerPositiveEpic

class AddPlacePowerPositiveLegendaryTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerPositiveLegendary


class AddPlacePowerNegativeCommonTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerNegativeCommon

class AddPlacePowerNegativeUncommonTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerNegativeUncommon

class AddPlacePowerNegativeRareTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerNegativeRare

class AddPlacePowerNegativeEpicTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerNegativeEpic

class AddPlacePowerNegativeLegendaryTests(AddPlacePowerMixin, testcase.TestCase):
    CARD = effects.AddPlacePowerNegativeLegendary
