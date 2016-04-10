import sys
sys.path.append("./Lib/site-packages/win32")

from Tix import *

import time
import SimpleDialog
import Pmw

import shelve
import os
import re
#--------------------------
import constdef
import login
import ado
import session
import config
import webbrowser

from systemset import *	 #pane sets

from netcenter import *
from user import *
import login
import log_query
from devinfo import *

wininfo={'title':unicode('���Դ���'),'geometry':'400x400+2+2'}
winoption={'*Button.background':'gray'}


	


		
#############################################################################
class MainFrame(Pmw.MegaToplevel):
	def __init__(self,master):
		Pmw.MegaToplevel.__init__(self,master)
		
		self.master = master
		self.tp = self.component('hull')
		self.tp.title(session.app_title)
		#self.createwidgets()
		self.createMenu()
		self.createToolbar()
		self.createStatusbar()
		self.create_subs()
		self.tp.wm_protocol("WM_DELETE_WINDOW", lambda : self.onclose())
		#self.component('hull').geometry('%sx%s'%(self.master.winfo_screenwidth(),self.master.winfo_screenheight()))
		self.component('hull').geometry('800x500')
	def onclose(self):
		sys.exit(0)
		
	def createStatusbar(self):
		self.fstatus = Frame(self.tp,borderwidth=2,relief='groove')
		self.fstatus.pack(side='bottom',fill='x',padx=10)
		self.timer = Label(self.fstatus)
		self.timer.pack(side='right')
		Label(self.fstatus,text=unicode('����Ա:')+session.user.real_name).pack(side='left')
		
		self.after(1000*2,self.ontimer)
		pass
	def ontimer(self):
		self.timer.config(text=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()))
		self.after(1000*2,self.ontimer)
		
	def createToolbar(self):
		pass
		
	def create_subs(self):
		self.context_frame = Frame(self.component('hull'))
		self.context_frame.pack(fill='both',expand=1)
		self.tab = NoteBook(self.context_frame)
		self.tab.nbframe.config(relief='sunken')
		self.tab.pack(fill='both',expand=1,padx=10,pady=4)
		p1 = self.tab.add('devinfo',label=unicode('�豸����'))
		p2 = self.tab.add('loginfo',label=unicode('��־����'))
		
		pdm = PaneDeviceMgr(p1)	
		pdm.pack(fill='both',expand=1)
		
		lq = log_query.PaneLogQuery(p2)
		lq.pack(fill='both',expand=1)

		
		
	
	
	def createMenu(self):
		self.tp = self.interior()
		
	 	self.menuBar = Pmw.MainMenuBar(self.tp)	
	 	self.menuBar.component('hull').config(relief='raise')
	 	self.menuBar.addmenu(unicode('ϵ ͳ'),'')
	 	self.menuBar.addmenuitem(unicode('ϵ ͳ'), 'command',label = unicode('��������'),command=self.onshownetcenter)
	 	#self.menuBar.addmenuitem(unicode('ϵ ͳ'), 'command',label = unicode('MSS ͳ��'))
	 	#self.menuBar.addmenuitem(unicode('ϵ ͳ'), 'command',label = unicode('CSS ͳ��'))	 	
	 	
	 	self.menuBar.addmenuitem(unicode('ϵ ͳ'), 'command',label = unicode('ϵͳ����'),command=self.sysconfig)
	 	
	 	self.menuBar.addmenuitem(unicode('ϵ ͳ'), 'separator')
	 	self.menuBar.addmenuitem(unicode('ϵ ͳ'), 'command',label = unicode('�� ��'),command=self.onclose)
	 	
	 	
	 	self.menuBar.addmenu(unicode('�� ��'),'')
	 	if session.user.has_rights(R_USER_MANAGE):
	 		self.menuBar.addmenuitem(unicode('�� ��'), 'command',label = unicode('�˺Ź���'),command=self.care_user)
	 	if session.user.has_rights(R_USER_CHANGE_PSW):
	 		self.menuBar.addmenuitem(unicode('�� ��'), 'command',label =unicode('��¼�����޸�'),command=self.changepsw)
	 	self.menuBar.addmenu(unicode('�� ��'),'')
#	 	self.menuBar.addmenuitem(unicode('�� ��'), 'command',label =unicode('���͸澯ʹ�ܱ�־'))
		
	 	self.menuBar.addmenuitem(unicode('�� ��'), 'command',label =unicode('�澯�������� '),command=self.on_warninglevel_set)

#	 	self.menuBar.addmenu(unicode('�� ��'),'')
#	 	self.menuBar.addmenuitem(unicode('�� ��'), 'command',label =unicode('�����豸'),command=self.on_warninglevel_set)

	 	self.menuBar.addmenu(unicode('�� ��'),'')
	 	self.menuBar.addmenuitem(unicode('�� ��'), 'command',label =unicode('ʹ�òο� '),command=self.onhelp)
	 	self.menuBar.addmenuitem(unicode('�� ��'), 'separator')	 	
	 	self.menuBar.addmenuitem(unicode('�� ��'), 'command',label =unicode('����NMS1900����ϵͳ'),command=self.onabout)
	 	
	 	
	 	
	 	
	 	
	 	
	 	
	 	self.tp.configure(menu = self.menuBar)
	 	self.menuBar.component('hull').config(background='green')
	 	
	def on_warninglevel_set(self):
		PaneWarningLevel(self.component('hull'))
			
	def onshownetcenter(self):
		nci = NetCenterInfo(self.component('hull'))
		nci.activate()
		
	def changepsw(self):
		pcp = PaneChangePsw(self.component('hull'))
		pcp.show_user(session.user)
		pcp.activate()
	
	#ϵͳ��������
	def sysconfig(self):
		config.config(self.tp)
			
	def onhelp(self):
		webbrowser.open_new(unicode('./help/NMS1900ֱ��վ����ϵͳ�û��ֲ�.htm'))			
				
	
	def care_user(self):
		''' �û���Ϣά��'''
		#Toplevel()
		tp = Toplevel()
		tp.title(unicode('�û��˺Ź���'))
		pcu = PaneCareUser(tp)
		pcu.pack()
		
		
	def onabout(self):
#		tp = Toplevel(self.tp)
#		global pi
#		pi = PhotoImage(file='./rc/app.gif')
#		f = Frame(tp)
#		f.pack(side,left=padx=10,pady=10)
#		Label(f,
		Pmw.aboutversion('1.0')
		Pmw.aboutcopyright(unicode('Copyright 2003 �Ϻ���������ͨѶ���޹�˾ \n�������а�Ȩ'))
		
		about = Pmw.AboutDialog(self.component('hull'),applicationname =session.app_title)
	
		
		
		
	def createwidgets(self):		
		
		
		self.tb = ToolsBar(self.rt)
		self.tb.config(bg='green',height=20)
		self.tb.pack(fill='x')
		
		
		wa = Frame(self.rt,bg='gray')
		wa.pack(expand=1,fill='both',side='top')
		self.sb = StatusBar(self.rt,height=40)
		self.sb.pack(side='bottom',fill='x')
		
		#�ָ�ڣ���������
		pw1 = PanedWindow(wa,orientation='vertical')
		p1 = pw1.add('up',expand=1)
		
		##��Ϣ��ʾ����
		p2 = pw1.add('msgout',size=100)
		self.createMsgout(p2)
		
		pw1.pack(expand=1,fill='both')
		################################################
		
		pw2 = PanedWindow(p1,orientation='horizontal')
		p3 = pw2.add('leftpane',size=240)
		p4 = pw2.add('detailpane')		
		pw2.pack(fill='both',expand=1)
		##p3 --����ѡ����
		##p4 --��Ϣ��ʾ����
		self.devlist = PaneListDevice(p4)
		
		
		##�豸״̬�澯��
		self.ws = WarningStatus(p3)		
		self.ws.pack(side='bottom',fill='x')	
		
		
		
	def createMsgout(self,pane):	
		'''��Ϣ��ʾ���岿��'''
		self.msgout = ScrolledListBox(pane,relief='groove',scrollbar='auto')		
		self.msgout.pack(fill='both',expand=1)
		self.msgout.listbox.insert('end',time.asctime() +unicode('-- ��ӭʹ��NMS1900����ϵͳ --'))
		
		
		
		
	def mainloop(self):
		self.rt.mainloop()
		

	
if __name__ == "__main__":

	#�����������Ϣ
	rt = Tk()
	session.root = rt
	rt.option_add('*Font',('����',10))
	#rt.option_add('*Button.background','gray')
	#rt.option_add('*Button.relief','groove')
	
	rt.wm_withdraw()
	#clear temp report file
	try:		
		for i in os.listdir('./cache'):
			os.remove("./cache/%s"%i)
	except:	
		print 'eror'
		pass
	# load runing params
	config.load_run_param()
		
	login = login.Login(rt)	
	login.activate()	
	
	if not session.login_ok:
		sys.exit(0)
	###################################
	#ʱ��ͬ�����ݿ�
	cur_time = session.getdata('select getdate() as T')[0]
	os.system('date %s'%cur_time['T'].Format('%Y-%m-%d'))
	os.system('time %s'%cur_time['T'].Format('%H:%M:%S'))
	###################################
	
	 
	
	session.areas = session.getdata('select * from area')
	session.providers=session.getdata('select * from provider')
	session.products=session.getdata('select * from products')
	session.repeatertype=session.getdata('select * from repeatertype')
	#session.repeaters = session.getdata('select * from repeaterinfo order by name')
	session.users = session.getdata('select * from userinfo ')
	session.current_dev_statuses = session.getdata("select  repeater_id,WARNINGLEVEL,OPTTIME from statusview ")
	session.param_configs = session.getdata("select  * from param_config")

	mf = MainFrame(rt)		
	
	
	rt.mainloop()
	
