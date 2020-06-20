module clkd(input CLK,output  DCLK, output PCLK);     //Clock divider
	reg [24:0] temp = 25'd0;
	always @(posedge CLK)
	begin
		temp <= temp + 1'b1;
	end
	assign DCLK = temp[24];
	assign PCLK = temp[21];
endmodule




module design_lab   (
out ,  // Output of the counter
CLK       
);

output out;
reg [3:0] i=0;
reg [1:0] count=0;
//reg f=0;
input CLK;
reg out;
reg [2:0] temp;
wire linear_feedback;

assign linear_feedback = (temp[0] ^ temp[2]);    //PRBS generation
clkd c1(CLK, CLK1, CLK2);



always @(posedge CLK1) begin
 $display("%b",out);
 
if(i!=4'b1010) begin                            //for 10 bit quantization

/*if (reset) begin // active high reset
  temp = 3'b0 ;
  out=1'b0;
end*/
if(!temp) temp=3'b111;
else begin
  temp = {temp[1],temp[0],linear_feedback};
  out=temp[2]^CLK1; 
  end
  
  i<=i+1;
end
  
else begin
case(count)
2'b00: out=1'b1;                             //Adding end bit(here 1111)
2'b01: out=1'b1;
2'b10: out=1'b1;
2'b11: begin out=1'b1;i<=0;end
endcase
count<=count+1;
end
  
end

endmodule 

