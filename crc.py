


r=0xffff
data ='fsafd'
def _xor(c):
	r = r^c
	for i in range(8):
		r = r>>1
		if r&1:
			r= r^0x1021

if __name__=='__main__'			:
	
	for i in data:
		print i
		#_xor(oct(i))
	print hex(r)
	 	 