===============
Ticking Machine
===============

A Plone product used to create applications which can react to time events

TickingMachine is a Plone product built using Archetypes and Zope3 framework. It adds the notion of a 'server tick' which is, basically, a simple time event triggered at specified intervals (set with a custom portal tool - portal_tickingmachine). This subsystem uses the observer pattern and zope3 events, which means that other subsystems can subscribe to it and get notified each time a tick takes place (thus being able to perceive the time flow and react to it by performing some actions).

The TickingMachine needs an external clock source. You can use the cron daemon, Zope ClockServer or whatever you wish as long as it can invoke the tick() method of the TickingMachine portal tool (e.g. by accessing it via HTTP(s) with its URL).

Tested with Plone 3.0, the product has proven to be production-ready while in use in one of the FTSE100 corporations.


Please note, I created this project for the now ancient version of Plone and stopped maintaining it in 2008 so it is probably of little use. I am putting it here for archiving purposes (too many of my projects were either lost or never open sourced).  After I had stopped maintaining it, this product served as base for the then new collective.timedevents product (see: `here <https://github.com/system7-open-source/collective.timedevents>`_).
