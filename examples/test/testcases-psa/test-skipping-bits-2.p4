#include <core.p4>
#include <psa.p4>
#include "../../include/std_headers.p4"

header dummy_t {
    bit<8> f8;
}

struct empty_metadata_t {
}

struct metadata {
}

struct headers {
    dummy_t dummy;
}
parser IngressParserImpl(packet_in packet,
                         out headers hdr,
                         inout metadata meta,
                         in psa_ingress_parser_input_metadata_t istd,
                         in empty_metadata_t resubmit_meta,
                         in empty_metadata_t recirculate_meta) {
    state start {
        packet.extract<dummy_t>(_);
        packet.advance(2*8);
        packet.extract(hdr.dummy);
        transition accept;
    }
}

control egress(inout headers hdr,
               inout metadata meta,
               in    psa_egress_input_metadata_t  istd,
               inout psa_egress_output_metadata_t ostd)
{
    apply {
       hdr.dummy.f8 = hdr.dummy.f8 + 1;
    }
}

control IngressDeparserImpl(packet_out buffer,
                            out empty_metadata_t clone_i2e_meta,
                            out empty_metadata_t resubmit_meta,
                            out empty_metadata_t normal_meta,
                            inout headers hdr,
                            in metadata meta,
                            in psa_ingress_output_metadata_t istd)
{
    apply {
        buffer.emit(hdr.dummy);
    }
}

#include "psa-testcase-dummy-pipeline.p4"
