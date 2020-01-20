#
#------------------------------------------------------------------------------
#   Copyright 2007-2011 Mentor Graphics Corporation
#   Copyright 2007-2010 Cadence Design Systems, Inc.
#   Copyright 2010 Synopsys, Inc.
#   Copyright 2019 Tuomas Poikela (tpoikela)
#   All Rights Reserved Worldwide
#
#   Licensed under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in
#   compliance with the License.  You may obtain a copy of
#   the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in
#   writing, software distributed under the License is
#   distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied.  See
#   the License for the specific language governing
#   permissions and limitations under the License.
#------------------------------------------------------------------------------

from ..base.uvm_port_base import UVMPortBase
from .uvm_tlm_imps import *

#------------------------------------------------------------------------------
# Title: TLM Export Classes
#------------------------------------------------------------------------------
# The following classes define the TLM export classes.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#
# CLASS: uvm_*_export #(T)
#
# The unidirectional uvm_*_export is a port that ~forwards~ or ~promotes~
# an interface implementation from a child component to its parent.
# An export can be connected to any compatible child export or imp port.
# It must ultimately be connected to at least one implementation
# of its associated interface.
#
# The interface type represented by the asterisk is any of the following
#
#|  blocking_put
#|  nonblocking_put
#|  put
#|
#|  blocking_get
#|  nonblocking_get
#|  get
#|
#|  blocking_peek
#|  nonblocking_peek
#|  peek
#|
#|  blocking_get_peek
#|  nonblocking_get_peek
#|  get_peek
#
# Type parameters
#
# T - The type of transaction to be communicated by the export
#
# Exports are connected to interface implementations directly via
# <uvm_*_imp #(T,IMP)> ports or indirectly via other <uvm_*_export #(T)> exports.
#
#------------------------------------------------------------------------------
#
#
# Function: new
#
# The ~name~ and ~parent~ are the standard <uvm_component> constructor arguments.
# The ~min_size~ and ~max_size~ specify the minimum and maximum number of
# interfaces that must have been supplied to this port by the end of elaboration.
#
#|  function new (string name,
#|                uvm_component parent,
#|                int min_size=1,
#|                int max_size=1)

#class uvm_blocking_put_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_BLOCKING_PUT_MASK,"uvm_blocking_put_export")
#  `UVM_BLOCKING_PUT_IMP ('m_if', T, t)
class UVMBlockingPutExport(UVMPortBase):
    pass
UVM_EXPORT_COMMON(UVMBlockingPutExport, UVM_TLM_BLOCKING_PUT_MASK,"uvm_blocking_put_export")
UVM_BLOCKING_PUT_IMP('m_if', UVMBlockingPutExport)

#class uvm_nonblocking_put_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_NONBLOCKING_PUT_MASK,"uvm_nonblocking_put_export")
#  `UVM_NONBLOCKING_PUT_IMP ('m_if', T, t)
class uvm_nonblocking_put_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_nonblocking_put_export, UVM_TLM_NONBLOCKING_PUT_MASK,"uvm_nonblocking_put_export")
UVM_NONBLOCKING_PUT_IMP ('m_if', uvm_nonblocking_put_export)
UVMNonBlockingPutExport = uvm_nonblocking_put_export

#class uvm_put_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_PUT_MASK,"uvm_put_export")
#  `UVM_PUT_IMP ('m_if', T, t)
class uvm_put_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_put_export, UVM_TLM_PUT_MASK,"uvm_put_export")
UVM_PUT_IMP('m_if', uvm_put_export)
UVMPutExport = uvm_put_export

#class uvm_blocking_get_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_BLOCKING_GET_MASK,"uvm_blocking_get_export")
#  `UVM_BLOCKING_GET_IMP ('m_if', T, t)
class uvm_blocking_get_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_blocking_get_export, UVM_TLM_BLOCKING_GET_MASK,"uvm_blocking_get_export")
UVM_BLOCKING_GET_IMP ('m_if', uvm_blocking_get_export)
UVMBlockingGetExport = uvm_blocking_get_export

#class uvm_nonblocking_get_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_NONBLOCKING_GET_MASK,"uvm_nonblocking_get_export")
#  `UVM_NONBLOCKING_GET_IMP ('m_if', T, t)
class uvm_nonblocking_get_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_nonblocking_get_export, UVM_TLM_NONBLOCKING_GET_MASK,"uvm_nonblocking_get_export")
UVM_NONBLOCKING_GET_IMP ('m_if', uvm_nonblocking_get_export)
UVMBlockingGetExport = uvm_nonblocking_get_export

#class uvm_get_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_GET_MASK,"uvm_get_export")
#  `UVM_GET_IMP ('m_if', T, t)
class uvm_get_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_get_export, UVM_TLM_GET_MASK,"uvm_get_export")
UVM_GET_IMP ('m_if', uvm_get_export)
UVMGetExport = uvm_get_export

#class uvm_blocking_peek_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_BLOCKING_PEEK_MASK,"uvm_blocking_peek_export")
#  `UVM_BLOCKING_PEEK_IMP ('m_if', T, t)
class uvm_blocking_peek_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_blocking_peek_export, UVM_TLM_BLOCKING_PEEK_MASK,"uvm_blocking_peek_export")
UVM_BLOCKING_PEEK_IMP ('m_if', uvm_blocking_peek_export)
UVMBlockingPeekExport = uvm_blocking_peek_export

#class uvm_nonblocking_peek_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_NONBLOCKING_PEEK_MASK,"uvm_nonblocking_peek_export")
#  `UVM_NONBLOCKING_PEEK_IMP ('m_if', T, t)
class uvm_nonblocking_peek_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_nonblocking_peek_export, UVM_TLM_NONBLOCKING_PEEK_MASK,"uvm_nonblocking_peek_export")
UVM_NONBLOCKING_PEEK_IMP ('m_if', uvm_nonblocking_peek_export)
UVMNonBlockingPeekExport = uvm_nonblocking_peek_export

#class uvm_peek_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_PEEK_MASK,"uvm_peek_export")
#  `UVM_PEEK_IMP ('m_if', T, t)
class uvm_peek_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_peek_export, UVM_TLM_PEEK_MASK,"uvm_peek_export")
UVM_PEEK_IMP ('m_if', uvm_peek_export)
UVMPeekExport = uvm_peek_export

#class uvm_blocking_get_peek_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_BLOCKING_GET_PEEK_MASK,"uvm_blocking_get_peek_export")
#  `UVM_BLOCKING_GET_PEEK_IMP ('m_if', T, t)
class uvm_blocking_get_peek_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_blocking_get_peek_export, UVM_TLM_BLOCKING_GET_PEEK_MASK,"uvm_blocking_get_peek_export")
UVM_BLOCKING_GET_PEEK_IMP('m_if', uvm_blocking_get_peek_export)
UVMBlockingGetPeekExport = uvm_blocking_get_peek_export

#class uvm_nonblocking_get_peek_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_NONBLOCKING_GET_PEEK_MASK,"uvm_nonblocking_get_peek_export")
#  `UVM_NONBLOCKING_GET_PEEK_IMP ('m_if', T, t)
class uvm_nonblocking_get_peek_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_nonblocking_get_peek_export, UVM_TLM_NONBLOCKING_GET_PEEK_MASK,"uvm_nonblocking_get_peek_export")
UVM_NONBLOCKING_GET_PEEK_IMP ('m_if', uvm_nonblocking_get_peek_export)
UVMNonBlockingGetPeekExport = uvm_nonblocking_get_peek_export

#class uvm_get_peek_export #(type T=int)
#  extends uvm_port_base #(uvm_tlm_if_base #(T,T));
#  `UVM_EXPORT_COMMON(`UVM_TLM_GET_PEEK_MASK,"uvm_get_peek_export")
#  `UVM_GET_PEEK_IMP ('m_if', T, t)
class uvm_get_peek_export(UVMPortBase):
    pass
UVM_EXPORT_COMMON(uvm_get_peek_export, UVM_TLM_GET_PEEK_MASK,"uvm_get_peek_export")
UVM_GET_PEEK_IMP('m_if', uvm_get_peek_export)
UVMGetPeekExport = uvm_get_peek_export

#------------------------------------------------------------------------------
#
# CLASS: uvm_*_export #(REQ,RSP)
#
# The bidirectional uvm_*_export is a port that ~forwards~ or ~promotes~
# an interface implementation from a child component to its parent.
# An export can be connected to any compatible child export or imp port.
# It must ultimately be connected to at least one implementation
# of its associated interface.
#
# The interface type represented by the asterisk is any of the following
#
#|  blocking_transport
#|  nonblocking_transport
#|  transport
#|
#|  blocking_master
#|  nonblocking_master
#|  master
#|
#|  blocking_slave
#|  nonblocking_slave
#|  slave
#
# Type parameters
#
# REQ - The type of request transaction to be communicated by the export
#
# RSP - The type of response transaction to be communicated by the export
#
# Exports are connected to interface implementations directly via
# <uvm_*_imp #(REQ, RSP, IMP, REQ_IMP, RSP_IMP)> ports or indirectly via other
# <uvm_*_export #(REQ,RSP)> exports.
#
#------------------------------------------------------------------------------
#
# Function: new
#
# The ~name~ and ~parent~ are the standard <uvm_component> constructor arguments.
# The ~min_size~ and ~max_size~ specify the minimum and maximum number of
# interfaces that must have been supplied to this port by the end of elaboration.
#
#|  function new (string name,
#|                uvm_component parent,
#|                int min_size=1,
#|                int max_size=1)

#class uvm_blocking_master_export #(type REQ=int, type RSP=REQ)
#  extends uvm_port_base #(uvm_tlm_if_base #(REQ, RSP));
#  `UVM_EXPORT_COMMON(`UVM_TLM_BLOCKING_MASTER_MASK,"uvm_blocking_master_export")
#  `UVM_BLOCKING_PUT_IMP ('m_if', REQ, t)
#  `UVM_BLOCKING_GET_PEEK_IMP ('m_if', RSP, t)
class uvm_blocking_master_export:
    pass
UVM_EXPORT_COMMON(uvm_blocking_master_export, UVM_TLM_BLOCKING_MASTER_MASK,"uvm_blocking_master_export")
UVM_BLOCKING_PUT_IMP('m_if', uvm_blocking_master_export)
UVM_BLOCKING_GET_PEEK_IMP('m_if', uvm_blocking_master_export)
UVMBlockingMasterExport = uvm_blocking_master_export

#class uvm_nonblocking_master_export #(type REQ=int, type RSP=REQ)
#  extends uvm_port_base #(uvm_tlm_if_base #(REQ, RSP));
#  `UVM_EXPORT_COMMON(`UVM_TLM_NONBLOCKING_MASTER_MASK,"uvm_nonblocking_master_export")
#  `UVM_NONBLOCKING_PUT_IMP ('m_if', REQ, t)
#  `UVM_NONBLOCKING_GET_PEEK_IMP ('m_if', RSP, t)
class uvm_nonblocking_master_export:
    pass
UVM_EXPORT_COMMON(uvm_nonblocking_master_export, UVM_TLM_NONBLOCKING_MASTER_MASK,
    "uvm_nonblocking_master_export")
UVM_NONBLOCKING_PUT_IMP('m_if', uvm_nonblocking_master_export)
UVM_NONBLOCKING_GET_PEEK_IMP('m_if', uvm_nonblocking_master_export)
UVMNonBlockingMasterExport = uvm_nonblocking_master_export

#class uvm_master_export #(type REQ=int, type RSP=REQ)
#  extends uvm_port_base #(uvm_tlm_if_base #(REQ, RSP));
#  `UVM_EXPORT_COMMON(`UVM_TLM_MASTER_MASK,"uvm_master_export")
#  `UVM_PUT_IMP ('m_if', REQ, t)
#  `UVM_GET_PEEK_IMP ('m_if', RSP, t)
class uvm_master_export:
    pass
UVM_EXPORT_COMMON(uvm_master_export, UVM_TLM_MASTER_MASK, "uvm_master_port")
UVM_PUT_IMP('m_if', uvm_master_export)
UVM_GET_PEEK_IMP('m_if', uvm_master_export)
UVMMasterExport = uvm_master_export

#class uvm_blocking_slave_export #(type REQ=int, type RSP=REQ)
#  extends uvm_port_base #(uvm_tlm_if_base #(RSP, REQ));
#  `UVM_EXPORT_COMMON(`UVM_TLM_BLOCKING_SLAVE_MASK,"uvm_blocking_slave_export")
#  `UVM_BLOCKING_PUT_IMP ('m_if', RSP, t)
#  `UVM_BLOCKING_GET_PEEK_IMP ('m_if', REQ, t)
class uvm_blocking_slave_export:  #(type REQ=int, type RSP=REQ)
    pass
UVM_EXPORT_COMMON(uvm_blocking_slave_export, UVM_TLM_BLOCKING_SLAVE_MASK, "uvm_blocking_slave_export")
UVM_BLOCKING_PUT_IMP('m_if', uvm_blocking_slave_export)
UVM_BLOCKING_GET_PEEK_IMP('m_if', uvm_blocking_slave_export)

#class uvm_nonblocking_slave_export #(type REQ=int, type RSP=REQ)
#  extends uvm_port_base #(uvm_tlm_if_base #(RSP, REQ));
#  `UVM_EXPORT_COMMON(`UVM_TLM_NONBLOCKING_SLAVE_MASK,"uvm_nonblocking_slave_export")
#  `UVM_NONBLOCKING_PUT_IMP ('m_if', RSP, t)
#  `UVM_NONBLOCKING_GET_PEEK_IMP ('m_if', REQ, t)
class uvm_nonblocking_slave_export:  #(type REQ=int, type RSP=REQ)
    pass
UVM_EXPORT_COMMON(uvm_nonblocking_slave_export, UVM_TLM_NONBLOCKING_SLAVE_MASK,"uvm_nonblocking_slave_export")
UVM_NONBLOCKING_PUT_IMP('m_if', uvm_nonblocking_slave_export)
UVM_NONBLOCKING_GET_PEEK_IMP('m_if', uvm_nonblocking_slave_export)
UVMNonBlockingSlaveExport = uvm_nonblocking_slave_export


#class uvm_slave_export #(type REQ=int, type RSP=REQ)
#  extends uvm_port_base #(uvm_tlm_if_base #(RSP, REQ));
#  `UVM_EXPORT_COMMON(`UVM_TLM_SLAVE_MASK,"uvm_slave_export")
#  `UVM_PUT_IMP ('m_if', RSP, t)
#  `UVM_GET_PEEK_IMP ('m_if', REQ, t)
class uvm_slave_export:  # (type REQ=int, type RSP=REQ)
    pass
UVM_EXPORT_COMMON(uvm_slave_export, UVM_TLM_SLAVE_MASK,"uvm_slave_export")
UVM_PUT_IMP('m_if', uvm_slave_export)
UVM_GET_PEEK_IMP('m_if', uvm_slave_export)
UVMSlaveExport = uvm_slave_export

#class uvm_blocking_transport_export #(type REQ=int, type RSP=REQ)
#  extends uvm_port_base #(uvm_tlm_if_base #(REQ, RSP));
#  `UVM_EXPORT_COMMON(`UVM_TLM_BLOCKING_TRANSPORT_MASK,"uvm_blocking_transport_export")
#  `UVM_BLOCKING_TRANSPORT_IMP ('m_if', REQ, RSP, req, rsp)
class uvm_blocking_transport_export:  #(type REQ=int, type RSP=REQ)
    pass
UVM_EXPORT_COMMON(uvm_blocking_transport_export, UVM_TLM_BLOCKING_TRANSPORT_MASK,
        "uvm_blocking_transport_export")
UVM_BLOCKING_TRANSPORT_IMP('m_if', uvm_blocking_transport_export)
UVMBlockingTransportExport = uvm_blocking_transport_export


#class uvm_nonblocking_transport_export #(type REQ=int, type RSP=REQ)
#  extends uvm_port_base #(uvm_tlm_if_base #(REQ, RSP));
#  `UVM_EXPORT_COMMON(`UVM_TLM_NONBLOCKING_TRANSPORT_MASK,"uvm_nonblocking_transport_export")
#  `UVM_NONBLOCKING_TRANSPORT_IMP ('m_if', REQ, RSP, req, rsp)
class uvm_nonblocking_transport_export:  #(type REQ=int, type RSP=REQ)
    pass
UVM_EXPORT_COMMON(uvm_nonblocking_transport_export, UVM_TLM_NONBLOCKING_TRANSPORT_MASK,"uvm_nonblocking_transport_export")
UVM_NONBLOCKING_TRANSPORT_IMP('m_if', uvm_nonblocking_transport_export)
UVMNonBlockingTransportExport = uvm_nonblocking_transport_export

#class uvm_transport_export #(type REQ=int, type RSP=REQ)
#  extends uvm_port_base #(uvm_tlm_if_base #(REQ, RSP));
#  `UVM_EXPORT_COMMON(`UVM_TLM_TRANSPORT_MASK,"uvm_transport_export")
#  `UVM_TRANSPORT_IMP ('m_if', REQ, RSP, req, rsp)
class uvm_transport_export:  #(type REQ=int, type RSP=REQ)
    pass
UVM_EXPORT_COMMON(uvm_transport_export, UVM_TLM_TRANSPORT_MASK,"uvm_transport_export")
UVM_TRANSPORT_IMP ('m_if', uvm_transport_export)
UVMTransportExport = uvm_transport_export

