# -*- coding: utf-8 -*-
#
# File: TickingMachine.py
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.TickingMachine.config import *


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
from DateTime.DateTime import DateTime
from zope.event import notify
from TickEvent import TickEvent
##/code-section module-header

schema = Schema((

    #<p>Represents a time when the last tick took place.</p>
    DateTimeField(
        name='lastTick',
        widget=CalendarWidget(
            label='Last tick',
            label_msgid='TickingMachine_label_lastTick',
            i18n_domain='TickingMachine',
        )
    ),

    #<p>Represents expected interval between ticks (in seconds).</p>
    FloatField(
        name='interval',
        default=300.0,
        required=1,
        widget=FloatField._properties['widget'](
            label='Time interval',
            label_msgid='TickingMachine_label_interval',
            i18n_domain='TickingMachine',
            description='A real number representing expected interval ' \
                        'between ticks (in seconds).',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TickingMachine_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TickingMachine(UniqueObject, BaseContent):
    """This is a portal tool which tries to make a Plone site aware of the
       passage of time, thus enabling it to react to time events. It does so by
       dispatching so called 'tick events' (vide the TickEvent class) to all
       its subscribers (via the zope3 event mechanism) each time its 'tick'
       method executes.
       The 'tick' method is a portal action and it should be triggered
       periodically (e.g. by a simple wget script run by a cron daemon).
       The tool stores a time of the last tick and also allows Plone site
       administrators to set a time interval between 'ticks' which serves as a
       safety mechanism to prevent the TickingMachine from unnecesserily
       dispatching tick events to all its subscribers in case a frequency of
       the tick action activation was too high.
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + \
                   (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'TickingMachine'

    meta_type = 'TickingMachine'
    portal_type = 'TickingMachine'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'TickingMachine.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "TickingMachine"
    typeDescMsgId = 'description_edit_tickingmachine'
    #toolicon = 'TickingMachine.gif'


    actions =  (


       {'action': "string:${object_url}/tick",
        'category': "object",
        'id': 'tick',
        'name': 'tick',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = TickingMachine_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_tickingmachine')
        self.setTitle('TickingMachine')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods
    #security.declarePublic('tick')
    def tick(self):
        """This method is a portal action responsible for deciding whether to
           dispatch tick events to the TickEvent subscribers. It should be
           triggered periodically using its URL (e.g. by a simple wget script
           run by a cron daemon).
        """

        # Check current time. 
        current = DateTime()

        # Get lastTick. If it is invalid, set it to the minimum possible value.
        last = self.getLastTick()
        if not isinstance(last, DateTime):
            last = DateTime(0)
        
        # Get interval. Make sure the value used here is no lesser than 0.
        interval = self.getInterval()
        if interval < 0:
            interval = 0

        # If current time less lastTick is equal to or greater than
        # (0.9 * interval) then set lastTick to the current time and
        # execute _notify(). Otherwise do nothing.
        if current.timeTime() - last.timeTime() >= 0.9 * interval:
            self.setLastTick(current)
            notify(TickEvent(current,self.getNextTickEstimation(
                                         last_tick=current,interval=interval)))
    

    def getNextTickEstimation(self, last_tick=None, interval=None):
        """This method tries to estimate a time when a next tick will occur.
           Then it returns a DateTime object representing that time. 
        """
        if last_tick is None:
            last_tick = DateTime(self.getLastTick())
            
        if interval is None:
            interval = float(self.getInterval())
            
        # unit conversion - seconds to days (needed by DateTime)
        interval = interval / 86400.0
        
        # compute a DateTime object for the estimated time
        next_tick_estimation = last_tick + interval
        
        return next_tick_estimation

registerType(TickingMachine, PROJECTNAME)
# end of class TickingMachine

##code-section module-footer #fill in your manual code here
##/code-section module-footer



