# ###################################################
# Copyright (C) 2012 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

import tempfile
import os

import horizons.main

from horizons.constants import BUILDINGS, PRODUCTION
from horizons.world.production.producer import Producer
from tests.gui import TestFinished, gui_test



@gui_test(use_fixture='boatbuilder', timeout=120)
def test_ticket_1224(gui):
	"""
	Boat builder running costs are inconsistent.
	"""
	yield # test needs to be a generator for now

	settlement = gui.session.world.player.settlements[0]
	boatbuilder = settlement.buildings_by_id[BUILDINGS.BOAT_BUILDER][0]

	# Select boat builder
	gui.cursor_click(64, 10, 'left')

	def running_costs():
		c = gui.find(name='BB_main_tab')
		return c.findChild(name='running_costs').text

	# Check (inactive) running costs
	assert running_costs() == '10', "Expected 10, got %s" % running_costs()

	# Select trade ships tab
	gui.trigger('tab_base', '1/action')

	# Build huker
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	# Wait until production starts
	producer = boatbuilder.get_component(Producer)
	while producer._get_current_state() != PRODUCTION.STATES.producing:
		yield

	# Check (active) running costs
	assert running_costs() == '25', "Expected 25, got %s" % running_costs()

	yield TestFinished


@gui_test(use_fixture='boatbuilder', timeout=120)
def test_ticket_1294(gui):
	"""
	Boatbuilder crash with out of order finishing.
	"""
	yield # test needs to be a generator for now

	settlement = gui.session.world.player.settlements[0]
	boatbuilder = settlement.buildings_by_id[BUILDINGS.BOAT_BUILDER][0]

	# Select boat builder
	gui.cursor_click(64, 10, 'left')

	# Select trade ships tab
	gui.trigger('tab_base', '1/action')

	# Build huker
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	# Pause huker construction
	gui.trigger('BB_main_tab', 'toggle_active_active/mouseClicked')

	# Select war ships tab
	gui.trigger('tab_base', '2/action')

	# Build frigate
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	# Wait until production ends
	producer = boatbuilder.get_component(Producer)
	while len(producer.get_productions()) > 1:
		yield

	# Unpause huker construction
	gui.trigger('BB_main_tab', 'toggle_active_inactive/mouseClicked')

	while producer.get_productions():
		yield

	yield TestFinished


@gui_test(use_fixture='boatbuilder', timeout=60)
def test_remove_from_queue(gui):
	"""
	Boatbuilder crashes when canceling a ship in the queue.
	"""
	yield # test needs to be a generator for now

	# Select boat builder
	gui.cursor_click(64, 10, 'left')

	# Select trade ships tab
	gui.trigger('tab_base', '1/action')

	# Build huker
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	# Select war ships tab
	gui.trigger('tab_base', '2/action')

	# Build frigate
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	# Cancel queue -> crash
	gui.trigger('BB_main_tab', 'queue_elem_0/mouseClicked')

	yield TestFinished

@gui_test(use_fixture='boatbuilder', timeout=60)
def test_cancel_ticket_1424(gui):
	"""
	Boatbuilder crashes when canceling a ship build.
	"""
	yield # test needs to be a generator for now

	# Select boat builder
	gui.cursor_click(64, 10, 'left')

	# Select trade ships tab
	gui.trigger('tab_base', '1/action')

	# Build huker
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	# Select war ships tab
	gui.trigger('tab_base', '2/action')

	# Build frigate
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	# Cancel build completely -> crash
	gui.trigger('BB_main_tab', 'BB_cancel_button/mouseClicked')


	yield TestFinished

@gui_test(use_fixture='boatbuilder', timeout=60)
def test_save_load_ticket_1421(gui):
	"""
	Boatbuilder crashes when saving/loading while a ship is being produced.
	"""
	yield # test needs to be a generator for now

	# Select boat builder
	gui.cursor_click(64, 10, 'left')

	# Select trade ships tab
	gui.trigger('tab_base', '1/action')

	# Build huker
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	# Select war ships tab
	gui.trigger('tab_base', '2/action')

	# Build frigate
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	fd, filename = tempfile.mkstemp()
	os.close(fd)

	assert gui.session.save(savegamename=filename)

	horizons.main.load_game( savegame=filename )

	yield TestFinished


@gui_test(use_fixture='boatbuilder', timeout=120)
def test_ticket_1513(gui):
	"""
	Boat builder costs don't go back to normal after cancelling a ship.
	"""
	yield # test needs to be a generator for now

	settlement = gui.session.world.player.settlements[0]
	boatbuilder = settlement.buildings_by_id[BUILDINGS.BOAT_BUILDER][0]

	# Select boat builder
	gui.cursor_click(64, 10, 'left')

	def running_costs():
		c = gui.find(name='BB_main_tab')
		return c.findChild(name='running_costs').text

	# Check (inactive) running costs
	assert running_costs() == '10', "Expected 10, got %s" % running_costs()

	# Select trade ships tab
	gui.trigger('tab_base', '1/action')

	# Build huker
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	# Wait until production starts
	producer = boatbuilder.get_component(Producer)
	while producer._get_current_state() != PRODUCTION.STATES.producing:
		yield

	# Check (active) running costs
	assert running_costs() == '25', "Expected 25, got %s" % running_costs()

	yield

	# Cancel build
	gui.trigger('BB_main_tab', 'BB_cancel_button/mouseClicked')

	# Check (inactive) running costs
	assert running_costs() == '10', "Expected 10, got %s" % running_costs()

	yield TestFinished


@gui_test(use_fixture='boatbuilder', timeout=120)
def test_ticket_1514(gui):
	"""
	Cancelling a ship doesn't update the ship builder's tab.
	"""
	yield # test needs to be a generator for now

	settlement = gui.session.world.player.settlements[0]
	boatbuilder = settlement.buildings_by_id[BUILDINGS.BOAT_BUILDER][0]

	# Select boat builder
	gui.cursor_click(64, 10, 'left')

	# nothing beeing build, no cancel button visible
	assert not gui.find('BB_cancel_button')

	# Select trade ships tab
	gui.trigger('tab_base', '1/action')

	# Build huker
	gui.trigger('boatbuilder_showcase', 'ok_0/action')

	assert gui.find('BB_cancel_button')

	# Wait until production starts
	producer = boatbuilder.get_component(Producer)
	while producer._get_current_state() != PRODUCTION.STATES.producing:
		yield

	yield

	# Cancel build
	gui.trigger('BB_main_tab', 'BB_cancel_button/mouseClicked')

	# The tab should have changed, no cancel button visible
	assert not gui.find('BB_cancel_button')

	yield TestFinished
