module AXIS_MSTR #(parameter pADDR_WIDTH = 12,
                   parameter pDATA_WIDTH = 32)
(
	input wire ARESET_N,
	input wire ASCLK,
	input wire [0:0] USER_PRJ_SEL,
	input wire a_sm_tready,
	input wire [pDATA_WIDTH-1:0] sm_tdata,
	input wire [pDATA_WIDTH-1:0] sm_tdata,
	input wire [pDATA_WIDTH-1:0] sm_tdata,
	input wire [pDATA_WIDTH-1:0] sm_tdata,
	input wire [2:0] sm_tid,
	input wire [2:0] sm_tid,
	input wire [2:0] sm_tid,
	input wire [2:0] sm_tid,
	input wire sm_tkeep,
	input wire sm_tkeep,
	input wire sm_tkeep,
	input wire sm_tkeep,
	input wire sm_tlast,
	input wire sm_tlast,
	input wire sm_tlast,
	input wire sm_tlast,
	input wire [3:0] sm_tstrb,
	input wire [3:0] sm_tstrb,
	input wire [3:0] sm_tstrb,
	input wire [3:0] sm_tstrb,
	input wire sm_tvalid,
	input wire sm_tvalid,
	input wire sm_tvalid,
	input wire sm_tvalid
	output wire [pDATA_WIDTH-1:0] a_sm_tdata,
	output wire [2:0] a_sm_tid,
	output wire a_sm_tkeep,
	output wire a_sm_tlast,
	output wire [3:0] a_sm_tstrb,
	output wire a_sm_tvalid,
	output wire sm_tready,
	output wire sm_tready,
	output wire sm_tready,
	output wire sm_tready
);

endmodule //AXIS_MSTR

