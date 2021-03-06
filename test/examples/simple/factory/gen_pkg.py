#//----------------------------------------------------------------------
#//   Copyright 2007-2010 Mentor Graphics Corporation
#//   Copyright 2007-2010 Cadence Design Systems, Inc.
#//   Copyright 2010-2011 Synopsys, Inc.
#//   Copyright 2019-2020 Tuomas Poikela (tpoikela)
#//   All Rights Reserved Worldwide
#//
#//   Licensed under the Apache License, Version 2.0 (the
#//   "License"); you may not use this file except in
#//   compliance with the License.  You may obtain a copy of
#//   the License at
#//
#//       http://www.apache.org/licenses/LICENSE-2.0
#//
#//   Unless required by applicable law or agreed to in
#//   writing, software distributed under the License is
#//   distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#//   CONDITIONS OF ANY KIND, either express or implied.  See
#//   the License for the specific language governing
#//   permissions and limitations under the License.
#//----------------------------------------------------------------------

from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
#from uvm import *
from packet_pkg import packet


class gen(UVMComponent):

    def __init__(self, name, parent):
        super().__init__(name, parent)


    def get_packet(self):

        # use the factory to generate a packet
        pkt = packet.type_id.create("p", self)

        # randomize it
        pkt.randomize()  # cast to 'void' removed

        return pkt


#    //Use the macro in a class to implement factory registration along with other
#    //utilities (create, get_type_name). To do only factory registration, use
#    //the macro `uvm_component_utils(gen,"gen").
uvm_component_utils(gen)
