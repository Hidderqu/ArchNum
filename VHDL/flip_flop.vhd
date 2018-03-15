library ieee ;
use ieee.std_logic_1164.all ;

entity d_flip_flop is
	port(
		clk		: in std_logic ;
		input	: in std_logic ;
		output	: in std_logic
	);
end entity ;

architecture rising_edge_ff of d_flip_flop is
begin

	process(clk) ;

	begin
		if rising_edge(clk) then
			output <= input ;
		end if ;
	end process ;

end rising_edge_ff ;