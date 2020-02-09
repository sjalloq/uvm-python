#------------------------------------------------------------------------------
#   Copyright 2007-2010 Mentor Graphics Corporation
#   Copyright 2007-2009 Cadence Design Systems, Inc.
#   Copyright 2010 Synopsys, Inc.
#   Copyright 2019 Tuomas Poikela
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

from .uvm_callback import (UVMCallback, UVMCallbacks, UVMCallbackIter,
    UVMCallbacksBase)
from .uvm_object_globals import *


class sev_id_struct:
    def __init__(self):
        self.sev_specified = False
        self.id_specified = False
        self.sev = 0
        self.id = ""
        self.is_on = False


# tpoikela: Not typedef like in SV-UVM, but special class with
# CB=UVMReportCatcher
class UVMReportCb(UVMCallbacks):

    def __init__(self, name='uvm_report_cb'):
        super().__init__(name, T=None, CB=UVMReportCatcher)

    @classmethod
    def get_first(cls, itr, obj):
        return super().get_first(itr, obj, UVMReportCatcher)


UVMReportCbIter = UVMCallbackIter

#------------------------------------------------------------------------------
#
# CLASS: uvm_report_catcher
#
# The uvm_report_catcher is used to catch messages issued by the uvm report
# server. Catchers are
# uvm_callbacks#(<uvm_report_object>,uvm_report_catcher) objects,
# so all facilities in the <uvm_callback> and <uvm_callbacks#(T,CB)>
# classes are available for registering catchers and controlling catcher
# state.
#
# The uvm_callbacks#(<uvm_report_object>,uvm_report_catcher) class is
# aliased to ~uvm_report_cb~ to make it easier to use.
# Multiple report catchers can be
# registered with a report object. The catchers can be registered as default
# catchers which catch all reports on all <uvm_report_object> reporters,
# or catchers can be attached to specific report objects (i.e. components).
#
# User extensions of <uvm_report_catcher> must implement the <catch> method in
# which the action to be taken on catching the report is specified. The catch
# method can return ~CAUGHT~, in which case further processing of the report is
# immediately stopped, or return ~THROW~ in which case the (possibly modified) report
# is passed on to other registered catchers. The catchers are processed in the order
# in which they are registered.
#
# On catching a report, the <catch> method can modify the severity, id, action,
# verbosity or the report string itself before the report is finally issued by
# the report server. The report can be immediately issued from within the catcher
# class by calling the <issue> method.
#
# The catcher maintains a count of all reports with FATAL,ERROR or WARNING severity
# and a count of all reports with FATAL, ERROR or WARNING severity whose severity
# was lowered. These statistics are reported in the summary of the <uvm_report_server>.
#
# This example shows the basic concept of creating a report catching
# callback and attaching it to all messages that get emitted:
#
#| class my_error_demoter extends uvm_report_catcher
#|   function new(string name="my_error_demoter")
#|     super.new(name)
#|   endfunction
#|   //This example demotes "MY_ID" errors to an info message
#|   function action_e catch()
#|     if(get_severity() == UVM_ERROR && get_id() == "MY_ID")
#|       set_severity(UVM_INFO)
#|     return THROW
#|   endfunction
#| endclass
#|
#| my_error_demoter demoter = new
#| initial begin
#|  // Catchers are callbacks on report objects (components are report
#|  // objects, so catchers can be attached to components).
#|
#|  // To affect all reporters, use ~null~ for the object
#|  uvm_report_cb::add(null, demoter)
#|
#|  // To affect some specific object use the specific reporter
#|  uvm_report_cb::add(mytest.myenv.myagent.mydriver, demoter)
#|
#|  // To affect some set of components (any "*driver" under mytest.myenv)
#|  // using the component name
#|  uvm_report_cb::add_by_name("*driver", demoter, mytest.myenv)
#| end
#
#
#------------------------------------------------------------------------------



UNKNOWN_ACTION = 0
THROW = 1
CAUGHT = 2


class UVMReportCatcher(UVMCallback):
    #`uvm_register_cb(uvm_report_object,uvm_report_catcher)
    m_modified_report_message = None  # UMVReportMessage
    m_orig_report_message = None  # UVMReportMessage
    m_set_action_called = False

    # Counts for the demoteds and caughts
    m_demoted_fatal = 0
    m_demoted_error = 0
    m_demoted_warning = 0
    m_caught_fatal = 0
    m_caught_error = 0
    m_caught_warning = 0

    #// Flag counts
    DO_NOT_CATCH      = 1
    DO_NOT_MODIFY     = 2
    m_debug_flags = 0

    do_report = False

    #// Function: new
    #//
    #// Create a new report catcher. The name argument is optional, but
    #// should generally be provided to aid in debugging.

    def __init__(self, name="uvm_report_catcher"):
        super().__init__(name)
        UVMReportCatcher.do_report = True

    #// Group: Current Message State
    #
    #// Function: get_client
    #//
    #// Returns the <uvm_report_object> that has generated the message that
    #// is currently being processed.
    def get_client(self):
        return UVMReportCatcher.m_modified_report_message.get_report_object()

    #// Function: get_severity
    #//
    #// Returns the <uvm_severity> of the message that is currently being
    #// processed. If the severity was modified by a previously executed
    #// catcher object (which re-threw the message), then the returned
    #// severity is the modified value.
    def get_severity(self):
        return UVMReportCatcher.m_modified_report_message.get_severity()
    #
    #// Function: get_context
    #//
    #// Returns the context name of the message that is currently being
    #// processed. This is typically the full hierarchical name of the component
    #// that issued the message. However, if user-defined context is set from
    #// a uvm_report_message, the user-defined context will be returned.
    def get_context(self):
        context_str = self.m_modified_report_message.get_context()
        if (context_str == ""):
            rh = self.m_modified_report_message.get_report_handler()
            context_str = rh.get_full_name()
        return context_str


    #// Function: get_verbosity
    #//
    #// Returns the verbosity of the message that is currently being
    #// processed. If the verbosity was modified by a previously executed
    #// catcher (which re-threw the message), then the returned
    #// verbosity is the modified value.
    #
    def get_verbosity(self):
        return self.m_modified_report_message.get_verbosity()


    #// Function: get_id
    #//
    #// Returns the string id of the message that is currently being
    #// processed. If the id was modified by a previously executed
    #// catcher (which re-threw the message), then the returned
    #// id is the modified value.
    #
    def get_id(self):
        return self.m_modified_report_message.get_id()


    #// Function: get_message
    #//
    #// Returns the string message of the message that is currently being
    #// processed. If the message was modified by a previously executed
    #// catcher (which re-threw the message), then the returned
    #// message is the modified value.
    #
    def get_message(self):
        return self.m_modified_report_message.get_message()


    #// Function: get_action
    #//
    #// Returns the <uvm_action> of the message that is currently being
    #// processed. If the action was modified by a previously executed
    #// catcher (which re-threw the message), then the returned
    #// action is the modified value.
    #
    def get_action(self):
        return self.m_modified_report_message.get_action()


    #// Function: get_fname
    #//
    #// Returns the file name of the message.
    #
    def get_fname(self):
        return self.m_modified_report_message.get_filename()


    #// Function: get_line
    #//
    #// Returns the line number of the message.
    #
    def get_line(self):
        return self.m_modified_report_message.get_line()


    #// Function: get_element_container
    #//
    #// Returns the element container of the message.
    #
    def get_element_container(self):
        return self.m_modified_report_message.get_element_container()


    #
    #// Group: Change Message State
    #
    #// Function: set_severity
    #//
    #// Change the severity of the message to ~severity~. Any other
    #// report catchers will see the modified value.
    def set_severity(self, severity):
        self.m_modified_report_message.set_severity(severity)


    #// Function: set_verbosity
    #//
    #// Change the verbosity of the message to ~verbosity~. Any other
    #// report catchers will see the modified value.
    #
    def set_verbosity(self, verbosity):
        self.m_modified_report_message.set_verbosity(verbosity)


    #// Function: set_id
    #//
    #// Change the id of the message to ~id~. Any other
    #// report catchers will see the modified value.
    #
    def set_id(self, id):
        self.m_modified_report_message.set_id(id)


    #// Function: set_message
    #//
    #// Change the text of the message to ~message~. Any other
    #// report catchers will see the modified value.
    def set_message(self, message):
        self.m_modified_report_message.set_message(message)


    #// Function: set_action
    #//
    #// Change the action of the message to ~action~. Any other
    #// report catchers will see the modified value.
    #
    def set_action(self, action):
        self.m_modified_report_message.set_action(action)
        self.m_set_action_called = 1

    #// Function: set_context
    #//
    #// Change the context of the message to ~context_str~. Any other
    #// report catchers will see the modified value.
    def set_context(self, context_str):
        self.m_modified_report_message.set_context(context_str)


    #// Function: add_int
    #//
    #// Add an integral type of the name ~name~ and value ~value~ to
    #// the message.  The required ~size~ field indicates the size of ~value~.
    #// The required ~radix~ field determines how to display and
    #// record the field. Any other report catchers will see the newly
    #// added element.
    #//
    #
    #protected function void add_int(string name,
    #      			  uvm_bitstream_t value,
    #      			  int size,
    #      			  uvm_radix_enum radix,
    #      			  uvm_action action = (UVM_LOG|UVM_RM_RECORD))
    #  self.m_modified_report_message.add_int(name, value, size, radix, action)
    #endfunction
    #
    #
    #// Function: add_string
    #//
    #// Adds a string of the name ~name~ and value ~value~ to the
    #// message. Any other report catchers will see the newly
    #// added element.
    #//
    #
    #protected function void add_string(string name,
    #      			     string value,
    #                                   uvm_action action = (UVM_LOG|UVM_RM_RECORD))
    #  self.m_modified_report_message.add_string(name, value, action)
    #endfunction
    #
    #
    #// Function: add_object
    #//
    #// Adds a uvm_object of the name ~name~ and reference ~obj~ to
    #// the message. Any other report catchers will see the newly
    #// added element.
    #//
    #
    #protected function void add_object(string name,
    #      			     uvm_object obj,
    #                                   uvm_action action = (UVM_LOG|UVM_RM_RECORD))
    #  self.m_modified_report_message.add_object(name, obj, action)
    #endfunction


    #// Group: Debug

    #// Function: get_report_catcher
    #//
    #// Returns the first report catcher that has ~name~.

    #static function uvm_report_catcher get_report_catcher(string name)
    #  static uvm_report_cb_iter iter = new(null)
    #  get_report_catcher = iter.first()
    #  while(get_report_catcher != null) begin
    #    if(get_report_catcher.get_name() == name)
    #      return get_report_catcher
    #    get_report_catcher = iter.next()
    #  end
    #  return null
    #endfunction


    #// Function: print_catcher
    #//
    #// Prints information about all of the report catchers that are
    #// registered. For finer grained detail, the <uvm_callbacks #(T,CB)::display>
    #// method can be used by calling uvm_report_cb::display(<uvm_report_object>).

    #static function void print_catcher(UVM_FILE file = 0)
    #        string msg
    #        string enabled
    #        uvm_report_catcher catcher
    #        static uvm_report_cb_iter iter = new(null)
    #        string q[$]
    #
    #        q.push_back("-------------UVM REPORT CATCHERS----------------------------\n")
    #
    #        catcher = iter.first()
    #        while(catcher != null) begin
    #      	  if(catcher.callback_mode())
    #      		  enabled = "ON"
    #      	  else
    #      		  enabled = "OFF"
    #
    #      	  q.push_back($sformatf("%20s : %s\n", catcher.get_name(),enabled))
    #      	  catcher = iter.next()
    #        end
    #        q.push_back("--------------------------------------------------------------\n")
    #
    #        `uvm_info_context("UVM/REPORT/CATCHER",`UVM_STRING_QUEUE_STREAMING_PACK(q),UVM_LOW,uvm_top)
    #endfunction

    #// Funciton: debug_report_catcher
    #//
    #// Turn on report catching debug information. ~what~ is a bitwise AND of
    #// * DO_NOT_CATCH  -- forces catch to be ignored so that all catchers see the
    #//   the reports.
    #// * DO_NOT_MODIFY -- forces the message to remain unchanged
    #
    #static function void debug_report_catcher(int what= 0)
    #  m_debug_flags = what
    #endfunction
    #

    #// Group: Callback Interface

    #// Function: catch
    #//
    #// This is the method that is called for each registered report catcher.
    #// There are no arguments to this function. The <Current Message State>
    #// interface methods can be used to access information about the
    #// current message being processed.
    #
    def catch(self):
        raise Exception("catch() must be implemented in user-class")


    #// Group: Reporting

    # // Function: uvm_report_fatal
    # //
    # // Issues a fatal message using the current message's report object.
    # // This message will bypass any message catching callbacks.
    #
    # protected function void uvm_report_fatal(string id,
    #      				    string message,
    #      				    int verbosity,
    #      				    string fname = "",
    #      				    int line = 0,
    #      				    string context_name = "",
    #      				    bit report_enabled_checked = 0)
    #
    #   self.uvm_report(UVM_FATAL, id, message, UVM_NONE, fname, line,
    #                   context_name, report_enabled_checked)
    # endfunction


    # // Function: uvm_report_error
    # //
    # // Issues an error message using the current message's report object.
    # // This message will bypass any message catching callbacks.
    #
    # protected function void uvm_report_error(string id,
    #      				    string message,
    #      				    int verbosity,
    #      				    string fname = "",
    #      				    int line = 0,
    #      				    string context_name = "",
    #      				    bit report_enabled_checked = 0)
    #
    #   self.uvm_report(UVM_ERROR, id, message, UVM_NONE, fname, line,
    #                   context_name, report_enabled_checked)
    # endfunction


    # // Function: uvm_report_warning
    # //
    # // Issues a warning message using the current message's report object.
    # // This message will bypass any message catching callbacks.
    #
    # protected function void uvm_report_warning(string id,
    #      				      string message,
    #      				      int verbosity,
    #      				      string fname = "",
    #      				      int line = 0,
    #      				      string context_name = "",
    #      				      bit report_enabled_checked = 0)
    #
    #   self.uvm_report(UVM_WARNING, id, message, UVM_NONE, fname, line,
    #                   context_name, report_enabled_checked)
    # endfunction
    #
    #
    # // Function: uvm_report_info
    # //
    # // Issues a info message using the current message's report object.
    # // This message will bypass any message catching callbacks.
    #
    # protected function void uvm_report_info(string id,
    #      				   string message,
    #      				   int verbosity,
    #      				   string fname = "",
    #      				   int line = 0,
    #      				   string context_name = "",
    #      				   bit report_enabled_checked = 0)
    #
    #   self.uvm_report(UVM_INFO, id, message, verbosity, fname, line,
    #                   context_name, report_enabled_checked)
    # endfunction
    #
    # // Function: uvm_report
    # //
    # // Issues a message using the current message's report object.
    # // This message will bypass any message catching callbacks.
    #
    # protected function void uvm_report(uvm_severity severity,
    #      			      string id,
    #      			      string message,
    #      			      int verbosity,
    #      			      string fname = "",
    #      			      int line = 0,
    #      			      string context_name = "",
    #      			      bit report_enabled_checked = 0)
    #
    #   uvm_report_message l_report_message
    #   if (report_enabled_checked == 0) begin
    #     if (!uvm_report_enabled(verbosity, severity, id))
    #       return
    #   end
    #
    #   l_report_message = uvm_report_message::new_report_message()
    #   l_report_message.set_report_message(severity, id, message,
    #      				 verbosity, fname, line, context_name)
    #   self.uvm_process_report_message(l_report_message)
    # endfunction
    #
    # protected function void uvm_process_report_message(uvm_report_message msg)
    #   uvm_report_object ro = m_modified_report_message.get_report_object()
    #   uvm_action a = ro.get_report_action(msg.get_severity(), msg.get_id())
    #
    #   if(a) begin
    #     string composed_message
    #     uvm_report_server rs = m_modified_report_message.get_report_server()
    #
    #     msg.set_report_object(ro)
    #     msg.set_report_handler(m_modified_report_message.get_report_handler())
    #     msg.set_report_server(rs)
    #     msg.set_file(ro.get_report_file_handle(msg.get_severity(), msg.get_id()))
    #     msg.set_action(a)
    #
    #     // no need to compose when neither UVM_DISPLAY nor UVM_LOG is set
    #     if (a & (UVM_LOG|UVM_DISPLAY))
    #       composed_message = rs.compose_report_message(msg)
    #     rs.execute_report_message(msg, composed_message)
    #   end
    # endfunction


    #// Function: issue
    #// Immediately issues the message which is currently being processed. This
    #// is useful if the message is being ~CAUGHT~ but should still be emitted.
    #//
    #// Issuing a message will update the report_server stats, possibly multiple
    #// times if the message is not ~CAUGHT~.

    #protected function void issue()
    #   string composed_message
    #   uvm_report_server rs = m_modified_report_message.get_report_server()
    #
    #   if(uvm_action_type'(m_modified_report_message.get_action()) != UVM_NO_ACTION)
    #   begin
    #     // no need to compose when neither UVM_DISPLAY nor UVM_LOG is set
    #     if (m_modified_report_message.get_action() & (UVM_LOG|UVM_DISPLAY))
    #       composed_message = rs.compose_report_message(m_modified_report_message)
    #     rs.execute_report_message(m_modified_report_message, composed_message)
    #   end
    #endfunction


    in_catcher = 0
    #//process_all_report_catchers
    #//method called by report_server.report to process catchers
    #//
    @classmethod
    def process_all_report_catchers(cls, rm):
        _iter = UVMCallback("_iter")
        catcher = None  # uvm_report_catcher
        thrown = 1
        orig_severity = 0  # uvm_severity
        #cls.in_catcher = 0  # static bit in_catcher
        l_report_object = rm.get_report_object()  # uvm_report_object

        if cls.in_catcher == 1:
            return 1

        cls.in_catcher = 1
        UVMCallbacksBase.m_tracing = 0  # turn off cb tracing so catcher stuff doesn't print

        orig_severity = rm.get_severity()  # cast to 'uvm_severity' removed
        cls.m_modified_report_message = rm

        catcher = UVMReportCb.get_first(_iter, l_report_object)
        if catcher is not None:
            if cls.m_debug_flags & cls.DO_NOT_MODIFY:
                #process p = process::self(); // Keep random stability
                p = None
                randstate = ""
                if p is not None:
                    randstate = p.get_randstate()
                cls.m_orig_report_message = rm.clone()
                #sv.cast(m_orig_report_message, rm.clone()) # have to clone, rm can be extended type
                if p is not None:
                    p.set_randstate(randstate)

        while catcher is not None:
            prev_sev = 0  # uvm_severity

            if catcher.callback_mode() is False:
                catcher = UVMReportCb.get_next(_iter, l_report_object)
                continue


            prev_sev = cls.m_modified_report_message.get_severity()
            cls.m_set_action_called = False
            thrown = catcher.process_report_catcher()

            # Set the action to the default action for the new severity
            # if it is still at the default for the previous severity,
            # unless it was explicitly set.
            if (not cls.m_set_action_called and
                cls.m_modified_report_message.get_severity() != prev_sev and
                cls.m_modified_report_message.get_action() ==
                l_report_object.get_report_action(prev_sev, "*@&*^*^*#")):

                cls.m_modified_report_message.set_action(
                    l_report_object.get_report_action(cls.m_modified_report_message.get_severity(), "*@&*^*^*#"))

            if thrown == 0:
                if orig_severity == UVM_FATAL:
                    cls.m_caught_fatal += 1
                elif orig_severity == UVM_ERROR:
                    cls.m_caught_error += 1
                elif orig_severity == UVM_WARNING:
                    cls.m_caught_warning += 1
                break
            catcher = UVMReportCb.get_next(_iter,l_report_object)

        # update counters if message was returned with demoted severity
        if orig_severity == UVM_FATAL:
            if cls.m_modified_report_message.get_severity() < orig_severity:
                cls.m_demoted_fatal += 1
        elif orig_severity == UVM_ERROR:
            if cls.m_modified_report_message.get_severity() < orig_severity:
                cls.m_demoted_error += 1
        elif orig_severity == UVM_WARNING:
            if cls.m_modified_report_message.get_severity() < orig_severity:
                cls.m_demoted_warning += 1

        cls.in_catcher = 0
        UVMCallbacksBase.m_tracing = 1  # turn tracing stuff back on
        return thrown


    #
    #//process_report_catcher
    #//internal method to call user <catch()> method
    #//
    def process_report_catcher(self):
        act = self.catch()

        if act == UNKNOWN_ACTION:
            self.uvm_report_error("RPTCTHR", "uvm_report_self.catch() in catcher instance "
                + self.get_name() + " must return THROW or CAUGHT", UVM_NONE)

        cls = UVMReportCatcher
        if cls.m_debug_flags & cls.DO_NOT_MODIFY:
            cls.m_modified_report_message.copy(cls.m_orig_report_message)

        if act == CAUGHT and not (cls.m_debug_flags & cls.DO_NOT_CATCH):
            return 0
        return 1

    #// Function: summarize
    #//
    #// This function is called automatically by <uvm_report_server::report_summarize()>.
    #// It prints the statistics for the active catchers.
    @classmethod
    def summarize(cls):
        s = ""
        q = []
        if UVMReportCatcher.do_report:
            q.append("\n--- UVM Report catcher Summary ---\n\n\n")
            q.append("Number of demoted UVM_FATAL reports  :{}\n".format(cls.m_demoted_fatal))
            q.append("Number of demoted UVM_ERROR reports  :{}\n".format(cls.m_demoted_error))
            q.append("Number of demoted UVM_WARNING reports:{}\n".format(cls.m_demoted_warning))
            q.append("Number of caught UVM_FATAL reports   :{}\n".format(cls.m_caught_fatal))
            q.append("Number of caught UVM_ERROR reports   :{}\n".format(cls.m_caught_error))
            q.append("Number of caught UVM_WARNING reports :{}\n".format(cls.m_caught_warning))
            #`uvm_info_context("UVM/REPORT/CATCHER",`UVM_STRING_QUEUE_STREAMING_PACK(q),UVM_LOW,uvm_top)

