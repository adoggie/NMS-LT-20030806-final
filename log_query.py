
##
#  ϵͳ��־����
#
#

from Tix import *
import Pmw
import tkMessageBox
import re
import string 
import time


import constdef
import login
import net_train
import ado
import session
import log
import export
import user


################################################################################
class BlinkButton(Button):
	def __init__(self,master):
		Button.__init__(self,master)
		self.canblink= 0
		
	def setblink(self):
		self.canblink= 1
		pass
	
class PaneLogStatus(Toplevel):
	'''״̬��ʾ���
		����:��ʾ�豸״̬��Ϣ��������ǰ�澯״̬
		�澯״̬��red,green��ɫ��ʾ��ͬʱ��ʾ��ǰ�ظ澯״ֵ̬
		״̬��¼�ṹ����:
												
	'''
	def __init__(self,master):
		self.master = master
		Toplevel.__init__(self,master)		
		#���ݶ���
		self.widgets=[]
		
		self.control_params=[]
		self.id =0
		self.status=[]
		
		fall = Frame(self)
		fall.pack(fill='both',expand=1)
		
		f = Frame(fall)
		f.pack(fill='x',side='top',pady=4)
		self.title = Label(f,text='')
		self.title.pack()
		self.time = Label(f,text='')
		self.time.pack()

		#�������������
		
		
		#tabpanel
		self.nb = NoteBook(fall)
		self.nb.pack(fill='both',side='top',expand=1,padx=10,pady=10)
		self.p1 = self.nb.add('status',label=unicode('״ ̬'))
		
		
		
		#״̬
		f = Frame(self.p1,relief='groove')
		f.pack(fill='x',side='bottom',padx=10,pady=4)

		#��������
		self.sw = ScrolledWindow(self.p1,scrollbar='auto')
		self.sw.pack(fill='both',side='top',expand=1,padx=10,pady=10)

		self.wm_protocol("WM_DELETE_WINDOW", lambda : self.onclose())
		
		self.wm_title(unicode('�豸״̬'))
		
		
	def onclose(self):
		
		self.destroy()
		

	def is_warning(self,param_item,cur_val):
		""" param_item:������¼ 
		cur_val	: ��ǰ��¼ֵ
		���cur_val�Ƿ���param_config->uplimit  downlimit ֮�䣬�����ж�Ϊ�澯(return 1)
		"""
		cur_val = float(cur_val)
		if cur_val >=param_item['UPLIMIT'] and cur_val <=param_item['DOWNLIMIT']:
			return 1
		
		return 0
			
#########################################################################
	#��ʾָ���豸��״̬��Ϣ
	# forlog_status_id -- ����״̬��־��ѯ��״̬��¼ID
	def show_status(self,devid):
		'''����״̬,���ƿؼ�'''
		self.id =  devid
		##################################################################
		for i in self.widgets:
			i.destroy()
			del i
		self.widgets=[]
		
		self.control_widget =[]
		self.control_params=[]
		##################################################################
		
		#��ȡ��ǰ�豸����״̬��¼
		
		sql = 'select * from status where id=%s'%devid	
			
		self.status = session.getdata(sql) 		
		cur_status = self.status
		if len(cur_status) ==0:
			param_status =[]
		else:	
			cur_status =cur_status[0]
		##############################################
		sql = "select * from repeaterinfo where id=%s"%cur_status['REPEATER_ID']	
		devinfo = session.getdata(sql)
		print sql
		title = session.getdevtitle(devinfo[0])
		
		self.title.config(text = title)
		
		row = devinfo[0]
		#param_status = 
		sql = "select * from param_config where repeatertype=%s and is_status=1 and isdisplay=1"%row['REPEATERTYPE']
		param_status = session.getdata(sql)
		#print "get %s object from param_config"%len(param_status)

		
		time=""					
		try:
			time = cur_status['OPTTIME']
			time = time.Format('%Y/%m/%d %H:%M:%S')
		except:
			time=""
		self.time.config(text=time)
		##############################################
			
			
		idx =0
		for i in param_status:
			#print i['PARAMNAME'],i['FIELDNAME']
			row= idx / 2
			column= idx % 2
			if column == 1:
				column = 2	#ͬ�еĵڶ���״̬�����Ų�λ��
#			elif column == 2:
#				column = 4							
			lb = Label(self.sw.window,text=i['DESCRIPT'],anchor='e',relief='groove')
			lb.grid(column = column,row = row,padx=4,pady=2,sticky='e')
			self.widgets.append(lb)
			
			i['PARAMNAME'] =string.strip(i['PARAMNAME'] )
			

			#�����ָ澯ֵ�����е�״ֵ̬�����и澯�Ŀ���
			text=""
			try:
				text =cur_status[i['FIELDNAME']]
			except:
				print 'get value error:SELECT VALUE INVALID!!!! ==> %s'%i['FIELDNAME']
				text ="?"
			
				
			#��ʾ�����ַ�
			if i['UI_TYPE']=='SELECT':	
				try:	
					ls1=[]
					ls1 = re.split(';',i['UI_VALUE_RANGE'])
					for s in ls1:
						ls2 =re.split(':',s)
						
						if int(ls2[1])==int(cur_status[i['FIELDNAME']]):	#
							text = ls2[0]
							break
						else: 
							text ="?"
				except:
					print 'SELECT VALUE INVALID!!!! ==> %s'%i['FIELDNAME']
					
					print "default switch value ==>",text
					
													
			lb = Label(self.sw.window,fg='blue',text=text,relief='raise',borderwidth=2)
			#��⵱ǰֵ�Ƿ�澯
			if self.is_warning(i,str(cur_status[i['FIELDNAME']])):
				lb.config(background='red')
			else:
				lb.config(background='green')
				
				
			lb.grid(column = column+1,row = row,padx=4,pady=2)
			self.widgets.append(lb)		
				
#		##################################################################
#			
			idx+=1
		


########################################################################333

class PaneLogControl(Toplevel):
	'''������ʷ��ʾ���
		����:��ʾ�豸������Ϣ
												
	'''
	def __init__(self,master):
		self.master = master
		Toplevel.__init__(self,master)		
		#���ݶ���
		self.widgets=[]
		self.control_widget=[]	#�û����Ʋ����������ز���
		self.control_params=[]
		self.id =0
		self.status=[]
		
		fall = Frame(self)
		fall.pack(fill='both',expand=1)
		
		f = Frame(fall)
		f.pack(fill='x',side='top',pady=4)
		self.title = Label(f,text='')
		self.title.pack()
		self.time = Label(f,text='')
		self.time.pack()
		#�������������
		
		
		#tabpanel
		self.nb = NoteBook(fall)
		self.nb.pack(fill='both',side='top',expand=1,padx=10,pady=10)
		self.p1 = self.nb.add('status',label=unicode('�� ��'))

		
		
		#״̬
		f = Frame(self.p1,relief='groove')
		f.pack(fill='x',side='bottom',padx=10,pady=4)
		#��������
		self.sw = ScrolledWindow(self.p1,scrollbar='auto')
		self.sw.pack(fill='both',side='top',expand=1,padx=10,pady=10)
		self.wm_protocol("WM_DELETE_WINDOW", lambda : self.onclose())
		
		self.wm_title(unicode('�豸������־'))
		
		
	def onclose(self):
		
		self.destroy()
		
		
#########################################################################		
	#��ʾָ���豸��״̬��Ϣ
	# forlog_status_id -- ����״̬��־��ѯ��״̬��¼ID
	def show(self,control_id):
		'''����״̬'''
		
		##################################################################
		for i in self.widgets:
			i.destroy()
			del i
		self.widgets=[]
		
		for i in self.control_widget:
			i[1].destroy()			
			del i[1]	#ɾ���洢�ģ����������
		self.control_widget =[]
		self.control_params=[]
		##################################################################
		
		#��ȡ��ǰ�豸����״̬��¼
		
		sql = 'select * from control where id=%s'%control_id				
		self.control = session.getdata(sql) 		
		cur_status = self.control

		if len(cur_status) ==0:
			param_status =[]
			return 
		else:	
			cur_status =cur_status[0]

		###################################################################
		# �Ż��ٶ�
		sql = "select * from repeaterinfo where id=%s"%cur_status['REPEATER_ID']
		devinfo = session.getdata(sql)
		title = session.getdevtitle(devinfo[0])
		self.title.config(text = title)
		row = devinfo[0]
		#param_status = 
		sql = "select * from param_config where repeatertype=%s and is_status=1 and is_control=1 and isdisplay=1"%row['REPEATERTYPE']
		param_status = session.getdata(sql)
			
		idx =0
		###################################################################
		for i in param_status:
			row= idx / 2
			column= idx % 2
			if column == 1:
				column = 2	#ͬ�еĵڶ���״̬�����Ų�λ��
#			elif column == 2:
#				column = 4		
			time=""					
			try:
				time = cur_status['OPTTIME']
				time = time.Format('%Y/%m/%d %H:%M:%S')
			except:
				time=""
			self.time.config(text=time)
			
			lb = Label(self.sw.window,text=i['DESCRIPT'],anchor='e',relief='groove')
			lb.grid(column = column,row = row,padx=4,pady=2,sticky='e')
			self.widgets.append(lb)
			
			i['PARAMNAME'] =string.strip(i['PARAMNAME'] )
			try:
				text=""
				try:
					text=cur_status[i['CONTROL_MAP_STATUS']]
				except:
					pass
				
					
				#��ʾ�����ַ�
				if i['UI_TYPE']=='SELECT':	
					text=""
					try:	
						text =constdef.switch[ str(cur_status[i['CONTROL_MAP_STATUS']]) ]	
					except:
						pass
			except:
				text=""												
			lb = Label(self.sw.window,fg='blue',text=text)
			lb.grid(column = column+1,row = row,padx=4,pady=2)
			self.widgets.append(lb)		
				
#		##################################################################
#			
			idx+=1
		
	
#|----------------------------|
#|		|					 |
#|		|--------------------|
#|		|					 |
#|		|					 |
#|		|					 |
#|----------------------------|
class PaneLogQuery(Frame):
	export_title=''
	def __init__(self,master):
		Frame.__init__(self,master)
		self.fall = Frame(self)
		self.fall.pack(fill='both',expand=1,padx=4,pady=4)
		
		sw = PanedWindow(self.fall,orientation='horizontal')
		sw.pack(fill='both',expand=1)
		p1 = sw.add('case',size=200)
		self.p2 = sw.add('result',expand=1)
		
		fleft = Frame(p1)
		fleft.pack(fill='both',expand=1,padx=4,pady=10)
		
		#self.fright = Frame(p2)
		#self.fright.pack(fill='both',expand=1,padx=4,pady=10)
		
		
		#Button(frtop,text='print').pack(pady=10)
		
		#self.frbottom= Frame(fright)
		#self.frbottom.pack(fill='both',expand=1,padx=4)
		
		self.context =None
		
		#
		self.context =None
		
		self.fcase = Frame(fleft)
		self.fcase.pack()

		self.cb_opttype1 = ComboBox(self.fcase,label=unicode('  ����:'),command=self.on_opttype1_sel)
		self.cb_opttype1.pack()
		self.cb_opttype1.append_history(unicode('�豸'))
		self.cb_opttype1.append_history(unicode('����Ա'))
		
		self.cb_opttype2 = ComboBox(self.fcase,label=unicode('  ����:'))
		self.cb_opttype2.pack()
		
		
		
		self.cb_repeaters = ComboBox(self.fcase,label=unicode('  �豸:'),command=self.on_dev_sel)
		#self.cb_repeaters.pack()
		self.cb_repeaters.append_history(unicode('�����豸'))
		for i in session.user.repeaters:			
			self.cb_repeaters.append_history(i['NAME'].strip())
			
		#self.cb_subdev = ComboBox(self.fcase,label=unicode('���豸:'))
		#self.cb_subdev.pack()
		
		self.cb_users= ComboBox(self.fcase,label=unicode('����Ա:'))
		#self.cb_users.pack()
		self.cb_users.append_history(unicode('���й���Ա'))
		for i in session.users:
			self.cb_users.append_history(i['REAL_NAME'].strip())
		
			
				
			
		
		t = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
		self.time1= Pmw.EntryField(self.fcase,labelpos = 'w',label_text = unicode('ʱ����:'),
						value=t)
		
		self.time2= Pmw.EntryField(self.fcase,labelpos = 'w',label_text = unicode('ʱ����:'),
						value=t)
		self.time2.pack(side='bottom')
		self.time1.pack(side='bottom')
		f = Frame(fleft)
		f.pack(fill='x',pady=10)
		self.doquery = Button(f,text=unicode('��ѯ'),command=self.doquery)		
		self.doquery.grid(column=0,row=0)
		self.doprint = Button(f,text=unicode('���'),command=self.onexport)		
		self.doprint.grid(column=1,row=0)
		
		
		self.pwl0 = PhotoImage(file='./rc/salert_0.gif')	
		self.pwl1 = PhotoImage(file='./rc/salert_1.gif')	
		self.pwl2 = PhotoImage(file='./rc/salert_2.gif')	
		self.pwl3 = PhotoImage(file='./rc/salert_3.gif')	
		
		
	def onexport(self):
		''' data export '''
		export.Make2Html(self.export_title,self.context)
		
	#����ѡ��
	def on_opttype1_sel(self,item):
		self.cb_opttype2.slistbox.listbox.delete(0,'end')
		self.cb_opttype2.configure(value='')
		sel = self.cb_opttype1.cget('value')
		if sel==unicode('����Ա'):
			if session.user.has_rights(user.R_LOG_LOGIN):		
				self.cb_opttype2.append_history(unicode('ϵͳ��¼'))
			if session.user.has_rights(user.R_LOG_USER_OPERATION):		
				self.cb_opttype2.append_history(unicode('�������'))
			self.cb_repeaters.forget()
			#self.cb_subdev.forget()
			self.cb_users.pack()

		elif sel==unicode('�豸'):
			if session.user.has_rights(user.R_LOG_STAUTS):		
				self.cb_opttype2.append_history(unicode('״̬'))
			if session.user.has_rights(user.R_LOG_ALARM):		
				self.cb_opttype2.append_history(unicode('�澯'))
			if session.user.has_rights(user.R_LOG_CONTROL):		
				self.cb_opttype2.append_history(unicode('����'))
			self.cb_repeaters.pack()
			#self.cb_subdev.pack()
			self.cb_users.forget()
	
	#ѡ���豸	
	def on_dev_sel(self,item):
		pass
		#sel =self.cb_repeaters.cget('value') 
		#if sel==unicode('�����豸'):
		#	self.cb_subdev.forget()
		#	return 
		#self.cb_subdev.pack()
		#self.cb_subdev.slistbox.listbox.delete(0,'end')
		#self.cb_subdev.append_history(unicode('�������豸'))
		
		#devcat = session.match(session.user.repeaters,"NAME","STRING",sel,"DEVCAT")
		#if devcat ==5:
		#	self.cb_subdev.append_history(constdef.dev_cat['5'])	
		#	self.cb_subdev.append_history(constdef.dev_cat['6'])	
		#elif devcat == 1:
		#	self.cb_subdev.append_history(constdef.dev_cat['1'])	
		#	self.cb_subdev.append_history(constdef.dev_cat['2'])	
		#else:
		#	self.cb_subdev.append_history(constdef.dev_cat[str(devcat)])	
	
	#����ʱ���ַ���		
	def gen_time_str(self,time):
		
		str=''
		if len(time)==3:
			str="%s-%s-%s"%time
		if len(time)==6:
			str="%s-%s-%s %s:%s:%s"%time
		return str
		
		
	#��ѯ
	def doquery(self):
		case1=  self.cb_opttype1.cget('value').strip()
		case2 = self.cb_opttype2.cget('value').strip()
		time1 = re.findall('\s*(\d+)-(\d+)-(\d+)\s+(\d+):(\d+):(\d+)', self.time1.getvalue())
		time2 = re.findall('\s*(\d+)-(\d+)-(\d+)\s+(\d+):(\d+):(\d+)', self.time2.getvalue())
		if len(time1)==0:
			time1 = re.findall('\s*(\d+)-(\d+)-(\d+)\s*', self.time1.getvalue())
			if len(time1)==0:
				tkMessageBox.showwarning(unicode('����!'),unicode('��ѯ��ʼʱ����Ч!'))
				return 
		if len(time2)==0:
			time2 = re.findall('\s*(\d+)-(\d+)-(\d+)\s*', self.time1.getvalue())
			if len(time2)==0:
				tkMessageBox.showwarning(unicode('����!'),unicode('��ѯ����ʱ����Ч!'))
				return 
		time1=  self.gen_time_str(time1[0])
		time2=  self.gen_time_str(time2[0])
		print time1
		print time2

		if case1=='':
			tkMessageBox.showwarning(unicode('����!'),unicode('��ѡ���ѯ����!'))
			return 
		if case2=='':
			tkMessageBox.showwarning(unicode('����!'),unicode('��ѡ���ѯ����!'))			
			return 
		if case1 ==unicode("�豸"):
			dev = self.cb_repeaters.cget('value').strip()
			#subdev = self.cb_subdev.cget('value').strip()
			if dev=='':
				tkMessageBox.showwarning(unicode('����!'),unicode('��ѡ���豸!'))			
				return 
			devids=[]
			if dev!=unicode('�����豸'):				
				masterid = session.match(session.user.repeaters,"NAME","STRING",dev,"ID")
				if masterid==None:
					tkMessageBox.showwarning(unicode('����!'),unicode('�豸�޷�ƥ��!'))			
					return
				
				#if subdev=='':
				#	tkMessageBox.showwarning(unicode('����!'),unicode('��ѡ�����豸!'))			
				#	return 
				#if subdev==unicode('�������豸'):
				#	devids=[]
				#	devids.append(masterid)	#���豸
				#	for i in session.user.repeaters:
				#		if i['PARENT_ID']==masterid:
				#			devids.append(i['ID'])
				#else:
				#	devids=[]
				#	devtype = constdef.dev_cat2[subdev]
				#	if devtype==1 or devtype==3 or devtype==4 or devtype==5 or devtype==7:
				#		devids.append(masterid)	#���豸
				#	else:
				#		for i in session.user.repeaters:							
				#			if i['PARENT_ID']==masterid:
				#				devids.append(i['ID'])
				devids.append(masterid)
				
			else:#==unicode('�����豸'):				
				devids=[]
				for i in session.user.repeaters:
					devids.append(i['ID'])
			########################################################
			searchkey=''
			
			if case2==unicode('״̬'):
				searchkey='repeater_id'	
				ls=[]
				for i in devids:
					ls.append(searchkey+"=%s"%i)
				where1 = string.join(ls," or ")
				where1="("+where1+")"
				sql  = "select * from status where "+where1				
				sql+=" and opttime between '%s' and '%s'"%(time1,time2)
				sql+=" order by opttime desc"
				
				self.showdetail(sql,'status')	
				self.export_title="�豸״̬"
				
			if case2==unicode('�澯'):
				searchkey='repeater_id'	
				ls=[]
				for i in devids:
					ls.append(searchkey+"=%s"%i)
				where1 = string.join(ls," or ")
				where1="("+where1+")"
				sql  = "select * from status where "+where1				
				sql+=" and opttime between '%s' and '%s'"%(time1,time2)
				sql+="  and warninglevel<>0 "
				sql+=" order by opttime desc"				
				self.showdetail(sql,'warning')	
				self.export_title="�豸�澯"					
			if case2==unicode('����'):
				searchkey='repeater_id'	
				ls=[]
				for i in devids:
					ls.append(searchkey+"=%s"%i)
				where1 = string.join(ls," or ")
				where1="("+where1+")"
				sql  = "select a.*,b.transactionstatus,b.settime,b.result  from control a,transactionstatus b  where "+where1				
				sql+=" and opttime between '%s' and '%s'"%(time1,time2)				
				sql+=" and a.transactionno= b.transactionno "
				sql+=" order by opttime desc"	
				
				self.showdetail(sql,'control')										
				self.export_title="�豸����"
				pass
			
			
					
					
					
					
					
		elif case1 ==unicode("����Ա"):
			user = self.cb_users.cget('value')
			if user=='':
				tkMessageBox.showwarning(unicode('����!'),unicode('��ѡ�����Ա!'))			
				return 	
			loginname = session.match(session.users,"REAL_NAME","STRING",user,"LOGIN_NAME")			
			sql = ''
			if case2==unicode('ϵͳ��¼'):
				sql = "select  * from logininfo where "
				if loginname!=None:
					sql +="  username='%s' and "%loginname
					
				sql+="  logintime between '%s' and '%s'"%(time1,time2)
				sql+=" order by logintime desc"
				
				self.showdetail(sql,'login')
				self.export_title="ϵͳ��¼"
						
			if case2==unicode('�������'):
				
				sql = "select a.*,b.descript,c.real_name,d.result from operateinfo a,action_type b,userinfo c ,transactionstatus d "
				sql+=" where a.actionid = b.actionid and a.operator=c.login_name and a.transactionno =d.transactionno"
				if loginname!=None:
					sql +="  and operator='%s' and "%loginname
					
				sql+=" and opttime between '%s' and '%s'"%(time1,time2)
				sql+=" order by opttime desc"
				
				self.showdetail(sql,'usermgr')
				self.export_title="����Ա���� "
			
		pass				
	
			
	def is_warning(self,param_item,cur_val):
		""" param_item:������¼ 
		cur_val	: ��ǰ��¼ֵ
		���cur_val�Ƿ���param_config->uplimit  downlimit ֮�䣬�����ж�Ϊ�澯(return 1)
		"""
		try:
			cur_val = float(cur_val)
		except:
			cur_val =0
			print "covert status value error: the value is invalible (in funcition is_warning)"
		if cur_val >=float(param_item['UPLIMIT']) and cur_val <=float(param_item['DOWNLIMIT']):
			return 1
		
		return 0

	# show query result set	
	def showdetail(self,sql,opttype):
		sql = sql.upper()
		sql =sql.replace("SELECT","SELECT TOP %s"%session.browse_rowsets)
		rs = session.getdata(sql)
		if self.context:
			self.context.destroy()
		fields={}
		if opttype.upper()=='LOGIN':
			#
			
			fields['USERNAME']=unicode('��¼��')
			fields['LOGINIP']=unicode('��¼IP')
			fields['LOGINTIME']=unicode('��¼ʱ��')
			
			cols = len(fields.keys())
			self.context = ScrolledHList(self.p2,scrollbar ='auto',options="hlist.columns %s header 1"%cols)
			self.context.pack(fill='both',expand=1)
			self.hlist = self.context.hlist
			self.hlist.config(separator='.', width=25, drawbranch=0)
			self.hlist.column_width(0, chars=12)
			self.hlist.column_width(1, chars=25)
			self.hlist.column_width(2, chars=25)
			
			ks = fields.keys()
			for k in fields.keys():
				try:
					self.hlist.header_create(ks.index(k),itemtype='text',text=fields[k])					
				except:
					tkMessageBox.showwarning(unicode('����!'),unicode('field name map to  hlist error!'))							
					return
			for r in rs:
				self.hlist.add(r['ID'],itemtype='text',text=r['USERNAME'])
				time = r['LOGINTIME']
				time = time.Format('%Y/%m/%d %H:%M:%S')
				self.hlist.item_create(r['ID'],1,itemtype='text',text=r['LOGINIP'])
				self.hlist.item_create(r['ID'],2,itemtype='text',text=time)
				
				
		if 	opttype.upper()=='STATUS':
			fields['k1']=unicode('״̬')
			fields['k2']=unicode('�豸����')
			fields['k3']=unicode('ʱ��')
			
			fields['k4']=unicode('���õص�')
			fields['k5']=unicode('�澯��')
			
			cols = len(fields.keys())
			self.context = ScrolledHList(self.p2,scrollbar ='auto',options="hlist.columns %s header 1"%cols)
			self.context.pack(fill='both',expand=1,padx=4,pady=4)
			self.hlist = self.context.hlist
			self.hlist.configure(command=self.onstatus)
			self.hlist.config(separator='.', width=25, drawbranch=0)
			self.hlist.column_width(0, chars=10)
			self.hlist.column_width(1, chars=25)
			self.hlist.column_width(2, chars=25)
			self.hlist.column_width(3, chars=25)
			#self.hlist.column_width(4, chars=25)

			ks = fields.keys()
			self.hlist.header_create(0,itemtype='text',text=fields['k1'])					
			self.hlist.header_create(1,itemtype='text',text=fields['k2'])					
			self.hlist.header_create(2,itemtype='text',text=fields['k4'])					
			self.hlist.header_create(3,itemtype='text',text=fields['k3'])					
			self.hlist.header_create(4,itemtype='text',text=fields['k5'])					
			for r in rs:
				
				wl = r['WARNINGLEVEL']
				
				if wl==None:
					wl=0
				wltext = constdef.warninglevel[str(wl)]
				
				pi =self.pwl0
				if wl==1:
					pi =self.pwl1
				if wl==2:
					pi =self.pwl2
				if wl==3:
					pi =self.pwl3
				
				self.hlist.add(r['ID'],itemtype='imagetext',image=pi,text=wltext)
				
				devtitle =''
				site=''
				for i in session.user.repeaters:
					if i['ID']==r['REPEATER_ID']:
						devtitle= session.getdevtitle(i)
						site = session.getsite(i)
					
				self.hlist.item_create(r['ID'],1,itemtype='text',text=devtitle)
				
				time = r['OPTTIME']
				time = time.Format('%Y/%m/%d %H:%M:%S')
				
				self.hlist.item_create(r['ID'],2,itemtype='text',text=site)
				self.hlist.item_create(r['ID'],3,itemtype='text',text=time)
				
				#�����б�
				sql = "SELECT c.fieldname,c.descript,c.UPLIMIT,C.DOWNLIMIT FROM repeaterinfo a ,status b,param_config c "
				sql+= " where a.id=b.repeater_id and a.repeatertype=c.repeatertype and c.is_warning=1 "
				sql+= "	and b.id=%s"
				sql = sql%r['ID']
				
				ret  = session.getdata(sql)
				param_list=[]
				for i in ret:
					if self.is_warning(i,str(r[i['FIELDNAME']]).strip()):					
						param_list.append(i['DESCRIPT'])
				self.hlist.item_create(r['ID'],4,itemtype='text',text=string.join(param_list,","))
				
		if 	opttype.upper()=='WARNING':
			fields['k1']=unicode('�澯����')
			fields['k2']=unicode('�豸����')
			fields['k5']=unicode('���õص�')
			fields['k3']=unicode('ʱ��')			
			fields['k4']=unicode('�澯��')
			
			cols = len(fields.keys())
			self.context = ScrolledHList(self.p2,scrollbar ='auto',options="hlist.columns %s header 1"%cols)
			self.context.pack(fill='both',expand=1,padx=4,pady=4)
			self.hlist = self.context.hlist
			self.hlist.configure(command=self.onwarning)
			
			self.hlist.config(separator='.', width=25, drawbranch=0)
			self.hlist.column_width(0, chars=20)
			self.hlist.column_width(1, chars=25)
			self.hlist.column_width(2, chars=25)
			

			ks = fields.keys()
			self.hlist.header_create(0,itemtype='text',text=fields['k1'])					
			self.hlist.header_create(1,itemtype='text',text=fields['k2'])					
			self.hlist.header_create(2,itemtype='text',text=fields['k5'])	
			self.hlist.header_create(3,itemtype='text',text=fields['k3'])				
			self.hlist.header_create(4,itemtype='text',text=fields['k4'])	
							
			for r in rs:				
				wl = r['WARNINGLEVEL']
				
				wltext = constdef.warninglevel[str(wl)]
				
				pi =self.pwl0
				if wl==1:
					pi =self.pwl1
				if wl==2:
					pi =self.pwl2
				if wl==3:
					pi =self.pwl3
				
				self.hlist.add(r['ID'],itemtype='imagetext',image=pi,text=wltext)
				
				
				
				devtitle =''
				site=''
				for i in session.user.repeaters:
					if i['ID']==r['REPEATER_ID']:
						devtitle= session.getdevtitle(i)
						site = session.getsite(i)
				
					
				self.hlist.item_create(r['ID'],1,itemtype='text',text=devtitle)
				self.hlist.item_create(r['ID'],2,itemtype='text',text=site)
				time = r['OPTTIME']
				time = time.Format('%Y/%m/%d %H:%M:%S')
				
				self.hlist.item_create(r['ID'],3,itemtype='text',text=time)
				
				#�����б�
				sql = "SELECT c.fieldname,c.descript,c.UPLIMIT,C.DOWNLIMIT FROM repeaterinfo a ,status b,param_config c "
				sql+= " where a.id=b.repeater_id and a.repeatertype=c.repeatertype and c.is_warning=1 "
				sql+= "	and b.id=%s"
				sql = sql%r['ID']
				
				ret  = session.getdata(sql)
				param_list=[]
				for i in ret:
					if self.is_warning(i,str(r[i['FIELDNAME']]).strip()):
						param_list.append(i['DESCRIPT'])
				self.hlist.item_create(r['ID'],4,itemtype='text',text=string.join(param_list,","))

	##########################################################################
					
		if 	opttype.upper()=='CONTROL':
			fields['k1']=unicode('�豸����')
			fields['k6']=unicode('���õص�')
			fields['k2']=unicode('����ʱ��')	
			#fields['k3']=unicode('��Ӧʱ��')
			fields['k4']=unicode('���ƽ��')
			fields['k5']=unicode('������')
			
			
			cols = len(fields.keys())
			
			self.context = ScrolledHList(self.p2,scrollbar ='auto',options="hlist.columns %s header 1"%cols)
			self.context.pack(fill='both',expand=1,padx=4,pady=4)
			self.hlist = self.context.hlist
			self.hlist.configure(command=self.oncontrol)
			
			self.hlist.config(separator='.', width=25, drawbranch=0)
			self.hlist.column_width(0, chars=20)
			self.hlist.column_width(1, chars=25)
			self.hlist.column_width(2, chars=25)
			self.hlist.column_width(3, chars=25)
			
			
			ks = fields.keys()
			self.hlist.header_create(0,itemtype='text',text=fields['k1'])	
			self.hlist.header_create(1,itemtype='text',text=fields['k6'])								
			self.hlist.header_create(2,itemtype='text',text=fields['k2'])					
			#self.hlist.header_create(3,itemtype='text',text=fields['k3'])					
			self.hlist.header_create(3,itemtype='text',text=fields['k4'])					
			self.hlist.header_create(4,itemtype='text',text=fields['k5'])					
			
			for r in rs:								
				devtitle =''
				site = ''
				for i in session.user.repeaters:
					if i['ID']==r['REPEATER_ID']:
						devtitle= session.getdevtitle(i)
						site = session.getsite(i)
				
				path = r['ID']
				self.hlist.add(path,itemtype='text',text=devtitle)	
				self.hlist.item_create(path,1,itemtype='text',text=site)
				
				time = r['OPTTIME']
				time = time.Format('%Y/%m/%d %H:%M:%S')
				self.hlist.item_create(path,2,itemtype='text',text=time)
				time = r['BACKTIME']
				if time:
					time = time.Format('%Y/%m/%d %H:%M:%S')
				else:
					time=""				
				#self.hlist.item_create(path,3,itemtype='text',text=time)
				
				result = r['RESULT']
				if result==None:
					result=""
				else:
					result=constdef.errors[str(result)]
				self.hlist.item_create(path,3,itemtype='text',text=result)

				#�����б�
				sql = "SELECT c.control_map_status,c.descript FROM repeaterinfo a ,control b,param_config c "
				sql+= " where a.id=b.repeater_id and a.repeatertype=c.repeatertype and c.is_control=1 "
				sql+= "	and b.id=%s"
				sql = sql%r['ID']
				
				ret  = session.getdata(sql)
				param_list=[]
				for i in ret:
					if r[i['CONTROL_MAP_STATUS']] != None:
						param_list.append(i['DESCRIPT'])
				self.hlist.item_create(r['ID'],4,itemtype='text',text=string.join(param_list,","))

		
		#�û��������
		if 	opttype.upper()=='USERMGR':
			fields['k1']=unicode('����')
			fields['k2']=unicode('�豸����')
			fields['k3']=unicode('����Ա')
			fields['k4']=unicode('ʱ��')	
			fields['k5']=unicode('״̬')	
			
			
			cols = len(fields.keys())
			
			self.context = ScrolledHList(self.p2,scrollbar ='auto',options="hlist.columns %s header 1"%cols)
			self.context.pack(fill='both',expand=1,padx=4,pady=4)
			self.hlist = self.context.hlist
			#self.hlist.configure(command=self.oncontrol)
			
			self.hlist.config(separator='.', width=25, drawbranch=0)
			self.hlist.column_width(0, chars=20)
			self.hlist.column_width(1, chars=20)
			self.hlist.column_width(2, chars=12)
			self.hlist.column_width(3, chars=20)
			self.hlist.column_width(4, chars=25)
			
			ks = fields.keys()
			self.hlist.header_create(0,itemtype='text',text=fields['k1'])					
			self.hlist.header_create(1,itemtype='text',text=fields['k2'])					
			self.hlist.header_create(2,itemtype='text',text=fields['k3'])					
			self.hlist.header_create(3,itemtype='text',text=fields['k4'])					
			self.hlist.header_create(4,itemtype='text',text=fields['k5'])					
			
			devtitle=''
			for r in rs:								
				path = r['TRANSACTIONNO']
				self.hlist.add(path,itemtype='text',text=r['DESCRIPT'])	
				target = r['TARGET']
				if target==None or target.strip()=="":
					target=unicode("ϵͳ")
				else:
					
					for i in session.user.repeaters:
						if i['ID']==int(str(target)):
							devtitle= session.getdevtitle(i)			
									
				self.hlist.item_create(path,1,itemtype='text',text=devtitle)
				self.hlist.item_create(path,2,itemtype='text',text=r['REAL_NAME'])
				time = r['OPTTIME']
				time = time.Format('%Y/%m/%d %H:%M:%S')
				self.hlist.item_create(path,3,itemtype='text',text=time)
				

				result = r['RESULT']
				try:
					result=constdef.errors[str(result)]
				except:
					result =""
					
				self.hlist.item_create(path,4,itemtype='text',text=result)

		
			
	def onwarning(self,item):
		pls = PaneLogStatus(self)
		pls.show_status(item)
		
		
	def onstatus(self,item):
		pls = PaneLogStatus(self)
		pls.show_status(item)
		
	def oncontrol(self,item):
		plc = PaneLogControl(self)
		plc.show(item)
		
		
		