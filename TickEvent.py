# -*- coding: utf-8 -*-
#
# File: TickEvent.py
#
# Copyright (c) 2007 by Tomasz J. Kotarba
# Generator: ArchGenXML Version 1.5.2
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Tomasz J. Kotarba <tomasz@kotarba.net>"""
__docformat__ = 'plaintext'

##code-section module-header #fill in your manual code here
from DateTime import DateTime

# tick_logger - begin
from zope.component import adapter
import logging
# tick_logger - end

##/code-section module-header

from Products.TickingMachine.ITickEvent import ITickEvent
import zope

class TickEvent(object):
    """This class implements the ITickEvent interface.
    """
    # zope3 interfaces
    zope.interface.implements(ITickEvent)

    ##code-section class-header_TickEvent #fill in your manual code here
    def __init__(self, date_time, next_tick):
        self.date_time = DateTime(date_time)
        self.next_tick = DateTime(next_tick)
    ##/code-section class-header_TickEvent


##code-section module-footer #fill in your manual code here

@adapter(ITickEvent)
def tick_logger(tick_event):
    """This function is a handler for the ITickEvent. Its purpose is to log all
       ticks.
    """
    l = logging.getLogger('TickingMachine')
    l.info('(%s) TICK detected.' % tick_event.date_time.ISO())

##/code-section module-footer


