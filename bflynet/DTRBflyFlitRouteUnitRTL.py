#=========================================================================
# DTRBflyFlitRouteUnitRTL.py
#=========================================================================
# A butterfly route unit supporting flit.
#
# Author : Cheng Tan
#   Date : July 14, 2019

from pymtl3             import *
from pymtl3.stdlib.ifcs import GetIfcRTL, GiveIfcRTL
from copy import deepcopy

class DTRBflyFlitRouteUnitRTL( Component ):

  def construct( s, MsgType, PositionType, num_outports, n_fly = 3 ):

    # Constants 

    s.num_outports = num_outports
    k_ary    = num_outports
    OutType  = mk_bits( clog2( s.num_outports ) )
    rows     = k_ary ** ( n_fly - 1 )
    EnType  = mk_bits( s.num_outports )
    DstType = mk_bits( clog2(k_ary) * n_fly )
    if rows == 1:
      RowWidth = 1
    else:
      RowWidth = clog2( k_ary )
    END = n_fly * RowWidth
    BEGIN = END - RowWidth

    # Interface

    s.get  = GetIfcRTL( MsgType )
    s.give = [ GiveIfcRTL(MsgType ) for _ in range ( s.num_outports ) ]
    s.pos  = InPort( PositionType )

    # Componets

    s.out_dir  = Wire( OutType )
    s.give_rdy = [ Wire( Bits1 ) for _ in range( s.num_outports ) ]
    s.give_ens = Wire( mk_bits( s.num_outports ) ) 

    # Connections

    for i in range( s.num_outports ):
#      s.connect( s.get.msg,     s.give[i].msg )
      s.connect( s.give_ens[i], s.give[i].en  )
      s.connect( s.give_rdy[i], s.give[i].rdy )
    
    # Routing logic
    @s.update
    def up_ru_routing():
#      s.out_dir = OutType( 0 )
      for i in range( s.num_outports ):
        s.give_rdy[i] = Bits1( 0 )

      if s.get.rdy:
        s.out_dir = s.get.msg.dst[ BEGIN : END]
        s.give_rdy[ s.out_dir ] = Bits1( 1 )
        
    @s.update
    def up_ru_get_en():
      s.get.en = s.give_ens>EnType(0)
      for i in range( s.num_outports ):
        s.give[i].msg = deepcopy( s.get.msg )
      if s.get.rdy:
        s.give[ s.out_dir ].msg.dst = DstType(s.get.msg.dst << RowWidth)

  # Line trace
  def line_trace( s ):
    out_str = [ "" for _ in range( s.num_outports ) ]
    for i in range (s.num_outports):
      out_str[i] = "{}".format( s.give[i] ) 

    return "{}({}){}".format( s.get, s.out_dir, "|".join( out_str ) )