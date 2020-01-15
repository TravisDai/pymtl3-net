'''
==========================================================================
run_test.py
==========================================================================
Driver scripts that runs different kind of tests.

Author : Yanghui Ou
  Date : Jan 14, 2020
'''
import argparse
import sys
import os
from pymtl3 import *

# Hacky way to add the project root directory to path
sys.path.insert( 0, os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
print( os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) ) )

from crt_utils import run_crt

#-------------------------------------------------------------------------
# add_generic_args
#-------------------------------------------------------------------------
# TODO: write help

def add_generic_args( p ):
  p.add_argument( '-v', '--verbose', action='store_true' )
  p.add_argument(       '--max-nterminals', type=int, default=8, metavar='' )
  p.add_argument(       '--max-ntrans', type=int, default=20, metavar='' )
  p.add_argument(       '--translate', choices=['', 'sverilog', 'yosys'], default='' )

#=========================================================================
# multi-level command line parser
#=========================================================================

class Driver:

  def __init__( self ):
    parser = argparse.ArgumentParser( description='driver script' )
    parser.add_argument( 'method', choices=['crt', 'idt', 'pyh2'] )
    self.parser = parser

    args = parser.parse_args( sys.argv[1:2] )
    getattr( self, args.method )()

  #-----------------------------------------------------------------------
  # crt
  #-----------------------------------------------------------------------

  def crt( self ):
    p = argparse.ArgumentParser( description='complete random test' )
    add_generic_args( p )
    p.add_argument( '--max-examples', type=int, default=100, metavar='' )

    opts = p.parse_args( sys.argv[2:] )
    rpt = run_crt( opts )

    print( '-'*74 )
    print( 'Report' )
    print( '#>'+'-'*72 )
    print( rpt         )
    print( '#<'+'-'*72 )

#=========================================================================
# main
#=========================================================================

if __name__ == '__main__':
  Driver()
