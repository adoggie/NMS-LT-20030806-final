

from Tix import *
import Pmw
import constdef
import login
import ado
import session
import user
import tkMessageBox
#############################################################################


class NetCenterInfo(Pmw.MegaToplevel):
	''' ����������Ϣ '''
	def __init__(self,master):
		Pmw.MegaToplevel.__init__(self,master)
		self.master = master
		tp = self.component('hull')
		
		
		tp.title(unicode('����������Ϣ'))
		########################################################
		#������
		frmtitle =Frame(tp)
		frmtitle.pack(side='top')
		#Label(frmtitle,text=unicode('����������Ϣ'),font=('����',16)).pack(pady=10)
		########################################################3
		#���ؾ������
		f = Frame(tp)

		f.pack(fill='both',expand=1)
		##############################################################
		
		self.netcentername=None
		self.addr = None
		self.man = None
		self.manaddr = None
		self.tel = None		
		self.labels=[ 
				 [ 'NAME',unicode('������������'),self.netcentername],
				 [ 'ADDR',unicode('�������ĵ�ַ'),self.addr ],
				 [ 'LINKMAN', unicode('��ϵ������'),self.man],
				 [ 'LINKADDR', unicode('��ϵ�˵�ַ'),self.manaddr],
			     [ 'LINKTEL',unicode('��ϵ�绰'),self.tel] 
			   ] 
		entries=[]
		self.netcentername = Pmw.EntryField(f,labelpos='w',label_text=unicode('������������'),labelmargin=10,validate={'max':50} )
		self.netcentername.pack(fill='x',padx=10,pady=2,expand=1)		
		entries.append(self.netcentername)
		
		self.addr = Pmw.EntryField(f,labelpos='w',label_text=unicode('�������ĵ�ַ'),labelmargin=10,validate={'max':50} )
		self.addr.pack(fill='x',padx=10,pady=2,expand=1)		
		entries.append(self.addr)

		self.man = Pmw.EntryField(f,labelpos='w',label_text=unicode('��ϵ������'),labelmargin=10,validate={'max':50} )
		self.man.pack(fill='x',padx=10,pady=2,expand=1)		
		entries.append(self.man)

		self.manaddr = Pmw.EntryField(f,labelpos='w',label_text=unicode('��ϵ�˵�ַ'),labelmargin=10,validate={'max':50} )
		self.manaddr.pack(fill='x',padx=10,pady=2,expand=1)		
		entries.append(self.manaddr)

		self.tel = Pmw.EntryField(f,labelpos='w',label_text=unicode('��ϵ�绰'),labelmargin=10,validate={'max':50} )
		self.tel.pack(fill='x',padx=10,pady=2,expand=1)		
		entries.append(self.tel)
		 		
		Pmw.alignlabels(entries,'e')
		
		###########################
		f = Frame(tp)
		f.pack(side ='bottom',fill='x',pady=10,padx=10)
		Button(f,text=unicode('�� ��'),command=lambda:self.destroy()).pack(side='right')		
		if session.user.has_rights(user.R_NETCENTER_SET):
			Button(f,text=unicode('�洢'),command = self.onsave).pack(side='right')
		
		
		self.load()		
		
	####################################################################
	def load(self):
		'''ˢ������  '''
		rs = session.getdata('select * from nmsinfo')		
		if rs ==[]:
			return
		item = rs[0]
		self.netcentername.setentry(item['NAME'])
		self.addr.setentry(item['ADDR'])
		self.man.setentry(item['LINKMAN'])
		self.manaddr.setentry(item['LINKADDR'])
		self.tel.setentry(item['LINKTEL'])		
	####################################################################
	def onsave(self):
		''' �޸����ݡ�'''		
		stm1 =None
		fields=[]
		occupysign =[]
		sql = 'insert into nmsinfo(NAME,ADDR,LINKMAN,LINKADDR,LINKTEL) values(:NAME,:ADDR,:LINKMAN,:LINKADDR,:LINKTEL)'
		data=[]
		rs = session.getdata('select count(*) as cnt from nmsinfo')
		cnt = rs[0]['CNT']
		if cnt !=0 :
			sql = 'update nmsinfo set NAME=:NAME,ADDR=:ADDR,LINKMAN=:LINKMAN,LINKADDR=:LINKADDR,LINKTEL=:LINKTEL'
		data.append(['NAME',self.netcentername.getvalue().strip()])			
		data.append(['ADDR',self.addr.getvalue().strip()])			
		data.append(['LINKMAN',self.man.getvalue().strip()])			
		data.append(['LINKADDR',self.manaddr.getvalue().strip()])			
		data.append(['LINKTEL',self.tel.getvalue().strip()])
					
		try:
			session.dbcnn.Execute2(sql,data)				
		except:			
			tkMessageBox.showinfo(unicode('����!'),unicode('�����޸�ʧ��!'))
			return 
		
		tkMessageBox.showinfo(unicode('��ʾ!'),unicode('�����޸ĳɹ�!'))
		
			
				
		
		
		
