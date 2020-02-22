#//
#// -------------------------------------------------------------
#//    Copyright 2004-2011 Synopsys, Inc.
#//    Copyright 2010 Mentor Graphics Corporation
#//    Copyright 2010 Cadence Design Systems, Inc.
#//    Copyright 2019-2020 Tuomas Poikela (tpoikela)
#//    All Rights Reserved Worldwide
#//
#//    Licensed under the Apache License, Version 2.0 (the
#//    "License"); you may not use this file except in
#//    compliance with the License.  You may obtain a copy of
#//    the License at
#//
#//        http://www.apache.org/licenses/LICENSE-2.0
#//
#//    Unless required by applicable law or agreed to in
#//    writing, software distributed under the License is
#//    distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#//    CONDITIONS OF ANY KIND, either express or implied.  See
#//    the License for the specific language governing
#//    permissions and limitations under the License.
#// -------------------------------------------------------------
#//

import cocotb
from cocotb.clock import Clock
from uvm import (UVMConfigDb, run_test, UVMCoreService, sv,
    UVMRegSequence, uvm_fatal)
from apb.apb_if import apb_if


@cocotb.test()
def initial_begin(dut):
    cs_ = UVMCoreService.get()
    env = tb_env("env")

    vif = apb_if(dut)
    cocotb.fork(Clock(dut.clk, 10, "NS").start())
    svr = cs_.get_report_server()
    svr.set_max_quit_count(10)

    seq_name = []
    if sv.value_plusargs("UVM_SEQUENCE=%s", seq_name):
        seq = UVMRegSequence.create_type_by_name(seq_name[0], "tb")
        if seq is None:
            uvm_fatal("NO_SEQUENCE",
                "This env requires you to specify the sequence to run using UVM_SEQUENCE=<name>")
        env.seq = seq


    UVMConfigDb.set(env, "apb", "vif", vif)
    UVMConfigDb.set(None, "DUT_REF", "dut", dut)
    yield run_test()