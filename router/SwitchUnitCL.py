#=========================================================================
# SwitchUnitCL.py
#=========================================================================
# Cycle level implementation of a round robin switch unit.
#
# Author : Yanghui Ou
#   Date : May 16, 2019

from pymtl                 import *
from pclib.ifcs.GuardedIfc import (
  GuardedCallerIfc, 
  GuardedCalleeIfc, 
  guarded_ifc 
)

class SwitchUnitCL( Component ):

  def construct( s, PacketType, num_inports=5 ):

    # Constants

    s.num_inports = num_inports

    # Interface

    s.get  = [ GuardedCallerIfc() for _ in range( s.num_inports ) ]
    s.send = GuardedCallerIfc()

    # Components

    s.priority = [ i for i in range( s.num_inports ) ]
    s.msg = None
    
    @s.update
    def up_su_arb_cl():
      if s.send.rdy() and s.any_ready():
        for i in s.priority:
          if s.get[i].rdy():
            s.priority.append( s.priority.pop(i) )
            s.send( s.get[i]() )
            break
    
    for i in range( s.num_inports ):
      s.add_constraints( M( s.get[i] ) < U( up_su_arb_cl ) )
      # s.add_constraints( U( up_su_arb_cl ) < M( s.get[i].rdy ) )
      # s.add_constraints( M( s.get[i] ) < M( s.send ) )

  def any_ready( s ):
    flag = False
    for i in range( s.num_inports ):
      flag = flag or s.get[i].rdy()
    return flag

  # TODO: CL line trace
  def line_trace( s ):
    return "{}{}".format(
      [ s.get[i].rdy() for i in range(3) ],
      s.priority
    )