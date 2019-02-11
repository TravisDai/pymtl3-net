from pymtl import *
from pclib.ifcs import InValRdyBundle, OutValRdyBundle
from pclib.rtl import Mux, RoundRobinArbiterEn
from pc import Encoder

class SwitchUnit( Model ):
  """
<<<<<<< HEAD
  A switch unit implementing round-robin arbitration.
=======
  A simple switch unit that supports single-phit packet.
>>>>>>> f40235250d98261530ec50fadf15439e28c43d3b
  """
  def __init__( s, msg_type, num_inports ):

<<<<<<< HEAD
    # Constants 
    s.num_inports = 5
    NORTH = 0
    SOUTH = 1
    WEST  = 2
    EAST  = 3
    SELF  = 4
=======
    # Constants
    s.num_inports = num_inports
    s.sel_width   = clog2( num_inports )
>>>>>>> f40235250d98261530ec50fadf15439e28c43d3b

    # Interface
    s.in_ =  InValRdyBundle[ s.num_inports ]( msg_type )
    s.out = OutValRdyBundle( msg_type )

<<<<<<< HEAD
    # Componets
#    s.in_rdys = Wire( s.num_outports )
    s.count_arbitor = Wire( Bits(8) ) # arbitrating in round-robin (increment in every tick)

    # Connections
#    for i in range( s.num_outports ):
#      s.connect( s.in_[i].msg,       s.out[i].msg )
#      s.connect( s.in_rdys[i],   s.in_[i].rdy )
    
    @s.combinational
    def assignInRdy():
      s.in_[s.count_arbitor].rdy.value = Bits(8, 0)

    # Switch logic
    @s.tick
    def switchLogic():
      s.out.val.next = s.in_[s.count_arbitor].val
      if s.reset:
        s.count_arbitor.next = 0
      else:
        if s.count_arbitor == SELF:
          s.count_arbitor.next = 0
        else:
          s.count_arbitor.next = s.count_arbitor + 1

=======
    # Components
    s.arbiter = RoundRobinArbiterEn( num_inports )
    s.encoder = Encoder( num_inports, sel_width )
    s.mux_msg = Mux( msg_type, num_inports )
    s.mux_val = Mux( 1,        num_inports )

    # Connections
    s.connect( s.arbiter.grants, s.encoder.in_ )
    s.connect( s.encoder.out,    s.mux_msg.sel )
    s.connect( s.encoder.out,    s.mux_val.sel )
    s.connect( s.mux_val.out,    s.out.val     )
    s.connect( s.mux_msg.out,    s.out.msg     )

    for i in range( num_inports ):
      s.connect( s.in_[i].msg, s.mux_msg.in_[i] )
      s.connect( s.in_[i].val, s.mux_val.in_[i] )

    @s.combinational
    def inRdy():
      for i in range( num_inports ):
        s.in_[i].rdy.value = s.arbiter.grants[i] and s.out.rdy
>>>>>>> f40235250d98261530ec50fadf15439e28c43d3b

  # TODO: implement line trace
  def line_trace( s ):
<<<<<<< HEAD
    return "{} {}".format( s.count_arbitor, s.out.val)
=======
    return ""
>>>>>>> f40235250d98261530ec50fadf15439e28c43d3b
