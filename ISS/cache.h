#define OFFSET_BITS 4 //(int)pow(2,2)
#define SET_BITS 64 //(int)pow(2,6)
#define TAG_BITS 2


typedef struct addr_sliced {
	int set;
	int tag;
	int offset;
} addr_sliced;


typedef struct line {
	int set;
	int valid;
	int tag;
	int bloc[OFFSET_BITS];
} line;


typedef struct Cache {
	line memoire[SET_BITS];
} Cache;


Cache ini_cache();
addr_sliced slice_addr(int addr);
void write_to_cache(addr_sliced addr);
void is_in_cache(addr_sliced addr);
int get_from_cache(int addr);
