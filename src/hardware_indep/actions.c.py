# SPDX-License-Identifier: Apache-2.0
# Copyright 2016 Eotvos Lorand University, Budapest, Hungary

from compiler_log_warnings_errors import addError, addWarning
from utils.codegen import format_declaration, format_statement, format_expr, format_type, get_method_call_env
from compiler_common import types, unique_everseen

#[ #include <unistd.h>

#[ #include "dpdk_lib.h"
#[ #include "actions.h"
#[ #include "util_debug.h"
#[ #include "util_packet.h"

#[ extern ctrl_plane_backend bg;

################################################################################


#[ #define STD_DIGEST_RECEIVER_ID 1024

# TODO make it unique by digest name
for mcall in hlir.all_nodes.by_type('MethodCallStatement').map('methodCall').filter(lambda n: 'path' in n.method and n.method.path.name=='digest'):
    digest = mcall.typeArguments[0]
    funname = f'{mcall.method.path.name}__{digest.path.name}'

    #{ ${format_type(mcall.urtype)} $funname(uint32_t /* ignored */ receiver, ctrl_plane_digest cpd, SHORT_STDPARAMS) {
    #[     debug(" " T4LIT(<<<<,outgoing) " " T4LIT(Sending digest,outgoing) " to port " T4LIT(%d,port) " using extern " T4LIT(extern_Digest_pack,extern) " for " T4LIT(cpd,extern) "\n", STD_DIGEST_RECEIVER_ID);

    #[    /* ctrl_plane_digest cpd = create_digest(bg, "digest");

    for fld in digest.urtype.fields:
        if fld.urtype.size > 32:
            #[     dbg_bytes(digest.${fld.name}, (${fld.urtype.size}+7)/8, "       : $[field]{fld.name}/" T4LIT(${fld.urtype.size}) " = ");
            #[     add_digest_field(cpd, digest.${fld.name}, ${fld.urtype.size});
        else:
            #[     debug("       : " T4LIT(ingress_port,field) "/" T4LIT(${fld.urtype.size}) " = " T4LIT(%x) "\n", digest.${fld.name});
            #[     add_digest_field(cpd, &(digest.${fld.name}), ${fld.urtype.size});
    #[ */
    #{ #ifdef T4P4S_P4RT
    #[        // dev_mgr_send_digest(dev_mgr_ptr, (struct p4_digest*)(((Digest_t*)cpd)->ctrl_plane_digest), STD_DIGEST_RECEIVER_ID);
    #} #endif
    #[     send_digest(bg, cpd, STD_DIGEST_RECEIVER_ID);
    #[     //sleep_millis(DIGEST_SLEEP_MILLIS);
    #} }
    #[


#{ void do_assignment(header_instance_t dst_hdr, header_instance_t src_hdr, SHORT_STDPARAMS) {
#{     if (likely(is_header_valid(src_hdr, pd))) {
#{         if (unlikely(!is_header_valid(dst_hdr, pd))) {
#[             activate_hdr(dst_hdr, pd);
#}         }
#[         memcpy(pd->headers[dst_hdr].pointer, pd->headers[src_hdr].pointer, hdr_infos[src_hdr].byte_width);
#[         dbg_bytes(pd->headers[dst_hdr].pointer, hdr_infos[src_hdr].byte_width, "    : Set " T4LIT(%s,header) "/" T4LIT(%dB) " = " T4LIT(%s,header) " = ", hdr_infos[dst_hdr].name, hdr_infos[src_hdr].byte_width, hdr_infos[src_hdr].name);
#[     } else {
#[         debug("   :: Set header " T4LIT(%s,header) "/" T4LIT(%dB) " = " T4LIT(invalid,status) " from " T4LIT(%s,header) "/" T4LIT(%dB) "\n", hdr_infos[dst_hdr].name, hdr_infos[dst_hdr].byte_width, hdr_infos[src_hdr].name, hdr_infos[src_hdr].byte_width);
#[         deactivate_hdr(dst_hdr, pd);
#}     }
#} }
#[


#{ char* action_names[] = {
for table in hlir.tables:
    for action in unique_everseen(table.actions):
        #[     "${action.action_object.name}",
#} };
#[

#{ char* action_canonical_names[] = {
for table in hlir.tables:
    for action in unique_everseen(table.actions):
        #[     "${action.action_object.canonical_name}",
#} };
#[

#{ char* action_short_names[] = {
for table in hlir.tables:
    for action in unique_everseen(table.actions):
        #[     "${action.action_object.short_name}",
#} };
#[

for ctl in hlir.controls:
    for act in ctl.actions:
        name = act.annotations.annotations.get('name')
        if name:
            #[ // action name: ${name.expr[0].value}
        #{ void action_code_${act.name}(action_${act.name}_params_t parameters, SHORT_STDPARAMS) {
        if len(act.body.components) != 0:
            #[     control_locals_${ctl.name}_t* local_vars = (control_locals_${ctl.name}_t*) pd->control_locals;

            for stmt in act.body.components:
                global pre_statement_buffer
                global post_statement_buffer
                pre_statement_buffer = ""
                post_statement_buffer = ""

                code = format_statement(stmt, ctl)
                if pre_statement_buffer != "":
                    #= pre_statement_buffer
                    pre_statement_buffer = ""
                #= code
                if post_statement_buffer != "":
                    #= post_statement_buffer
                    post_statement_buffer = ""
        #} }
        #[
