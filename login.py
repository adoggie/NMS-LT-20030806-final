

import sys
sys.path.append('.')

from Tix import *
from tktable import *
import time
import SimpleDialog
import Pmw 
import shelve
import ado
import tkMessageBox
import re

import log
import user
import config
import session


class Login(Pmw.MegaToplevel):
		
	def __init__(self,master):		
		Pmw.MegaToplevel.__init__(self,master)
		self.hull = self.component('hull')
		f = Frame(self.hull)
		f.pack(pady=10,padx=10)
		
		self.master = master	#�������������
		
		self.user = Pmw.EntryField(f,labelpos='w',label_text=unicode(' �� ��:'),validate={'max':15,'validator':'alphabetic'})
		self.user.pack(pady=4)
		self.psw = Pmw.EntryField(f,labelpos='w',label_text=unicode(' �� ��:'),validate={'max':15,'validator':'alphanumeric'})
		self.psw.component('entry').config(show='*')
		self.psw.pack(pady=4)
		self.dbserver= Pmw.EntryField(f,labelpos='w',label_text=unicode('���ݿ������:'),validate={'max':15})
		self.dbserver.pack(pady=4)
		Pmw.alignlabels((self.user,self.psw,self.dbserver))
	

		f = Frame(f)
		f.pack(pady=2)
		
		Button(f,command=self.login,text=unicode('��¼')).grid(column=0,row=0,padx=4)
		Button(f,text=unicode('�ر�'),command=lambda:self.destroy()).grid(column=1,row=0,padx=4)
		
		
		self.user.focus_set()
		
		self.hull.title(unicode('NMS1900����ϵͳ--ϵͳ��¼'))
		self.hull.resizable(0,0)		
		
		
		self.user.setvalue("admin")
		self.psw.setvalue("admin")
		
		db = shelve.open(session.sys_config_file)
		server = db['dbserver']
		self.dbserver.setentry(server)
		
		
	def login(self):
		u = self.user.getvalue().strip()
		p = self.psw.getvalue().strip()
		session.login_ok=0
		try:			
			session.dbcnnstr =session.dbcnnstr_template% self.dbserver.getvalue()			
			session.dbcnn =None
			session.dbcnn = ado.PAdo(session.dbcnnstr)
			
			rs  = session.dbcnn .Select('select * from userinfo')
			#print session.dbcnnstr
			while not rs.EOF:
				usr = rs.Fields.Item('LOGIN_NAME').Value
				psw = rs.Fields.Item('PSW').Value					
					
				
				if u==string.strip(usr) and p==string.strip(psw):
					print '================�û�У��ͨ����ע���û�����============================='	
					
					db = shelve.open(session.sys_config_file)
					db['dbserver']=self.dbserver.getvalue()
					
					
					#�Ǽǵ�ǰ��½�û�
					session.user = user.User(str(rs.Fields.Item('ID').Value))	
					
					session.login_ok=1
					log.recLogin()	#��¼��½��־
					print "sessoin.user		"
					
					break
				rs.MoveNext()
			if session.login_ok==0:
				tkMessageBox.showwarning('',unicode('������û������¼���룡'))
			else:
				self.destroy()
				
		except:
			session.login_ok=0
			tkMessageBox.showwarning('',unicode('������������ʧ�ܣ��������ò���!'))
			
			
		
		
		
		
		
		
		
