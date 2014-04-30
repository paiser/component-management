#!/usr/bin/env python
from storm.locals import *
from IMSmotorcfg import *
from IMSmotor import *
import sys

class Instrument(object):
    __storm_table__ = "instrument"
    id = Int(primary=True)
    name = Unicode()
    #locations = Unicode()
    def __init__(self, name):
        self.name = name
        
class Loc(object):
    __storm_table__ = "location"
    #instrument_id = Int(primary=True)
    id = Int(primary=True)
    instrument_id = Int()
    instrument = Reference(instrument_id, Instrument.id)
    name = Unicode()
    ###components = Unicode()
    #locations = Reference(Instrument.locations, name)
    
class Location(Loc):
    def __init__(self, name):
        self.name = name
        #self.initialize()

class Component(Location):
    __storm_table__ = "component"
    id = Int(primary=True) 
    location_id = Int()  
    location = Reference(location_id, Location.id)
    
    def __init__(self, name):
        self.name = name
 
class Device(Component):
    __storm_table__ = "device"
    id = Int(primary=True) 
    component_id = Int()  
    component = Reference(component_id, Component.id)
    
    def __init__(self, name):
        self.name = name    
            
class MotorManager(object):
    def __init__(self, scheme, user, passwd, hostname, port, dbname, parent=None):
        dbpars   = (scheme, user, passwd, hostname, port, dbname)
        database = create_database("%s://%s:%s@%s:%s/%s" % dbpars)        
        self.store = Store(database)
        
    def create_alltables(self):
        try:
            self.store.execute("CREATE TABLE instrument "
                               "(id INTEGER  PRIMARY KEY, name VARCHAR)", noresult=True)
            
            self.store.execute("CREATE TABLE location "
                               "(id INTEGER PRIMARY KEY, instrument_id INTEGER, name VARCHAR)", noresult=True)

            self.store.execute("CREATE TABLE component "
                               "(id INTEGER PRIMARY KEY, instrument_id INTEGER, location_id INTEGER, name VARCHAR)", noresult=True)            
            
            self.store.execute("CREATE TABLE device "
                               "(id INTEGER PRIMARY KEY, instrument_id INTEGER, location_id INTEGER, component_id INTEGER, name VARCHAR)", noresult=True)            

            self.store.execute("CREATE TABLE cfgparameter "
                               "(name VARCHAR(20) NOT NULL DEFAULT '', cfg_id INTEGER(10) NOT NULL DEFAULT '0',value VARCHAR(45) NOT NULL DEFAULT '', PRIMARY KEY (name, cfg_id))", noresult=True)

            self.store.execute("CREATE TABLE cfgparameterinfo "
                               "(name VARCHAR(20) NOT NULL DEFAULT '', info VARCHAR(255) NOT NULL DEFAULT '', PRIMARY KEY (name))", noresult=True)                
            
            self.store.execute("CREATE TABLE imsmotorcfg "
                               "(id INTEGER PRIMARY KEY NOT NULL, component_name VARCHAR(25), motor_name INTEGER(10), name VARCHAR(40) NOT NULL DEFAULT '', description VARCHAR(255), signature VARCHAR(40), date datetime NOT NULL DEFAULT '')", noresult=True)
            
            self.store.execute("CREATE TABLE imsmotor "
                               "(component_name VARCHAR(25) NOT NULL DEFAULT '', name VARCHAR(25) NOT NULL DEFAULT '', alias VARCHAR(30), PRIMARY KEY (component_name, name))", noresult=True)
        
        except:
            pass
        
        # References:
        Instrument.locations = ReferenceSet(Instrument.id, Location.instrument_id)
        Location.components  = ReferenceSet(Location.id, Component.location_id)   
             
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
        newinstrument = self.store.add(Instrument(unicode(instrument_name)))
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
            newlocation = self.store.add(Location(unicode(location_name)))
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
    
    def adddevice(self, device_name=None, component=None):
        if component:
            device = self.getdevice(device_name)
            if device:
                if device.name == device_name:
                    print 'Device %s already exists in' % device.name, device.component.name
                    return device
            newdevice = self.store.add(Device(unicode(device_name)))
            newdevice.component = component
            newdevice.location = component.location
            newdevice.instrument = component.instrument            
            print 'Creating New Device', newdevice.name, 'in component', component.name, 'in location', component.location.name, 'in instrument', newdevice.instrument.name
            self.commit()     
            return newdevice
        return None
    
    def getinstrument(self, instrument_name):
        return self.store.find(Instrument, Instrument.name == unicode(instrument_name)).one()

    def getlocation(self, location_name):
        return self.store.find(Location, Location.name == unicode(location_name)).one()
   
    def getcomponent(self, component_name):
        return self.store.find(Component, Component.name == unicode(component_name)).one()

    def getdevice(self, device_name):
        return self.store.find(Device, Device.name == unicode(device_name)).one()
    
    def getinstruments(self):
        result = self.store.find(Instrument, Instrument.name==unicode('*'))
        result.order_by(Instrument.name)
        return result.count()
    
    def getlocations(self, instrument):
        locations = list()
        for location in instrument.locations:
            locations.append(str(location.name))
        return locations
    
    def getcomponents(self, location):
        components = list()
        for component in location.components:
            components.append(str(component.name))
        return components
         
    def delinstrument(self, instrument):
        self.store.remove(instrument)
        del instrument
        self.commit()
    
    def dellocation(self, location):
        self.store.remove(location)
        del location
        self.commit() 
    
    def delcomponent(self, component):
        self.store.remove(component)
        del component
        self.commit()
        
    def deldevice(self, device):
        self.store.remove(device)
        del device
        self.commit() 

    def addIMSconfiguration(self, motor, config=None):         
        if config:
            newconfig = self.store.add(IMSMotorCfg(motor.name))
            print 'Creating New Configuration', newconfig.name
            self.commit()
            return newconfig
        return None
    
    def addIMSmotor(self, motor, component=None):         
        if component:
            newimsmotor = self.store.add(IMSMotor(motor.name, component.name))
            print 'Creating New IMSmotor', newimsmotor.name
            self.commit()
            return newimsmotor
        return None    
             
if __name__ == '__main__':
    import platform
    scheme   = 'sqlite'
    user     = 'pcds'
    passwd   = 'pcds2014'
    hostname = 'localhost' # to change
    port     = ''
    mypc     = platform.system()
    if mypc == 'Linux':
        dbdirectory = '/reg/neh/home1/paiser'
    elif mypc == 'Osx':
        dbdirectory = '/Users/paiser'
    else:
        dbdirectory = '/Users/paiser'
    dbname   = '%s/aaaadb' % dbdirectory
    manager = MotorManager(scheme, user, passwd, hostname, port, dbname)
    manager.create_alltables()

    amo = manager.addinstrument('AMO')
    cxi = manager.addinstrument('CXI')
    lamp = manager.addlocation('LAMP', amo)
    #lamp1 = manager.addlocation('LAMP1', amo)
    
    #sl02 = manager.addcomponent('slits02', lamp)
    sb2 = manager.addlocation('SB2', cxi)
    sb3 = manager.addlocation('SB3', cxi)
    
    sl00 = manager.addcomponent('slits00', lamp)
    sl01 = manager.addcomponent('slits01', sb2)
    sl02 = manager.addcomponent('slits02', sb2)
    sl03 = manager.addcomponent('slits03', sb3)
    sl04 = manager.addcomponent('slits04', sb3)
    sl05 = manager.addcomponent('slits05', sb3)
    
    print '\nTHIS IS OK'
    print 'sb2.components.count()', sb2.components.count()
    print 'sb3.components.count()', sb3.components.count()
    print '\nTHIS IS OK'
    print 'amo.locations.count()', amo.locations.count()
    print 'cxi.locations.count()', cxi.locations.count()
    print '\nTHIS IS OK'
    print manager.getlocations(amo)
    print manager.getlocations(cxi)
    print '\nTHIS IS OK'
    print manager.getcomponents(sb2)
    print manager.getcomponents(sb3)
    print manager.getcomponents(lamp)
    print'\nDEL COMPONENT, LOCATION, INSTRUMENT'
    print manager.getcomponents(sb3)
    print 'Deleting', sl05.name
    manager.delcomponent(sl05)
    print manager.getcomponents(sb3)
    print 'Adding Motors to Components'
    mot00 = manager.adddevice('AMO:TST:MMS:01', sl00)
    mot01 = manager.adddevice('CXI:TST:MMS:01', sl03)
    mot02 = manager.adddevice('CXI:TST:MMS:02', sl01)
    mot03 = manager.adddevice('CXI:TST:MMS:03', sl03)
    print 'mot00', mot00.name, 'added'
    print 'mot01', mot01.name, 'added'
    print 'mot02', mot02.name, 'added'
    print 'mot03', mot03.name, 'added'
    print 'ONGOING: Now the configuration setup and storage...'
    config = ('t0=0','t1=1')
    cfg01 = manager.addIMSconfiguration(mot01, config)
    print 'cfg01', cfg01
    print sl01.name
    #m01 = manager.addIMSmotor(mot01, sl01)
    #m02 = manager.addIMSmotor(mot02, sl02)
    #print 'm01', m01
    