module IRQ_MUX #(parameter pADDR_WIDTH = 12,
                 parameter pDATA_WIDTH = 32)
(
	input wire ALCLK,
	input wire ARESET_N,
	input wire [0:0] USER_PRJ_SEL,
	input wire hi_pri_req,
	input wire hi_pri_req,
	input wire hi_pri_req,
	input wire hi_pri_req,
	input wire user_irq,
	input wire user_irq,
	input wire user_irq,
	input wire user_irq
	output wire hi_pri_req,
	output wire user_irq
);

endmodule //IRQ_MUX

