#!/usr/bin/env python
from storm.locals import *
import sys

class Instrument(object):
    __storm_table__ = "instrument"
    id = Int(primary=True)
    name = Unicode()
   
    def __init__(self, name):
        self.name = name

class Loc(object):
    __storm_table__ = "location"
    #instrument_id = Int(primary=True)
    instrument_name = Unicode(primary=True)
    id = Int()
    #instrument = Reference(instrument_id, Instrument.id)
    instrument = Reference(instrument_name, Instrument.name)
    name = Unicode()
    
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
    id = Int()#primary=True)
    #location_id = Int()    
    location_name = Unicode() 
    #location = Reference(location_id, Location.instrument_id)
    ###location = Reference(location_name, Location.instrument_name)
    location = Reference(location_name, Location.name)
    #component_instrument_id = Int()
    #instrument = Reference(component_instrument_id, Instrument.id)

    
    def __init__(self, name):
        self.name = name
  
class Device(object):
    __storm_table__ = "device"
    id = Int(primary=True)
#     instrument_id = Int()
#     location_id   = Int()
#     component_id  = Int()
    instrument_name = Unicode()
    location_name   = Unicode()
    component_name  = Unicode()    
    name = Unicode()
    alias = Unicode()
    #dtype = Unicode()

class PCDSmotor(Device):
    __storm_table__ = "pcdsmotor"
    id = Int(primary=True)
    brand = Unicode()
    #component_id = Unicode()
    component_name = Unicode()
    location_name = Unicode()
    instrument_name = Unicode()
    #component = Reference(component_id, Component.location_id)
    component = Reference(component_name, Component.location_name)
    location = Reference(location_name, Location.name)
    instrument = Reference(instrument_name, Instrument.name)

    def __init__(self, name, alias, brand=None):
        self.name = name
        self.alias = alias
        self.brand = brand
		
class NewportMotor(PCDSmotor):
    #__storm_table__ = "pcdsmotor"
    __storm_table__ = "newportmotor"    
    #component_id = Int()
    component_name = Unicode()
    location_name = Unicode()
    instrument_name = Unicode()
    #component = Reference(component_id, Component.location_id)
    #component = Reference(component_name, Component.location_name)
    component = Reference(component_name, Component.name)
    location = Reference(location_name, Location.name)
    instrument = Reference(instrument_name, Instrument.name)
    
    def __init__(self, name, alias, brand=u'Newport'):
        self.name = name
        self.alias = alias
        self.brand = brand
        
class IMSMotor(PCDSmotor):
    #__storm_table__ = "pcdsmotor"
    __storm_table__ = "imsmotor"    
    #component_id = Int()
    #component = Reference(component_id, Component.location_id)
    component_name = Unicode()
    location_name = Unicode()
    instrument_name = Unicode()
    #component = Reference(component_name, Component.location_name)
    component = Reference(component_name, Component.name)
    location = Reference(location_name, Location.name)
    instrument = Reference(instrument_name, Instrument.name)
        
    def __init__(self, name, alias, brand=u'IMS'):
        self.name = name
        self.alias = alias
        self.brand = brand

class MotorManager(object):
    def __init__(self, scheme, user, passwd, hostname, port, dbname, parent=None):
        #database = create_database("sqlite:")
        dbpars   = (scheme, user, passwd, hostname, port, dbname)
        database = create_database("%s://%s:%s@%s:%s/%s" % dbpars)        
        self.store = Store(database)
        #Location.imsmotors = ReferenceSet(Component.location_id, IMSMotor.component_id)        
        #Location.newportmotors = ReferenceSet(Component.location_id, NewportMotor.component_id)      
        Location.imsmotors = ReferenceSet(Component.location_name, IMSMotor.component_name)        
        Location.newportmotors = ReferenceSet(Component.location_name, NewportMotor.component_name)             
        # TO BE FIXED:
        #Instrument.locations = ReferenceSet(Loc.instrument_name, Instrument.name)                
        #Location.components  = ReferenceSet(Location.id, Component.id)
        #Component.devices    = Reference(Component.id, PCDSmotor.id)
        
    def create_alltables(self):
        try:
            self.store.execute("CREATE TABLE instrument "
                               "(id INTEGER PRIMARY KEY, name VARCHAR)", noresult=True)

            self.store.execute("CREATE TABLE location "
                               "(id INTEGER PRIMARY KEY, instrument_name VARCHAR, name VARCHAR)", noresult=True)

            self.store.execute("CREATE TABLE component "
                               "(id INTEGER PRIMARY KEY, instrument_name VARCHAR, location_name VARCHAR, name VARCHAR)", noresult=True)

            self.store.execute("CREATE TABLE device "
                               "(id INTEGER PRIMARY KEY, instrument_name VARCHAR, location_name VARCHAR, component_name VARCHAR, name VARCHAR, alias VARCHAR)", noresult=True)

            self.store.execute("CREATE TABLE pcdsmotor "
                               "(id INTEGER PRIMARY KEY, instrument_name VARCHAR, location_name VARCHAR, component_name VARCHAR, name VARCHAR, brand VARCHAR)", noresult=True)
                                       
            self.store.execute("CREATE TABLE newportmotor "
                               "(id INTEGER PRIMARY KEY, instrument_name VARCHAR, location_name VARCHAR, component_name VARCHAR, name VARCHAR, alias VARCHAR, brand VARCHAR)", noresult=True)
            
            self.store.execute("CREATE TABLE imsmotor "
                               "(id INTEGER PRIMARY KEY, instrument_name VARCHAR, location_name VARCHAR, component_name VARCHAR, name VARCHAR, alias VARCHAR, brand VARCHAR)", noresult=True)
 


#             self.store.execute("CREATE TABLE location "
#                                "(id INTEGER PRIMARY KEY, instrument_id INTEGER, name VARCHAR)", noresult=True)
# 
#             self.store.execute("CREATE TABLE component "
#                                "(id INTEGER PRIMARY KEY, instrument_id INTEGER, location_id INTEGER, name VARCHAR)", noresult=True)
# 
#             self.store.execute("CREATE TABLE device "
#                                "(id INTEGER PRIMARY KEY, instrument_id INTEGER, location_id INTEGER, component_id INTEGER, name VARCHAR, alias VARCHAR)", noresult=True)
# 
#             self.store.execute("CREATE TABLE pcdsmotor "
#                                "(id INTEGER PRIMARY KEY, instrument_id INTEGER, location_id INTEGER, component_id INTEGER, name VARCHAR, brand VARCHAR)", noresult=True)
#                                        
#             self.store.execute("CREATE TABLE newportmotor "
#                                "(id INTEGER PRIMARY KEY, instrument_id INTEGER, location_id INTEGER, component_id INTEGER, name VARCHAR, alias VARCHAR, brand VARCHAR)", noresult=True)
#             
#             self.store.execute("CREATE TABLE imsmotor "
#                                "(id INTEGER PRIMARY KEY, instrument_id INTEGER, location_id INTEGER, component_id INTEGER, name VARCHAR, alias VARCHAR, brand VARCHAR)", noresult=True)
#          
        
        
        
        
        
        
        
        
        
        
            """
            self.store.execute("CREATE TABLE instrument "
                               "(id INTEGER PRIMARY KEY, name VARCHAR)", noresult=True)

            self.store.execute("CREATE TABLE location "
                               "(id INTEGER PRIMARY KEY, name VARCHAR, instrument_id INTEGER)", noresult=True)

            self.store.execute("CREATE TABLE component "
                               #"(id INTEGER PRIMARY KEY, name VARCHAR, location_id INTEGER)", noresult=True)
                               "(id INTEGER PRIMARY KEY, name VARCHAR, location_id INTEGER, instrument_id INTEGER, component_instrument_id INTEGER)", noresult=True)

            self.store.execute("CREATE TABLE genericmotor "
                               "(id INTEGER PRIMARY KEY, name VARCHAR, component_id INTEGER)", noresult=True)

            self.store.execute("CREATE TABLE newportmotor "
                               "(id INTEGER PRIMARY KEY, name VARCHAR, component_id INTEGER)", noresult=True)
                               
            self.store.execute("CREATE TABLE imsmotor "
                               "(id INTEGER PRIMARY KEY, name VARCHAR, component_id INTEGER)", noresult=True)
            """
        except:
            pass
            
    def commit(self):
        self.store.commit()

    def roolback(self):
        self.store.rollback()

    def addinstrument(self, instrument):    	
        newinstrument = Instrument(unicode(instrument))
        print 'Creating New Instrument', newinstrument.name
        return newinstrument

    def addlocation(self, location, instrument):
        newlocation = Location(unicode(location))
        newlocation.instrument = instrument
        print 'Creating New Location', newlocation.name, 'in instrument', instrument.name
        return newlocation

    def addcomponent(self, component, location=None):
    	newcomponent = self.store.add(Component(unicode(component)))
    	newcomponent.location = location
        newcomponent.instrument = location.instrument
        print 'Creating New Component', newcomponent.name, 'in location', location.name, 'in instrument', newcomponent.instrument.name        
    	return newcomponent

    def addimsmotor(self, motor, alias=None, component=None):
        newmotor = self.store.add(IMSMotor(unicode(motor), unicode(alias)))
        newmotor.component  = component
        newmotor.location   = component.location
        newmotor.instrument = component.instrument
        #newmotor.brand = u'ims'        
        print 'Creating New IMS motor', newmotor.name, 'with alias', newmotor.alias, 'in  component', newmotor.component.name, 'in location', newmotor.location.name, 'in instrument', newmotor.instrument.name       
        return newmotor

    def addnewmportmotor(self, motor, alias=None, component=None):
        newmotor = self.store.add(NewportMotor(unicode(motor), unicode(alias)))
        newmotor.component  = component
        newmotor.location   = component.location
        newmotor.instrument = component.instrument
        #newmotor.brand = u'newport'
        print 'Creating New Newport motor', newmotor.name, 'with alias', newmotor.alias, 'in  component', newmotor.component.name, 'in location', newmotor.location.name, 'in instrument', newmotor.instrument.name       
        return newmotor
    
    
    def getComponents(self, location):
        print 'looking for', location.name
        #return self.store.find(Component, name=unicode(location.name))#.one()
        return location.name.find(unicode(location.name+'dd'))#name=unicode(location.name)).one()        
            
