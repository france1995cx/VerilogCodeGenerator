module USER_PRJ #(parameter pADDR_WIDTH = 12,
                  parameter pDATA_WIDTH = 32)
(
	input wire ALCLK,
	input wire ALCLK,
	input wire ALCLK,
	input wire ALCLK,
	input wire ARESET_N,
	input wire ARESET_N,
	input wire ARESET_N,
	input wire ARESET_N,
	input wire ASCLK,
	input wire ASCLK,
	input wire ASCLK,
	input wire ASCLK,
	input wire Arvalid_0,
	input wire USER_CLK2,
	input wire USER_CLK2,
	input wire USER_CLK2,
	input wire USER_CLK2,
	input wire [pDATA_WIDTH-1:0] Wdata,
	input wire [pDATA_WIDTH-1:0] Wdata,
	input wire [pDATA_WIDTH-1:0] Wdata,
	input wire [pDATA_WIDTH-1:0] Wdata,
	input wire [pADDR_WIDTH-1:0] araddr,
	input wire [pADDR_WIDTH-1:0] araddr,
	input wire [pADDR_WIDTH-1:0] araddr,
	input wire [pADDR_WIDTH-1:0] araddr,
	input wire arvalid_1,
	input wire arvalid_2,
	input wire arvalid_3,
	input wire [pADDR_WIDTH-1:0] awaddr,
	input wire [pADDR_WIDTH-1:0] awaddr,
	input wire [pADDR_WIDTH-1:0] awaddr,
	input wire [pADDR_WIDTH-1:0] awaddr,
	input wire awvalid_0,
	input wire awvalid_1,
	input wire awvalid_2,
	input wire awvalid_3,
	input wire rready,
	input wire rready,
	input wire rready,
	input wire rready,
	input wire sm_tready,
	input wire sm_tready,
	input wire sm_tready,
	input wire sm_tready,
	input wire [pDATA_WIDTH-1:0] ss_tdata,
	input wire [pDATA_WIDTH-1:0] ss_tdata,
	input wire [pDATA_WIDTH-1:0] ss_tdata,
	input wire [pDATA_WIDTH-1:0] ss_tdata,
	input wire [2:0] ss_tid,
	input wire [2:0] ss_tid,
	input wire [2:0] ss_tid,
	input wire [2:0] ss_tid,
	input wire ss_tkeep,
	input wire ss_tkeep,
	input wire ss_tkeep,
	input wire ss_tkeep,
	input wire ss_tlast,
	input wire ss_tlast,
	input wire ss_tlast,
	input wire ss_tlast,
	input wire [3:0] ss_tstrb,
	input wire [3:0] ss_tstrb,
	input wire [3:0] ss_tstrb,
	input wire [3:0] ss_tstrb,
	input wire ss_tvalid_0,
	input wire ss_tvalid_1,
	input wire ss_tvalid_2,
	input wire ss_tvalid_3,
	input wire wstrb_0,
	input wire wstrb_1,
	input wire wstrb_2,
	input wire wstrb_3,
	input wire wvalid_0,
	input wire wvalid_1,
	input wire wvalid_2,
	input wire wvalid_3
	output wire arready,
	output wire arready,
	output wire arready,
	output wire arready,
	output wire awready,
	output wire awready,
	output wire awready,
	output wire awready,
	output wire hi_pri_req,
	output wire hi_pri_req,
	output wire hi_pri_req,
	output wire hi_pri_req,
	output wire [63:0] la_data,
	output wire [63:0] la_data,
	output wire [63:0] la_data,
	output wire [63:0] la_data,
	output wire [pDATA_WIDTH-1:0] rdata,
	output wire [pDATA_WIDTH-1:0] rdata,
	output wire [pDATA_WIDTH-1:0] rdata,
	output wire [pDATA_WIDTH-1:0] rdata,
	output wire rvalid,
	output wire rvalid,
	output wire rvalid,
	output wire rvalid,
	output wire [pDATA_WIDTH-1:0] sm_tdata,
	output wire [pDATA_WIDTH-1:0] sm_tdata,
	output wire [pDATA_WIDTH-1:0] sm_tdata,
	output wire [pDATA_WIDTH-1:0] sm_tdata,
	output wire [2:0] sm_tid,
	output wire [2:0] sm_tid,
	output wire [2:0] sm_tid,
	output wire [2:0] sm_tid,
	output wire sm_tkeep,
	output wire sm_tkeep,
	output wire sm_tkeep,
	output wire sm_tkeep,
	output wire sm_tlast,
	output wire sm_tlast,
	output wire sm_tlast,
	output wire sm_tlast,
	output wire [3:0] sm_tstrb,
	output wire [3:0] sm_tstrb,
	output wire [3:0] sm_tstrb,
	output wire [3:0] sm_tstrb,
	output wire sm_tvalid,
	output wire sm_tvalid,
	output wire sm_tvalid,
	output wire sm_tvalid,
	output wire ss_tready,
	output wire ss_tready,
	output wire ss_tready,
	output wire ss_tready,
	output wire user_irq,
	output wire user_irq,
	output wire user_irq,
	output wire user_irq,
	output wire wready,
	output wire wready,
	output wire wready,
	output wire wready
);

endmodule //USER_PRJ

