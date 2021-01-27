#!/usr/bin/env python3

import sys
sys.path.append("../../src")
import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
from uvm import UVMRegBlock, UVMReg, UVMRegField, UVMRegItem, uvm_hdl
from uvm.macros import uvm_object_utils
from uvm.reg.uvm_reg_model import *

class Register(UVMReg):
    def __init__(self, name):
        super().__init__(name, 32)

    def build(self):
        self.count = UVMRegField.type_id.create("count")
        self.count.configure(self, 32, 0, "RO", True, 0, True, False, False)
    
uvm_object_utils(Register)

class Regfile(UVMRegBlock):
    def __init__(self, name='regfile'):
        super().__init__(name, UVM_NO_COVERAGE)

    def build(self):
        self.count = Register.type_id.create("count_qs")
        self.count.configure(self, None, "count_q")
        self.count.build()

uvm_object_utils(Regfile)


@cocotb.test()
async def test(dut):
    regfile = Regfile("register_file")
    regfile.add_hdl_path("u_reg")
    regfile.build()

    uvm_hdl.set_dut(dut)

    cocotb.fork(Clock(dut.clk, 5, 'ns').start())
    dut.rst_n <= 1
    await RisingEdge(dut.clk)
    dut.rst_n <= 0
    await RisingEdge(dut.clk)
    dut.rst_n <= 1
    
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    print(regfile.count.get_mirrored_value())
    
    await Timer(100,'ns')
    await RisingEdge(dut.clk)
    print(int(dut.u_reg.count_q.value))
    print("%s needs_update=%s"%(regfile.count.name, regfile.count.needs_update()))
    
    rw = UVMRegItem.type_id.create("pseudo-read_item", None, "")
    regfile.count.backdoor_read(rw)
    print("backdoor_value=%s"%rw.value[0])
    print("mirrored_value=%s"%regfile.count.get_mirrored_value()) 