library ieee ;
use ieee.std_logic_1164.all ;

entity d_flip_flop is
	generic (NB_BITS : natural := 8);
	port(
		reset_n : in std_logic ;	
		clk		: in std_logic ;
		sreset  : in std_logic ;
		input	: in std_logic_vector(NB_BITS-1 downto 0) ;
		output	: in std_logic_vector(NB_BITS-1 downto 0)
	);
end entity ;

architecture rising_edge_ff of d_flip_flop is
begin

	process(reset_n, clk) ;

	begin
		if reset_n = '0' then
			output <= (others => '0');
		elsif rising_edge(clk) then		-- all bits to 0
			output <= input ;
		end if ;
	end process ;

end rising_edge_ff ;