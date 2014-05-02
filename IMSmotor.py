from storm.locals import *
from conflict import *
#from icepapdrivercfg import IcepapDriverCfg
#from conflict import Conflict
#from configmanager import ConfigManager
#from icepapcontroller import IcepapController
#from stormmanager import StormManager
#import os
#import time
#from datetime import datetime
#import socket
#from pyIcePAP import IcepapMode


class IMSMotor(Storm):
    __storm_table__ = "imsmotor"
    __storm_primary__ = ("component_name")
    component_name = Unicode()
    name = Unicode()
    
    """ references """
    component = Reference(component_name, "Component.name")
    historic_cfgs = ReferenceSet((component_name, name), ("IMSMotorCfg.component_name", "IMSMotorCfg.motor_name"))
    #historic_cfgs = ReferenceSet((icepapsystem_name, addr), ("IcepapDriverCfg.icepapsystem_name", "IcepapDriverCfg.driver_addr"))
    
    def __init__(self, motor_name, component_name):
        self.motor_name = unicode(motor_name)
        self.component_name = unicode(component_name)
        print 'init', self.motor_name, self.component_name        
        self.current_cfg = None
        self.initialize()
            
    def __storm_loaded__(self):
        self.current_cfg = self.historic_cfgs.order_by("date").last()       
        self.initialize()
    
    def initialize(self):
        self._undo_list = []
        self.startup_cfg = self.current_cfg
        self.conflict = Conflict.NO_CONFLICT
        
    def addConfiguration(self, cfg, current = True):
        if current:
            if not self.current_cfg is None:
                self._undo_list.append(self.current_cfg)
            else:
                self.startup_cfg = cfg
            self.current_cfg = cfg
            cfg.setMotor(self)
        self.historic_cfgs.add(cfg)

    def setConflict(self, conflict):
        self.conflict = conflict
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = unicode(name)
    
    def signDriver(self):
        # THE COMMIT SHOULD BE DONE IN THE DATABASE FIRST, AND IF NO ERRORS, 
        # THEN COMMUNICATE THE MOTOR THAT THE VALUES SHOULD BE SIGNED.
        try:
            user = ConfigManager().username
            host = socket.gethostname()
            # HERE NEED TO CHECK HOWTO: -----------------
            signature = user+"@"+host+"_"+datetime.now().strftime('%Y/%m/%d_%H:%M:%S')
            IcepapController().signDriverConfiguration(self.component_name, signature)
            db = StormManager()
            db.commitTransaction()
            # -------------------------------------------
            self.current_cfg.name = unicode(time.ctime())
            self.current_cfg.setSignature(signature)        
            self.startup_cfg = self.current_cfg
            self.conflict = Conflict.NO_CONFLICT
        except Exception,e:
            print "Some exception while trying to sign the driver", e

    
    def setStartupCfg(self):
        self.current_cfg = self.startup_cfg
        self.conflict = Conflict.NO_CONFLICT
    
    def undo(self, config):
        self.addConfiguration(config)
        # THE CURRENT CONFIGURATION SHOULD NOT BE IN THE UNDO LIST
        return self._undo_list.pop()
        
    def getUndoList(self):
        return self._undo_list.pop()
    
    def hasUndoList(self):
        return len(self._undo_list) > 0
    
    def saveHistoricCfg(self, now, name, desc):
        self.current_cfg.name = unicode(name)
        self.current_cfg.description = unicode(desc)
    
    def deleteHistoricCfg(self, cfg):
        self.historic_cfgs.remove(cfg)

    def __cmp__(self, other):
        if self.current_cfg == other.current_cfg:
            self.setConflict(Conflict.NO_CONFLICT)
            return 0
        self.setConflict(Conflict.MOTOR_CHANGED)
        return -1
     
    # SORT THE IMS MOTORS IN THE TREE
    def __lt__(self,other):
        if isinstance(other, IMSMotor):
            return self.addr < other.addr
