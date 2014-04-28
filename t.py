#!/usr/bin/env python
from storm.locals import *
import sys

class Instrument(object):
    __storm_table__ = "instrument"
    id = Int(allow_none=False)
    name = Unicode(allow_none=False, primary=True)
    locations = Unicode()
    def __init__(self, name):
        self.name = name
        
class Loc(object):
    __storm_table__ = "location"
    #instrument_id = Int(primary=True)
    instrument_name = Unicode(allow_none=False, primary=True)
    id = Int(allow_none=False)
    instrument = Reference(instrument_name, Instrument.name)
    name = Unicode(allow_none=False)
    #components = Unicode()
    locations = Reference(Instrument.locations, name)
    
class Location(Loc):
    def __init__(self, name):
        self.name = name
        #self.initialize()

class Component(Location):
    __storm_table__ = "component"
    id = Int(allow_none=False)#primary=True)   
    location_name = Unicode(allow_none=False) 
    location = Reference(location_name, Location.name)
    devices = Unicode()
    
    def __init__(self, name):
        self.name = name
        
class MotorManager(object):
    def __init__(self, scheme, user, passwd, hostname, port, dbname, parent=None):
        #database = create_database("sqlite:")
        dbpars   = (scheme, user, passwd, hostname, port, dbname)
        database = create_database("%s://%s:%s@%s:%s/%s" % dbpars)        
        self.store = Store(database)
        
    def create_alltables(self):
        try:
            self.store.execute("CREATE TABLE instrument "
                               "(id INTEGER  PRIMARY KEY, name VARCHAR, locations VARCHAR)", noresult=True)
            
            self.store.execute("CREATE TABLE location "
                               "(id INTEGER PRIMARY KEY, instrument_name VARCHAR, name VARCHAR, components VARCHAR)", noresult=True)

            self.store.execute("CREATE TABLE component "
                               "(id INTEGER PRIMARY KEY, instrument_name VARCHAR, location_name VARCHAR, name VARCHAR, devices VARCHAR)", noresult=True)            
        except:
            pass
        
    def commit(self):
        self.store.commit()

    def roolback(self):
        self.store.rollback()
        
    def addinstrument(self, instrument_name=None): 
        # CHECK IF INSTRUMENT ALREADY EXISTS:
        instrument = self.getinstrument(instrument_name)
        if instrument:
            if instrument.name == instrument_name:
                print 'Instrument %s already exists' % instrument.name
                return instrument        
        newinstrument = Instrument(unicode(instrument_name))
        print 'Creating New Instrument', newinstrument.name
        self.commit()
        return newinstrument

    def addlocation(self, location_name=None, instrument=None):
        if instrument:
            location = self.getlocation(location_name)
            if location:
                if location.name == location_name:
                    print 'Location %s already exists in' % location.name, location.instrument.name
                    return location
            newlocation = Location(unicode(location_name))
            newlocation.instrument = instrument
            print 'Creating New Location', newlocation.name, 'in instrument', instrument.name
            self.commit()
            return newlocation
        return None

    def addcomponent(self, component_name=None, location=None):
        if location:
            component = self.getcomponent(component_name)
            if component:
                if component.name == component_name:
                    print 'Component %s already exists in' % component.name, component.location.name
                    return component
            newcomponent = self.store.add(Component(unicode(component_name)))
            newcomponent.location = location
            newcomponent.instrument = location.instrument
            print 'Creating New Component', newcomponent.name, 'in location', location.name, 'in instrument', newcomponent.instrument.name
            self.commit()     
            return newcomponent
        return None
    
    def getinstrument(self, instrument_name):
        return self.store.find(Instrument, Instrument.name == unicode(instrument_name)).one()

    def getlocation(self, location_name):
        return self.store.find(Location, Location.name == unicode(location_name)).one()
   
    def getcomponent(self, component_name):
        return self.store.find(Component, Component.name == unicode(component_name)).one()
    
    def getinstruments(self):
        result = self.store.find(Instrument, Instrument.name==unicode('*'))
        result.order_by(Instrument.name)
        return result.count()
    
    def getlocations(self, instrument):
        print self.store.find(Instrument, Instrument.name)
        for i in self.store.find(Instrument, Instrument.name):#.values():
              print 'i', i#.one()
        #print 'n', n
#         locations = list()
#         for loc in Location.name:
#             locations.append(loc)
#         return loc
    
    def getcomponents(self, location):
        pass
         
        #print res.one().count()
#     def get_instruments(store, info_classes=None):
#         print 'here'
#         where = []
#         
#         if info_classes:
#             info_types = [info_class.info_type for info_class in info_classes]
#             where = [Instrument.info_type.is_in(info_types)]
#         result = self.store.find(Instrument, *where)
#         result.order_by(Instrument.name)
#         return result
#                 
if __name__ == '__main__':
    scheme   = 'sqlite'
    user     = 'pcds'
    passwd   = 'pcds2014'
    hostname = 'localhost' # to change
    port     = ''
    dbname   = '/Users/paiser/aaaadb'
    manager = MotorManager(scheme, user, passwd, hostname, port, dbname)
    manager.create_alltables()

    amo = manager.addinstrument('AMO')
    cxi = manager.addinstrument('CXI')
    lamp = manager.addlocation('LAMP', amo)
    sl02 = manager.addcomponent('slits02', lamp)
    #sl02 = manager.addcomponent('slits02', lamp)
    sb2 = manager.addlocation('SB2', cxi)
    sl01 = manager.addcomponent('slits01', sb2)
    print '\nNEED TO FIND INSTRUMENTS, LOCATIONS AND COMPONENTS...\n'
    #print manager.getinstruments()
    
    Instrument.locations = ReferenceSet(Instrument.name, Location.name)
    print amo.locations.count()
    print manager.getlocations(amo)