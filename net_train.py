


from Tix import *
import Pmw
import tkMessageBox
import re
import string 
import ado
#tcp 数据传输

import constdef
from socket import *
import session



def send2mss(tcp_str):
	try:
		s ="NMS20022"
		print session.mss_addr,session.mss_listen_port
		s ="%s%04d%s"%(s,len(tcp_str),tcp_str)
#		print '>>>>>>>>>>>>>>>>>>'
		print s
		#return 1
#		print '^^^^^^^^^^^^^^^^^^^^^^^^^'
		sk = socket(AF_INET,SOCK_STREAM)
		sk.connect((session.mss_addr,session.mss_listen_port))
		sk.send(s)
		
		sk.close()
		return 1
	except:
		print "socket eror"
		return 0
	
def getlocalip():	
	return gethostbyname(gethostname())
	

#显示正在发送的命令
class net_send_status(Toplevel):
	def __init__(self,master):
		Toplevel.__init__(self,master)
		self.option_add('*Font',('宋体',10))
		self.title(unicode('命令队列'))
		self.shl = ScrolledHList(self,scrollbar='auto', options='hlist.columns 5 hlist.header 1')
		self.shl.pack(fill='both',expand=1,padx=6, pady=6)
		self.hlist = self.shl.hlist
		#self.hlist.column_width(3,0)
		self.hlist.config(separator='.', width=25, drawbranch=0)
#		self.hlist.column_width(0, chars=20)
#		self.hlist.column_width(1, chars=12)
#		self.hlist.column_width(2, chars=8)
#		self.hlist.column_width(3, chars=20)
		
		self.hlist.header_create(0, itemtype='text', text=unicode('类 别'))
		self.hlist.header_create(1, itemtype='text', text=unicode('设 备'))
		self.hlist.header_create(2, itemtype='text', text=unicode('事务号'))
		self.hlist.header_create(3, itemtype='text', text=unicode('响应时间'))
		self.hlist.header_create(4, itemtype='text', text=unicode('当前状态'))
		
		
		self.wm_protocol("WM_DELETE_WINDOW", lambda : self.onclose())	
		self.wait_trans=[]
		
	def onclose(self):
		session.form_send_status=None
		self.destroy()
		
	def add_item(self,trans_no):
		''' trans -> string '''
		self.wait_trans.append(trans_no)
		
		self.lift()
		self.geometry('600x200')
		p = str(trans_no)
		self.hlist.add(p,at=0,itemtype='text',text='')
		self.hlist.item_create(p,1,itemtype='text',text='')
		self.hlist.item_create(p,2,itemtype='text',text='')
		self.hlist.item_create(p,3,itemtype='text',text='')
		self.hlist.item_create(p,4,itemtype='text',text='')
		self.get_current_status(p)
		self.after(session.send_cmd_fresh_interval*1000,self.ontimer)
		pass
		
	def ontimer(self):
		print 'timer out!'
		for i in self.wait_trans:
			self.get_current_status(str(i))
			
		self.after(session.send_cmd_fresh_interval*1000,self.ontimer)
		
		
	def get_current_status(self,path):
		sql="select a.*,b.TRANSACTIONSTATUS,b.settime,b.result  ,c.DESCRIPT  from operateinfo a ,transactionstatus b ,action_type c where a.transactionno = b.transactionno and a.ACTIONID= c.ACTIONID and b.transactionno=%s"%path				
		
		rs = session.getdata(sql) 
		
		
		if len(rs)==0:
			#print 'non record'
			return 
		rs = rs[0]
		self.hlist.item_configure(path,0,text=rs['DESCRIPT'].strip())
		self.hlist.item_configure(path,2,text=rs['TRANSACTIONNO'])
		time = rs['SETTIME']
		if time!=None:
			time = time.Format('%Y-%m-%d %H:%M:%S')
			self.hlist.item_configure(path,3,text=time)
		status = rs['TRANSACTIONSTATUS']
		try:
			status = constdef.transfer_status[str(status)]	
		except:
			status=""

		result = rs['RESULT']
		
		if result!=None:
			status+= constdef.errors[str(result)]
		self.hlist.item_configure(path,4,text=status)
		for i in session.user.repeaters:
			if i['ID']==int(rs['TARGET']):
				devtitle = session.getdevtitle(i)
				self.hlist.item_configure(path,1,text=devtitle)
				break
		
		
		pass
	
if __name__=='__main__':
	rt = Tk()
	session.dbcnn = ado.PAdo(session.dbcnnstr)

	nss = net_send_status(rt)
	nss.add_item(3562)
	
	rt.mainloop()
	