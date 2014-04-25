#!/usr/bin/env python
import sys
from storm_motor import *

if __name__ == '__main__':
    scheme   = 'sqlite'
    user     = 'pcds'
    passwd   = 'pcds2014'
    hostname = 'localhost' # to change
    port     = ''
    dbname   = 'motordb'
    manager = MotorManager(scheme, user, passwd, hostname, port, dbname)
    manager.create_alltables()

    amo = manager.addinstrument('AMO')
    sxr = manager.addinstrument('SXR')
    xpp = manager.addinstrument('XPP')
    xcs = manager.addinstrument('XCS')
    cxi = manager.addinstrument('CXI')
    mec = manager.addinstrument('MEC')

    sb2  = manager.addlocation('SB2' , cxi)
    lamp = manager.addlocation('LAMP', amo)
    sl01 = manager.addcomponent('slits01', sb2)
    ##sl03 = manager.addcomponent('slits03', sb2)    
    sl02 = manager.addcomponent('slits02', lamp)
    slr = manager.addimsmotor('IOC:TST:MMS:01', 'slits_right', sl01)
    sll = manager.addnewmportmotor('IOC:TST:NMS:01', 'slits_left', sl01)
    sld = manager.addimsmotor('IOC:TST:MMS:02', 'slits_down', sl01)    
    slu = manager.addimsmotor('IOC:TST:MMS:03', 'slits_up', sl02)
    ##slc = manager.addimsmotor('IOC:TST:MMS:04', 'slits_caca', sl03)
    
    print 'Before commit ----------------------------'
    #for m in [slr, sll, slu, sld, slc]:    
    for m in [slr, sll, slu, sld]:
       id = m.id; name = m.name; alias = m.alias; comp = m.component.name;
       loc = m.location.name; instr = m.instrument.name
       print '%r, %r, %-15r, %r, %-7r, %r' % (id, name, alias, comp, loc, instr)
            
    manager.commit()

    print 'After commit -----------------------------'
    print slr.id
    print slr.name
    print slr.alias
    print slr.component#.name
    print slr.location.name
    print slr.instrument.name
    
    
    #for m in [slr, sll, slu, sld, slc]:
    for m in [slr, sll, slu, sld]:
       id = m.id; name = m.name; alias = m.alias; comp = m.component.name;
       loc = m.location.name; instr = m.instrument.name
       print '%04d, %r, %-15r, %r, %-7r, %r' % (id, name, alias, comp, loc, instr)
       
    print '--------------------------------'
    
    print 'Q. Whose components belong to which locations and instruments?'
    print 'A.'
    for c in [sl01, sl02]:
        print '%r, %r belongs to location %r that belongs to instrumet %r' % \
        (c.id, str(c.name), str(c.location.name), str(c.instrument.name))               
    for l in [sb2, lamp]:
        print '%r, %r belongs to instrument %r' % (l.id, str(l.name), str(l.instrument.name))
    print '--------------------------------'
    print 'Q. How many components are in the location %s?' % sb2.name
    print 'A.'
    print manager.getComponents(sb2)
    #print manager.store.count()
    
    """
    print cxi.locations.count()
    print sb2.components.count()
    print lamp.components.count()
    print sl01.devices.count()
    print sl02.devices.count()
    
    print sl03.devices        
    print '%s: %d' % (slr.name, slr.count())
    print '%s: %d' % (sl01.name, sl01.count())
    
    print 'Motors count -----------------------------'
    print 'Number of IMS motors in %s: %d' % (sl01.name, sl01.imsmotors.count())
    print 'Number of NEWPORT motors in %s: %d' % (sl01.name, sl01.newportmotors.count())

    """
