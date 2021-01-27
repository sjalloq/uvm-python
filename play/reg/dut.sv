module regfile (
  input wire clk,
  input wire rst_n
);

  reg [31:0] count_q;

  always @(posedge clk or negedge rst_n)
    if (!rst_n)
      count_q <= '0;
    else
      count_q <= count_q + 1;

endmodule


module dut (
  input wire clk,
  input wire rst_n
);

regfile u_reg (.clk (clk), .rst_n (rst_n));

endmodule