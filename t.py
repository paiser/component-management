#!/usr/bin/env python
from storm.locals import *
import sys

class Instrument(object):
    __storm_table__ = "instrument"
    id = Int(allow_none=False)
    name = Unicode(allow_none=False, primary=True)
   
    def __init__(self, name):
        self.name = name
        
class Loc(object):
    __storm_table__ = "location"
    #instrument_id = Int(primary=True)
    instrument_name = Unicode(allow_none=False, primary=True)
    id = Int(allow_none=False)
    #instrument = Reference(instrument_id, Instrument.id)
    instrument = Reference(instrument_name, Instrument.name)
    name = Unicode(allow_none=False)
    
class Location(Loc):
    def __init__(self, name):
        self.name = name
        self.initialize()
    
    def initialize(self):
        self._inmemory_locations = {}
                
    def __storm_loaded__(self):
        print 'storm_loaded'
        self.initialize()
        #for location in self.locations:
        self._inmemory_locations[self.name] = self.name

class Component(Location):
    __storm_table__ = "component"
    id = Int(allow_none=False)#primary=True)
    #location_id = Int()    
    location_name = Unicode(allow_none=False) 
    #location = Reference(location_id, Location.instrument_id)
    ###location = Reference(location_name, Location.instrument_name)
    location = Reference(location_name, Location.name)
    #component_instrument_id = Int()
    #instrument = Reference(component_instrument_id, Instrument.id)

    
    def __init__(self, name):
        self.name = name
        
class MotorManager(object):
    def __init__(self, scheme, user, passwd, hostname, port, dbname, parent=None):
        #database = create_database("sqlite:")
        dbpars   = (scheme, user, passwd, hostname, port, dbname)
        database = create_database("%s://%s:%s@%s:%s/%s" % dbpars)        
        self.store = Store(database)
        self.instruments = list()
        self.location = None
        self.component = None
        
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
        print 'commit'
        self.store.commit()

    def roolback(self):
        self.store.rollback()
        
    def addinstrument(self, instrument): 
        # NEED TO CHECK IF INSTRUMENT ALREADY EXISTS:
        ##result = manager.store.find(Instrument)
        result = self.store.find(Instrument, Instrument.name.is_in([unicode(instrument)]))
        if result.count():
            print 'Instrument %s Exists' % instrument
            print 'SHOULD RETURN THE REQUESTED EXISTING INSTRUMENT'
            return None# Instrument.instrument
        #result.order_by(Instrument.name)
        ##print 'result', result.count()
        ##print 'result.names', list(result.values(Instrument.name))
        ##for i in result:
        ##    print 'i',i.name



        newinstrument = Instrument(unicode(instrument))
#         try:
#             print self.instrument.name.count(newinstrument.name)#find(unicode(instrument))
#         except:
#             pass               
        #newinstrument = Instrument(unicode(instrument))
        print 'Creating New Instrument', newinstrument.name
        #print self.store.find(Instrument, newinstrument.name).order_by(newinstrument.name).one()
        
        self.commit()
        #self.instrument = newinstrument
        return newinstrument

    def addlocation(self, location, instrument):
        #try:
        newlocation = Location(unicode(location))
        newlocation.instrument = instrument
        #except:
        #    pass
        print 'Creating New Location', newlocation.name, 'in instrument', instrument.name
        #self.inmemory_locations[instrument.name] = newlocation.name
        #self.locations.append(newlocation.name)
        self.commit()
        return newlocation

    def addcomponent(self, component, location=None):
        newcomponent = self.store.add(Component(unicode(component)))
        newcomponent.location = location
        print 'lll', location.instrument.name
        #print self.store.find(Instrument, Instrument.name.is_in([unicode(location.instrument.name)]))#.order_by('instrument_name').one()
        #print self.store.find(Component)#, newcomponent.name == unicode(newcomponent.instrument.name))
        
        print 'kiki'
        #print newcomponent.instrument.find(newcomponent.instrument.name)
            #print 'ERROR: Instrument Exist!'

        #print location.find(unicode(location))
#             print 'ERROR: Location Exist!'
#             return None
        #print newcomponent.name.find(newcomponent.name)
#             print 'ERROR: Component Exist!'
            #return None        
        
        
        newcomponent.instrument = location.instrument
        print 'Creating New Component', newcomponent.name, 'in location', location.name, 'in instrument', newcomponent.instrument.name
        #print self.store.find(Instrument, newcomponent.instrument.name).order_by(newcomponent.instrument.name).one()
        #print self.store.find(Component, 'instrument_name').order_by('instrument_name').one()
#         print [type(component.name) for component in self.store.find(Instrument).order_by(Instrument.name)]
#         print 'here'
#         instr = self.get_instruments(self.store)#, info_classes=[Instrument]).one()
#         print instr.name
        self.commit()     
        return newcomponent
    
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
    #amo  = manager.addinstrument('AMO')
    #print amo.name.find(unicode('AMO'))
#             print 'ERROR: Location Exist!'
#             return None
        
    #amo  = manager.addinstrument('AMO')
    lamp = manager.addlocation('LAMP', amo)
    #print lamp.name.find(unicode('LAMP'))
    sl02 = manager.addcomponent('slits02', lamp)
    sb2 = manager.addlocation('SB2', cxi)
    sl01 = manager.addcomponent('slits01', sb2)