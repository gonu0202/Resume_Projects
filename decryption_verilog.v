module receiver(
in,CLK,ot);
input in;
input CLK;
output reg ot;
reg detector_out=0,f=0;
reg [2:0] current_state, next_state=3'b000; // current state and next state

parameter  Zero=3'b000, // "Zer0" State
  One=3'b001, // "One" State
  OneOne=3'b011, // "OneOne" State
  OneOneOne=3'b101, // "OneOneOne" State
  OneOneOneOne=3'b110;// "OneOneOneOne" State

reg [3:0] count=0;
reg [1:0] c1=0;
reg [2:0] temp;
clkd c2(CLK, CLK1, CLK2);


wire linear_feedback;
assign linear_feedback = (temp[0] ^ temp[2]);

always @(posedge CLK1) begin
	
	if(!f)
	current_state <= next_state; // otherwise, next state
end
	
	// combinational logic of the Moore FSM
	// to determine next state 
	
always @(current_state,in)begin
	
	if(!f) begin
	
	case(current_state) 
	Zero:begin
	if(in==1)
   		next_state <= One;
	else
		next_state <= Zero;
	end
	
	One:begin
	if(in==1)
		next_state <= OneOne;
	else
   		next_state <= Zero;
	end
	
	OneOne:begin
  	if(in==0)
   		next_state <= Zero;
  	else
   		next_state <= OneOneOne;
	end 
 
	OneOneOne:begin
  	if(in==0)
   		next_state <= Zero;
  	else
   		next_state <= OneOneOneOne;
	end
 
 default:next_state <= Zero;
 endcase
 
 end
end

// combinational logic to determine the output
// of the Moore FSM, output only depends on current state

always @(current_state) begin 

if(!f) begin
 case(current_state) 
 Zero:   detector_out <= 0;
 One:   detector_out <= 0;
 OneOne:  detector_out <= 0;
 OneOneOne:  detector_out <= 0;
 OneOneOneOne: begin detector_out <= 1;f=1; end
 default:  detector_out <= 0;
 endcase
 
end
end 
	
	
	
always @(posedge CLK1) begin

	if(detector_out) begin
	if(count != 4'b1010) begin
		if(!temp) temp=3'b111;
		else begin
			temp = {temp[1],temp[0],linear_feedback};
			//prbs_out=temp[2]; 
		end
		ot=in^temp[2];
		count=count+1;
	end
	
	else begin
		if(c1!=2'b11) begin
			c1 = c1+1;
		end
		else begin
			count=4'b0000;
			c1=0;
		end
	end
	end
	
end
endmodule

