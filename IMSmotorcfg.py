from storm.locals import *
import datetime

class IMSMotorCfg(Storm):
    __storm_table__ = "imsmotorcfg"
    id = Int(primary=True)
    component_name = Unicode()
    name = Unicode()
    description = Unicode()
    signature = Unicode()
    date = DateTime()
    """ references """
    ims_motor = Reference(component_name, "IMSMotor.component_name")
    parameters = ReferenceSet(id, "CfgParameter.cfg_id")
    
    def __init__(self, name, description = None):
        if description == None:
            description = unicode("")
        self.description = unicode(description)
        self.name = unicode(name)
        self.date = datetime.datetime.now()
        self.initialize()
    
    def __storm_loaded__(self):
        self.initialize()
        for cfgpar in self.parameters:
            self._inmemory_parameters[cfgpar.name] = cfgpar
        
    def initialize(self):
        self._inmemory_parameters = {}
        
    def setMotor(self, motor):
        self.ims_motor = motor
    
    def resetMotor(self):
        self.ims_motor = None
        self.component_name = None
        
    def setSignature(self, signature):
        self.signature = unicode(signature)
    
    def getSignature(self):
        return str(self.signature)
    
    def setParameter(self, name, value):
        name = unicode(name)
        value = unicode(value)        
        cfgpar = None
        try:
            cfgpar = self.parameters.find(CfgParameter.name == name).one()
        except:
            pass
        if cfgpar is None:
            cfgpar = CfgParameter(self, name, value)
            self.parameters.add(cfgpar)
        else:            
            cfgpar.value = value        
        self._inmemory_parameters[unicode(name)] = cfgpar
    
    def getParameter(self, name, in_memory = False):
        if in_memory:
            if self._inmemory_parameters.has_key(unicode(name)):                
                return self._inmemory_parameters[unicode(name)].value
            else:
                return None
        else:
            cfgpar = self.parameters.find(CfgParameter.name == name).one()
            if not cfgpar is None:
                return cfgpar.value
            else:
                return None
    
    def toList(self):
        list = []
        for cfgpar in self._inmemory_parameters.values():
            list.append((cfgpar.name, cfgpar.value))
        return list
    
    def __str__(self):
        text = "Configuration"
        for par in self.parameters:
             text = text + "\n" + par.name +":\t" + par.value
        return text
        
    
    def __cmp__(self, other):
        other_list = other.toList()
        self_list = self.toList()
            
        for name, value in self_list:
            other_value = other.getParameter(name, True)
            #if name == 'IMSNAME' or name == 'VER':
            #    pass
            #elif not other_value is None:
            if not other_value is None:
                if value != other_value:
                    return -1
            else:
                return -1

        return 0
        
class CfgParameter(Storm):
    __storm_table__ = "cfgparameter"
    __storm_primary__ = ("name", "cfg_id")
    cfg_id = Int()
    name = Unicode()
    value = Unicode()
    """ references """
    motor_cfg = Reference(cfg_id, "IMSMotorCfg.id")    
    def __init__(self, cfg, name, value):
        self.motor_cfg = cfg
        self.name = unicode(name)
        self.value = unicode(value)

        
        
