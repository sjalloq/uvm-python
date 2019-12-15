#
#----------------------------------------------------------------------
#   Copyright 2007-2011 Mentor Graphics Corporation
#   Copyright 2007-2010 Cadence Design Systems, Inc.
#   Copyright 2010 Synopsys, Inc.
#   Copyright 2013 NVIDIA Corporation
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
#----------------------------------------------------------------------

import cocotb
from cocotb.triggers import Timer
from .uvm_phase import UVMPhase
from .uvm_object_globals import *
from .uvm_debug import uvm_debug
from .uvm_globals import *

#------------------------------------------------------------------------------
#
# Class: uvm_task_phase
#
#------------------------------------------------------------------------------
# Base class for all task phases.
# It forks a call to <uvm_phase::exec_task()>
# for each component in the hierarchy.
#
# The completion of the task does not imply, nor is it required for,
# the end of phase. Once the phase completes, any remaining forked
# <uvm_phase::exec_task()> threads are forcibly and immediately killed.
#
# By default, the way for a task phase to extend over time is if there is
# at least one component that raises an objection.
#| class my_comp extends uvm_component;
#|    task main_phase(uvm_phase phase);
#|       phase.raise_objection(this, "Applying stimulus")
#|       ...
#|       phase.drop_objection(this, "Applied enough stimulus")
#|    endtask
#| endclass
#
#
# There is however one scenario wherein time advances within a task-based phase
# without any objections to the phase being raised. If two (or more) phases
# share a common successor, such as the <uvm_run_phase> and the
# <uvm_post_shutdown_phase> sharing the <uvm_extract_phase> as a successor,
# then phase advancement is delayed until all predecessors of the common
# successor are ready to proceed.  Because of this, it is possible for time to
# advance between <uvm_component::phase_started> and <uvm_component::phase_ended>
# of a task phase without any participants in the phase raising an objection.

class UVMTaskPhase(UVMPhase):

    #  // Function: new
    #  //
    #  // Create a new instance of a task-based phase
    #  //
    def __init__(self, name):
        UVMPhase.__init__(self, name, UVM_PHASE_IMP)
        self.m_is_task_phase = True

    #  // Function: traverse
    #  //
    #  // Traverses the component tree in bottom-up order, calling <execute> for
    #  // each component. The actual order for task-based phases doesn't really
    #  // matter, as each component task is executed in a separate process whose
    #  // starting order is not deterministic.
    #  //
    @cocotb.coroutine
    def traverse(self, comp, phase, state):
        phase.m_num_procs_not_yet_returned = 0
        yield self.m_traverse(comp, phase, state)

    @cocotb.coroutine
    def m_traverse(self, comp, phase, state):
        name = ""
        phase_domain = phase.get_domain()
        comp_domain = comp.get_domain()

        if comp.has_first_child():
            child = comp.get_first_child()
            while child is not None:
                uvm_debug(self, "m_traverse", "Yielding now child traverse with "
                    + child.get_name())
                yield self.m_traverse(child, phase, state)
                child = comp.get_next_child()

        uvm_debug(self, "m_traverse", comp.get_name() + "Comp children done.  Moving to its own phase..")

        if UVMPhase.m_phase_trace:
            dom_name = "unknown"
            if comp_domain is not None:
                dom_name = comp_domain.get_name()
            uvm_report_info("PH_TRACE",
                ("topdown-phase phase={} state={} comp={} comp.domain={} phase.domain={}".format(
                  phase.get_name(), str(state), comp.get_full_name(), dom_name,phase_domain.get_name()
                  )), UVM_DEBUG)

        from .uvm_domain import UVMDomain
        if (phase_domain == UVMDomain.get_common_domain() or phase_domain == comp_domain):
            if state == UVM_PHASE_STARTED:
                comp.m_current_phase = phase
                comp.m_apply_verbosity_settings(phase)
                comp.phase_started(phase)
                if hasattr(comp, 'm_sequencer_id'):
                    seqr = comp # was if ($cast(seqr, comp))
                    yield seqr.start_phase_sequence(phase)
            elif state == UVM_PHASE_EXECUTING:
                ph = self # uvm_phase
                if self in comp.m_phase_imps:
                    ph = comp.m_phase_imps[self]

                uvm_debug(self, "m_traverse", comp.get_name() + " yield ph.execute")
                yield ph.execute(comp, phase);
            elif state == UVM_PHASE_READY_TO_END:
                comp.phase_ready_to_end(phase)
            elif state == UVM_PHASE_ENDED:
                uvm_debug(self, "m_traverse", "KKK")
                if hasattr(comp, 'm_sequencer_id'):
                    seqr = comp # was if ($cast(seqr, comp))
                    seqr.stop_phase_sequence(phase);
                comp.phase_ended(phase);
                comp.m_current_phase = None
            else:
                uvm_report_fatal("PH_BADEXEC","task phase traverse internal error")
        uvm_debug(self, "m_traverse", "KKK SSS ZZZ")

    #  // Function: execute
    #  //
    #  // Fork the task-based phase ~phase~ for the component ~comp~.
    #  //
    @cocotb.coroutine
    def execute(self, comp, phase):
        uvm_debug(self, 'execute', 'exec task_phase |' + self.get_name() + '| with comp: ' +
                comp.get_name())
        #fork
        #begin
        #process proc;
        # reseed this process for random stability
        #proc = process::self();
        #proc.srandom(uvm_create_random_seed(phase.get_type_name(), comp.get_full_name()));
        phase.m_num_procs_not_yet_returned += 1
        proc = cocotb.fork(self.exec_task(comp,phase))
        phase.m_num_procs_not_yet_returned -= 1
        yield Timer(0)
        #end
        #join_none
        #endfunction
    #endclass
