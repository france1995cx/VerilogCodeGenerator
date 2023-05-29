module USER_SUB_SYS #(parameter pADDR_WIDTH = 12,
                      parameter pDATA_WIDTH = 32)
(
	input wire [pADDR_WIDTH-1:0] a_ls_araddr,
	input wire a_ls_arvalid,
	input wire [pADDR_WIDTH-1:0] a_ls_awaddr,
	input wire a_ls_awvalid,
	input wire [pDATA_WIDTH-1:0] a_ls_wdata,
	input wire a_ls_wstrb,
	input wire a_ls_wvalid,
	input wire a_lsrready,
	input wire a_sm_tready,
	input wire [pDATA_WIDTH-1:0] a_ss_tdata,
	input wire [2:0] a_ss_tid,
	input wire a_ss_tkeep,
	input wire a_ss_tlast,
	input wire [3:0] a_ss_tstrb,
	input wire a_ss_tvalid
	output wire a_ls_arready,
	output wire a_ls_awready,
	output wire [pDATA_WIDTH-1:0] a_ls_rdata,
	output wire a_ls_rvalid,
	output wire a_ls_wready,
	output wire [pDATA_WIDTH-1:0] a_sm_tdata,
	output wire [2:0] a_sm_tid,
	output wire a_sm_tkeep,
	output wire a_sm_tlast,
	output wire [3:0] a_sm_tstrb,
	output wire a_sm_tvalid,
	output wire a_ss_tready,
	output wire hi_pri_req,
	output wire [63:0] la_data,
	output wire user_irq
);

endmodule //USER_SUB_SYS

