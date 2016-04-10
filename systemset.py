


#----------------------------------------------------------------------------------------
#包括系统基础信息的维护
#
#历史:
#		1. 2003.07.22 添加get_paramtype方法，在发送命令参数包是，读取数据表param_config的参数的类型（1，2，3），发送给mss
#----------------------------------------------------------------------------------------


from Tix import *
import Pmw
import tkMessageBox
import re
import string 
import time
import webbrowser
import copy

import constdef
import login
import net_train
import ado
import session
import log
import user
#############################################################################

################################################################################
class BlinkButton(Button):
	def __init__(self,master):
		Button.__init__(self,master)
		self.canblink= 0
		
	def setblink(self):
		self.canblink= 1
		pass
	
class PaneStatus(Toplevel):
	'''状态显示面板
		功能:显示设备状态信息，包括当前告警状态
		告警状态用red,green颜色显示，同时显示当前地告警状态值
		状态记录结构定义:
												
	'''
	def __init__(self,master):
		self.master = master
		Toplevel.__init__(self,master)		
		#数据定义
		self.widgets=[]
		self.control_widget=[]	#用户控制参数而创建地部件
		self.control_params=[]
		self.id =0
		self.status=[]
		self.cur_dev=None
		
		fall = Frame(self)
		fall.pack(fill='both',expand=1)
		
		f = Frame(fall)
		f.pack(fill='x',side='top',pady=4)
		self.title = Label(f,text='')
		self.title.pack()
		self.time = Label(f,text='')
		self.time.pack()

		#创建命令控制条
		
		
		#tabpanel
		self.nb = NoteBook(fall)
		self.nb.pack(fill='both',side='top',expand=1,padx=10,pady=10)
		self.p1 = self.nb.add('status',label=unicode('状 态'))
		self.p2 = self.nb.add('control',label=unicode('控 制'))
		
		
		#状态
		f = Frame(self.p1,relief='groove')
		f.pack(fill='x',side='bottom',padx=10,pady=4)

		if session.user.has_rights(user.R_DEV_STATUS_QUERY):
			Button(f,text=unicode('查询'),command=self.doquery).pack(side='right',padx=8,pady=2)
		Button(f,text=unicode('刷新'),command=lambda :self.show_status(self.id)).pack(side='right',padx=8,pady=2)		
		#滚动容器
		self.sw = ScrolledWindow(self.p1,scrollbar='auto')
		self.sw.pack(fill='both',side='top',expand=1,padx=10,pady=10)

		#控制
		f = Frame(self.p2,relief='groove')
		f.pack(fill='x',side='bottom',padx=10,pady=4)
		if session.user.has_rights(user.R_DEV_CONTROL):
			Button(f,text=unicode('控制'),command=self.oncontrol).pack(side='right',padx=8,pady=2)		

		self.swcontrol = ScrolledWindow(self.p2,scrollbar='auto',relief='groove')
		self.swcontrol.pack(fill='both',side='top',expand=1,padx=10,pady=10)
		
		#开始检测告警参数，准备闪烁
		#self.after(500,self.blink)
		self.wm_protocol("WM_DELETE_WINDOW", lambda : self.onclose())
		
		self.wm_title(unicode('设备状态'))
		
		
	def onclose(self):
		session.form_status =None
		self.destroy()
		
	#发送查询命令 
	def doquery(self):
		session.query_it(self.id)
		
	#取类型，参数设定的参数类型，整型，浮点，字符串型
	def get_paramtype(self,repeatertype,paramname):
		for item in session.param_configs:
			if item['REPEATERTYPE']==repeatertype and item['PARAMNAME']==paramname:
				return item['PARAM_TYPE']
		return 1 #default is integer
		
#########################################################################		
	#参数控制,用户选择控制按钮
	def oncontrol(self):
		if self.status==[]:
			return
		if self.control_params==[]:
			return 
		sel_list =[]
		has_sel=0
		for pc in self.control_params:
			
			stm = "v= self.var%s.get()"%pc['PARAMNAME']			
			exec(stm)
			if v:	#如果选择设置　
				print pc['PARAMNAME']
				has_sel=1
				for c in self.control_widget:
					
					if c[0]==pc['PARAMNAME']:						
						
						w = c[1]
						val =''
						if c[2]=='en':
							if not w.valid():
								tkMessageBox.showwarning(unicode('警告!'),unicode('参数值无效:')+pc['DESCRIPT'])
								return
							else:															
								sel_list.append([pc['PARAMNAME'],w.getvalue(),0,1])
						if c[2]=='cb':
							val = w.cget('value')
							try:
								ls1=[]
								ls1 = re.split(';',pc['UI_VALUE_RANGE'])
								for s in ls1:
									ls2 =re.split(':',s)
									
									if ls2[0]==val:	#
										print ls2[0],val,"compare"
										val = int(ls2[1])
										break
									
								
							except:
								val =0
								#tkMessageBox.showwarning(unicode('警告!'),unicode('参数值无效:')+pc['DESCRIPT'])
								#return
							sel_list.append([pc['PARAMNAME'],val,0,1])
						
			else:				
				#取当前状态记录的当前字段值
				fieldname=pc['FIELDNAME']							
				
				cur_rec = self.status[0]	
				try:
					v =cur_rec[fieldname]
					if v==None:
						v=str(session.control_run_param_default)
				except:
					v =str(session.control_run_param_default)
					
				sel_list.append([pc['PARAMNAME'],v,0,0])
		
				
		
		if has_sel==0:	#当前无控制参数，撤销操作 
			return		
		
			
			
		s=[]
		for ctrl_item in sel_list:
			type =""
			type = self.get_paramtype(self.cur_dev['REPEATERTYPE'],ctrl_item[0])
			s.append("%s,%s,%s"%(ctrl_item[0],type,ctrl_item[1]))
			
		data = session.grab_tcp_package(self.id)
		data[4]="%s"%constdef.CMD_REMOTE_CTRL
		data[8]= "%s"%session.getsequence()
		sendstr = "%s@%s"%(string.join(data,','),string.join(s,';'))
		print sendstr
		try:
			if  net_train.send2mss(sendstr)!=1:
				raise 1
			log.recLog(str(self.id),log.LOG_CONTROL,data[8])			
			tkMessageBox.showwarning('',unicode('控制命令发送中!'))			
		except:
			tkMessageBox.showwarning('',unicode(' 与MSS通信失败!'))
			return 

		
		
	def blink(self):
		'''闪烁'''
		for i in self.widgets:			
			if i.__class__.__name__ =='BlinkButton':
				#检测是否可闪烁
				if i.canblink==1:					
					color = i.cget('background')
					if color=='red':
						i.config(background='green')
					else:
						i.config(background='red')
		self.after(500,self.blink)
		
	def is_warning(self,param_item,cur_val):
		""" param_item:参数记录 
		cur_val	: 当前记录值
		检测cur_val是否在param_config->uplimit  downlimit 之间，否则判断为告警(return 1)
		"""
		#print param_item['PARAM_NAME'],cur_val
		cur_val = float(cur_val)
		if cur_val >=param_item['UPLIMIT'] and cur_val <=param_item['DOWNLIMIT']:
			return 1
		
		return 0
		
#########################################################################
	#显示指定设备的状态信息
	# forlog_status_id -- 用于状态日志查询的状态记录ID
	def show_status(self,devid):
		'''创建状态,控制控件'''
		self.id =  devid
		##################################################################
		for i in self.widgets:
			i.destroy()
			del i
		self.widgets=[]
		
		for i in self.control_widget:
			i[1].destroy()
			
			del i[1]	#删除存储的ｗｉｇｅｔ对象
		self.control_widget =[]
		self.control_params=[]
		##################################################################
		# 优化速度
		sql = "select * from repeaterinfo where id=%s"%devid		
		devinfo = session.getdata(sql)
		title = session.getdevtitle(devinfo[0])
		self.title.config(text = title)
		row = devinfo[0]
		self.cur_dev = row
		#param_status = 
		sql = "select * from param_config where repeatertype=%s and is_status=1 and isdisplay=1"%row['REPEATERTYPE']
		param_status = session.getdata(sql)
		#print "get %s object from param_config"%len(param_status)
		#获取当前设备工作状态记录
		
		sql = 'select * from statusview where repeater_id=%s'%devid	
			
		self.status = session.getdata(sql) 		
		cur_status = self.status
		if len(cur_status) ==0:
			param_status =[]
		else:	
			cur_status =cur_status[0]
		##############################################
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
				column = 2	#同行的第二个状态参数排布位置
#			elif column == 2:
#				column = 4							
			lb = Label(self.sw.window,text=i['DESCRIPT'],anchor='e',relief='groove')
			lb.grid(column = column,row = row,padx=4,pady=2,sticky='e')
			self.widgets.append(lb)
			
			i['PARAMNAME'] =string.strip(i['PARAMNAME'] )
			

			#不区分告警值，所有的状态值都是有告警的可能
			text=""
			try:
				text =cur_status[i['FIELDNAME']]
			except:
				print 'get value error:SELECT VALUE INVALID!!!! ==> %s'%i['FIELDNAME']
				text ="?"
			
				
			#显示开关字符
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
			#检测当前值是否告警
			if self.is_warning(i,str(cur_status[i['FIELDNAME']])):
				lb.config(background='red')
			else:
				lb.config(background='green')
				
				
			lb.grid(column = column+1,row = row,padx=4,pady=2)
			self.widgets.append(lb)		
				
#		##################################################################
#		# 创建控制面板参数
			if i['IS_CONTROL']==1:
				self.control_params.append(i) #将当前参数结构保存
				lb = Label(self.swcontrol.window,text=i['DESCRIPT'],anchor='e')
				lb.grid(column = 0,row = idx,padx=4,pady=2,sticky='e')				
				#self.control_widget.append(lb) 
				self.widgets.append(lb)
				
				
				stm="self.var%s=IntVar()"%i['PARAMNAME']				
				exec(stm)
				stm ="self.ck%s= Checkbutton(self.swcontrol.window,variable=self.var%s )"%(i['PARAMNAME'],i['PARAMNAME'])								
				exec(stm)				
				stm ="self.ck%s.grid(column = 2,row = idx,padx=4,pady=2)"%i['PARAMNAME']
				exec(stm)
				
				stm = "self.widgets.append(self.ck%s)"%i['PARAMNAME']
				exec(stm)
				
								
				if i['UI_TYPE']=='TEXT':					
					#在这里，没有进行entry值输入的约束，对输入控制的参数没有进行校验
					stm=""
					if i['PARAM_TYPE']==1:	#整型值
						stm = "self.en%s = Pmw.EntryField(self.swcontrol.window,labelpos='w',validate = {'validator' : 'integer'} )"
					elif i['PARAM_TYPE']==3:	#浮点型
						stm = "self.en%s = Pmw.EntryField(self.swcontrol.window,labelpos='w',validate = {'validator' : 'real'} )"
						
					stm = stm%i['PARAMNAME']
					exec(stm)
					stm ="self.en%s.grid(column = 1,row = idx,padx=4,pady=2,sticky='w')"
					stm = stm%i['PARAMNAME']
					exec(stm)
					#负值
					v=""
					try:
						v =cur_status[i['FIELDNAME']]
					except:
						v=""
					stm ="self.en%s.setentry(%s)"%(i['PARAMNAME'],v)
					exec(stm)
					
					stm = "self.control_widget.append(['%s',self.en%s,'en'])"%(i['PARAMNAME'],i['PARAMNAME'])
					exec(stm)
				if i['UI_TYPE']=='SELECT':						
					stm = "self.cb%s=ComboBox(self.swcontrol.window )"%i['PARAMNAME']					
					exec(stm)
					stm ="self.cb%s.grid(column = 1,row = idx,padx=4,pady=2,sticky='w')"
					stm = stm%i['PARAMNAME']
					
					exec(stm)
					
					stm = "self.control_widget.append(['%s',self.cb%s,'cb'])"%(i['PARAMNAME'],i['PARAMNAME'])
					exec(stm)
					
					range = i['UI_VALUE_RANGE']
					
					ls1 = re.split(';',range)
					for s in ls1:
						ls2 =re.split(':',s)
						
						stm = "self.cb%s.append_history(unicode('%s'))"%(i['PARAMNAME'],ls2[0])	
						exec(stm)
						
					#负值
					v=0
					try:
						ls1=[]
						ls1 = re.split(';',i['UI_VALUE_RANGE'])
						for s in ls1:
							ls2 =re.split(':',s)
							if int(ls2[1])==int(cur_status[i['FIELDNAME']]):	#
								v = ls2[0]
								break
						else: 
							v ="?"
						
					except:
						v=""

					stm = "self.cb%s.config(value=unicode('%s'))"%(i['PARAMNAME'],v)	
					#print stm
					exec(stm)
#			
			idx+=1
		
			
			

#############################################################################
class PaneAlarmFlag(Toplevel):
	'''
		功能:显示和设置设备告警使能标志
			 支持对一单独设备的告警使能标志的设定												
	'''
	def __init__(self,master):
		self.master = master
		Toplevel.__init__(self,master)		
		#数据定义
		self.id =0
		self.devinfo=None #当前设备记录
		#定义widget容器
		self.widgets=[]
		
		fall = Frame(self)
		fall.pack(fill='both',expand=1)
		
		f = Frame(fall)
		f.pack(fill='x',side='top',pady=4)
		self.title = Label(f,text='')
		self.title.pack(side='left')
		
		self.fbottom = Frame(fall)
		self.fbottom.pack(side='bottom',fill='x',padx=10,pady=10)
		self.apply = IntVar()
		self.ckApply =Checkbutton(self.fbottom,text =unicode('应用于所有设备') ,variable=self.apply)
		#self.ckApply.pack(side='left' )
		Button(self.fbottom,text=unicode('关 闭'),command = self.onclose).pack(side='right')
		if session.user.has_rights(user.R_DEV_ALARM_FLAG_SET):
			Button(self.fbottom,text=unicode('设 置'),command = self.onsave).pack(side='right')
		
		#参数的容器面板
		self.fcontext = Frame(fall,relief='sunken',borderwidth=2)
		self.fcontext.pack(fill='both',padx=10,pady=14)
		
		self.wm_protocol("WM_DELETE_WINDOW", lambda : self.onclose())
		self.wm_title(unicode('设备告警使能标志'))
		
	def onclose(self):
		session.form_warningflag =None
		self.destroy()

		
	def show(self,devid):
		self.id = devid
		sql = "select * from repeaterinfo where id=%s"%devid				
		self.devinfo = session.getdata(sql)
		title = session.getdevtitle(self.devinfo[0])
		
		self.title.config(text = unicode('设备: ')+title)
		row = self.devinfo[0]
		for i in self.widgets:
			i[1].destroy()
			del i[1]
		self.widgets =[]
		#取得告警参数
		sql = "select * from param_config where repeatertype=%s and is_warning=1 "%row['REPEATERTYPE']
		param_warning = session.getdata(sql)
		idx=0
		for i in param_warning :
			lb = Label(self.fcontext,text=i['DESCRIPT'],anchor='w',relief='groove')
			lb.grid(column = 0,row =idx,padx=4,pady=2,sticky='w')
			self.widgets.append( [   i['PARAMNAME'],lb,'lb' ] )
			stm="self.var%s=IntVar()"%i['PARAMNAME']				
			exec(stm)
			stm ="self.ck%s= Checkbutton(self.fcontext,variable=self.var%s )"%(i['PARAMNAME'],i['PARAMNAME'])								
			exec(stm)				
			stm ="self.ck%s.grid(column = 1,row = idx,padx=4,pady=2)"%i['PARAMNAME']
			exec(stm)
			stm = "self.widgets.append( ['%s',self.ck%s,'ck' ] )"%(i['PARAMNAME'],i['PARAMNAME'])
			exec(stm)	#将widget添加到数据容器
			pos=0
			
			pos = constdef.alarmflags.index(i['PARAMNAME'])
				
			print 'alarm flat ocurpy >> ',pos
			#显示当前的使能标志状态
			if row['ALARMFLAG'] & (1<<pos)!=0:
				
				stm = "self.var%s.set(1)"%i['PARAMNAME']				
				exec(stm)				

			idx+=1	
			
	#保存目前设置使能参数
	def onsave(self):
		intval=0
		params=[]
		for w in self.widgets:
			if w[2]=='ck':
				
				v =0
				stm = "v = self.var%s.get()"%w[0]	#取checkbutton帮定的IntVar的值
				exec(stm)
				if v:
					params.append("%s,1,1"%w[0])
				else:
					params.append("%s,1,0"%w[0])
#					pos = constdef.alarmflags.index(w[0])
#					intval |=1<<pos					
					
		#将告警值存入数据库
		#sql = "update repeaterinfo set ALARMFLAG=%d where id = %d"%(intval,self.id)
		#print sql
		data = session.grab_tcp_package(self.id)
		data[4]="%s"%constdef.cmd_list['SET_AUTO_ALARM_FLAG']
		data[8]= "%s"%session.getsequence()
		
		try:
			#session.dbcnn.Execute(sql)
			#notify mss by net_train
			sendstr= "%s@%s"%(string.join(data,','),string.join(params,";"))
			if  net_train.send2mss(sendstr)!=1:
				
				raise 1

			tkMessageBox.showwarning('',unicode('告警使能标志设置发送中!'))
			
		except:
			tkMessageBox.showwarning('',unicode(' 与MSS通信失败!'))
			return 
		#写入日志
		log.recLog(str(self.id),log.LOG_MODIFY_ALARMFLAG,data[8])
		

		
#############################################################################
class PaneArea(Frame):
	''' 
		统计告经个数 
	'''
	def __init__(self,owner,master,callback):		
		Frame.__init__(self,owner)		
		#self.option_add('*Button.Font',('宋体',2))
		self.master = master
		self.id =0
		self.name=''
		self.callback = callback	#回调显示指定设备
		
		self.bt_area = Button(self,command=self.show_repeater,width=10)
		self.bt_area.pack(side='left',padx=4,pady=2)

		self.w0 = Button(self,relief='raise',bg='green',font=('宋体',7),command= lambda : self.onwarningsel(0))
		self.w1 = Button(self,relief='raise',bg='yellow',font=('宋体',7),command= lambda : self.onwarningsel(1))
		self.w2 = Button(self,relief='raise',bg='blue',font=('宋体',7),command= lambda : self.onwarningsel(2))
		self.w3 = Button(self,relief='raise',bg='red',font=('宋体',7),command= lambda : self.onwarningsel(3))
		#显示响应超时设备
		self.no_response = Button(self,relief='raise',font=('宋体',7),command= lambda : self.callback(self,self.id,-1,1))
		
		self.w0.pack(side='right')
		self.w1.pack(side='right')
		self.w2.pack(side='right')
		self.w3.pack(side='right')
		self.no_response.pack(side='right')
		
		
		
		self.bt_area.bind('<3>',self.area_options)

	
	#显示区域信息以及告经类别		
	def set(self,id,name,ondelete):
		self.bt_area.config(text = name)
		self.name = name
		self.id =id
		self.ondelete = ondelete
		
		
		w0=0
		w1=0
		w2=0
		w3=0
		data=[]
		#查找主设备 ，根据区域编号 
		for i in session.user.repeaters:
			print i['AREA_ID'],id
			
			if i['AREA_ID']==int(id):
				data.append(i)
		
		print "%s repeater in this area"%len(data)
		for i in data:
			v = session.get_warning_type(i['ID'])			
			if v == 0:
				w0+=1
			if v==1:
				w1+=1
			if v==2:
				w2+=1
			if v==3:
				w3+=1
		w0 = len(data)-w3-w2-w1				
		# do no response device time out
		timeout_cnt=0
		for i in data:			
			if session.is_timeout(i['ID']):	#master device timeout
				timeout_cnt+=1;

		print '--告警个数统计--%s-%s-%s-%s'%(w0,w1,w2,w3)	
		self.w0.config(text=w0)
		self.w1.config(text=w1)
		self.w2.config(text=w2)
		self.w3.config(text=w3)
		self.no_response.config(text=timeout_cnt)
		
	#取４种告警总数
	def get_warningcount(self):
		pass
		
	
	#显示本区域指定告警级别的设备
	def onwarningsel(self,waringtype):
		self.callback(self,self.id,waringtype)
		pass 
		
	
	def area_options(self,ev):
		menu =Menu(ev.widget,selectcolor='red',tearoff=0)
		
		#menu.add_separator()
		#menu.add_command(label=unicode('新 增'))
		#删除区域信息，将id,name回传给调用者
		if session.user.has_rights(user.R_AREA_DEL):
			menu.add_command(label=unicode('删 除'),command=lambda :self.ondelete(self.id,self.name))		
		if session.user.has_rights(user.R_AREA_MODIFY):
			menu.add_command(label=unicode('修 改'),command=lambda :self.onmodify())		
		
		menu.add_separator()
		if session.user.has_rights(user.R_DEV_STATUS_QUERY):
			menu.add_command(label=unicode('状态查询'),command=lambda:session.batch_query_status(self.id))
		if session.user.has_rights(user.R_DEV_PARAM_QUERY):
			menu.add_command(label=unicode('网管参数查询'),command=lambda:session.batch_query_netparam(self.id))				
		menu.add_separator()
		#设备报表输出
		menu.add_command(label=unicode('输出设备清单'),command=self.on_dev_print)				
		
		menu.post(ev.widget.winfo_rootx()+ev.x,ev.widget.winfo_rooty()+ev.y)

	#显示区域所有设备
	def show_repeater(self):
		'''显示区域所有设备'''
		self.callback(self,self.id)
		pass
	def onmodify(self):
		pca = PaneCareArea(self.master)
		pca.show(self.id,self.name)
		pca.activate()
	
	#设备打印
	#报表
	def on_dev_print(self):
		cache ='./cache'
		html =unicode("设备区域:%s<br>\n%s<br>%s")
		
		
		area = session.match(session.areas,"ID","INT",int(self.id),"NAME")
		table ="<table width='100%' border=1 align='center' cellpadding=0 cellspacing=0>\n"
		table+="<tr><td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n </tr>" %(unicode('设备名称'),unicode('设备电话'),unicode('站点号'),unicode('设备类型'),unicode('放置地点'))
		list =[]
		for i in session.user.repeaters:			
			if i['AREA_ID']==self.id:  #主设备
				product = session.match(session.products,"ID","INT",i['PRODUCT_ID'],"DESCRIPT")
		 		table+="\n<tr><td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n </tr>"%(i['NAME'],i['REPEATER_PHONE'],i['REPEATER_ID'],product,i['SITE'])
		table+="</table>"
		timetag = time.strftime("%Y-%m-%d %H:%M:%S ",time.localtime())
		html = html%(area,table,unicode('打印时间:')+timetag)
		
		tempreport = "%s/%s.htm"%(cache,str(time.clock()))
		fh = open(tempreport,'w')
		fh.write(html)
		fh.close()
		#显示报表输出
		webbrowser.open(tempreport)
	
		 			
#####################################################################################################################		
		
		
	

		
		
		
import repeaterlist		
import devinfo
class PaneDeviceMgr(Frame):
	'''  
		功能:设备管理
		　　　区域管理，设备查询，控制
		--------------------------------------------|
		|		  tools bar						|
		|-------|-----------------------------------|	
		| areas	|									|
		|---s--	|									|
		|		|       	  repeater list			|
		|		|									|
		|		|									|
		--------------------------------------------|
	'''
	def __init__(self,master):		
		Frame.__init__(self,master)		
		self.master = master
		
		self.top = Frame(self,borderwidth=2)
		self.top.pack(side='top',fill='x',padx=2,pady=2)	
		if session.user.has_rights(user.R_AREA_ADD):			
			Button(self.top,text=unicode('添加区域'),command= self.on_new_area).pack(side='left',padx=4)
		if session.user.has_rights(user.R_DEV_ADD):			
			Button(self.top,text=unicode('添加设备'),command = self.on_new_dev).pack(side='left',padx=4)
		Button(self.top,text=unicode('刷新'),command = self.do_manual_flash).pack(side='left',padx=4)
		
		
		
		self.down = Frame(self,borderwidth=2)
		self.down.pack(fill='both',expand= 1,padx=2,pady=2)		

		self.fleft = Frame(self.down,borderwidth=2,width=180)
		self.fleft.pack(side='left',fill='y',padx=2,pady=2)
		self.fright = Frame(self.down,borderwidth=2,relief='groove')
		self.fright.pack(fill='both',expand=1,padx=4,pady=4)

		
		#Button(self.fleft,text='top bar').pack()
		Label(self.fleft,text=unicode('设备区域:')).pack(pady=4)
		#告警
		#self.fwarning_status = PaneWarning(self.fleft,{'borderwidth':2,'relief':'raise'})
		#self.fwarning_status.pack(side='bottom',fill='x',padx=4,pady=4)
		self.sw_area = ScrolledWindow(self.fleft,scrollbar='auto')
		self.sw_area.pack(fill='both',expand=1)
		#显示区域标签
		self.areas =[]
		self.reload_area()	
		#显示当前设备
		self.rlist = repeaterlist.RepeaterList(self.fright)
		self.rlist.pack(expand=1,fill='both')
		#self.all_warning = Frame(self.fright)
		
		#开启定时器
		#2003.05.16 由于定时刷新造成许多后续维护操作，所以去除定时，改为手动刷新
		#2003.06.04 开放区域告警个数统计的定时 
		self.after(session.area_warningcount_interval,self.flashwarningcount)
	
	def onstatus(self):
		ps =PaneStatus(Toplevel())
		ps.pack()
		ps.show_status(2)
		
	def on_area_delete(self,id,name):
		sql = 'select count(*) as cnt from repeaterinfo where area_id =%s'%id
		rs = session.getdata(sql)
		rs = rs[0]
		if int(rs['CNT']):	
			tkMessageBox.showwarning(unicode('警告!'),unicode('存在设备，区域不能被删除!'))						
			return 
		if tkMessageBox.askyesno(unicode('提示!'),unicode('是否真的要删除?'))==0:
			return 

		sql ='delete from area where id=%s'%id
		try:
			session.dbcnn.Execute(sql)
			sql = "select * from area"
			session.areas = session.getdata(sql)
			session.user.load_area_rights()
			self.reload_area() 	#刷新区域信息列表

		except:
			tkMessageBox.showwarning(unicode('警告!'),unicode('删除区域失败!'))							
			return 

				
		
		
		pass
		
	def reload_area(self):
		for w in self.areas:
			w.destroy()
			del w
			
		self.areas=[]
		#print session.user.areas
		for i in session.user.areas:
			pa = PaneArea(self.sw_area.window,self,self.onshow)						
			pa.set(i['ID'],i['NAME'],self.on_area_delete)			
			pa.pack()			
			self.areas.append(pa)		
			
	
	def do_flash(self):
		sql= "select  repeater_id,WARNINGLEVEL,OPTTIME from statusview "		
		session.current_dev_statuses = session.getdata(sql)
		session.user.load_repeaters()
		print sql
		#刷新区域告警个数		
		for i in self.areas:
			#print i
			i.set(i.id,i.name,self.on_area_delete)	
			
	def do_manual_flash(self):
		''' 手动刷新区域告警个数和本次区域设备状态信息'''				
		print "do manual query area warning count and devs in current  area"
		self.do_flash()		
		self.rlist.reflash()
		
	def flashwarningcount(self):
		''' 定时刷新告警个数'''
		print "time out for quering warning count of area"
		self.do_flash()
		self.after(session.area_warningcount_interval,self.flashwarningcount)
	
	#显示设备
	def onshow(self,area,area_id,warning=-1,show_no_response=0):
		''' 显示区域设备
		参数:
		show_no_response	-- 显示未响应设备 ,default=0
		'''
		
		#设置选择颜色
		for w in self.areas:
			w.config(background='SystemButtonFace')
						
		area.config(background='goldenrod2')	
		
		self.rlist.show(area_id,warning,show_no_response)
		
	def on_new_area(self):
		pca = PaneCareArea(self)
		pca.new()
		pca.activate()
	def on_new_dev(self):
		devinfo.PaneDevInfo(self)

		
#区域添加维护
class PaneCareArea(Pmw.MegaToplevel):
	def __init__(self,master):
		Pmw.MegaToplevel.__init__(self,master)
		self.master = master
		f =Frame(self.component('hull'))
		f.pack(fill='x',side='bottom',padx=4,pady=4)
		Button(f,text=unicode('确定'),command= self.onsave).grid(column=0,row=0)
		Button(f,text=unicode('取消'),command=lambda :self.destroy()).grid(column=1,row=0)
		f = Frame(self.component('hull'))
		f.pack(fill='both',padx=4,pady=4)
		self.enArea = Pmw.EntryField(f,labelpos = 'w',label_text=unicode('区域名称:'),validate={'max':20})
		self.enArea.pack(fill='x',expand=1)
		self.status =''
		
	def new(self):
		self.status ='new'
		self.component('hull').title(unicode('新增区域'))
		pass 
	def show(self,id,name):
		self.status ='update'
		self.id = id
		self.enArea.setvalue(name)		
		self.component('hull').title(unicode('区域修改'))
		
	def onsave(self):
		name = self.enArea.getvalue().strip()
		if name=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('名称无效!'))			
			return 
		if self.status=='new':
			id =session.match(session.areas,'NAME','STRING',name,'ID')
			if id :
				tkMessageBox.showwarning(unicode('警告!'),unicode('区域名称已经存在!'))			
				return 
			sql = "insert into area (id,name) values(?,?)"
			data =[]
			data.append(['id',ado.INT,session.getsequence()])
			data.append(['name',ado.STRING,name])
			try:
				session.dbcnn.Execute(sql,data)
				tkMessageBox.showwarning(unicode(''),unicode('区域添加成功!'))							
			except:
				tkMessageBox.showwarning(unicode('警告!'),unicode('操作失败，无法添加区域!'))			
				return
		else:
			sql = "update area set name=:name where id=%s"%self.id
			data=[]
			data.append(['name',name])
			try:
				session.dbcnn.Execute2(sql,data)
				tkMessageBox.showwarning(unicode(''),unicode('区域修改成功!'))							
			except:
				tkMessageBox.showwarning(unicode('警告!'),unicode('修改失败!'))			
				return
							
		sql = "select * from area"
		session.areas = session.getdata(sql)
		session.user.load_area_rights()
		self.master.reload_area() 	#刷新区域信息列表

		self.destroy()
		
		
		
#############################################################################
class PaneWarningLevel(Toplevel):
	'''
		功能:显示和设置设备告警级别
			 
	'''
	def __init__(self,master):
		self.master = master
		Toplevel.__init__(self,master)		
		#数据定义
		self.id =0
		self.devinfo=None #当前设备记录
		#定义widget容器
		
		
		fall = Frame(self)
		fall.pack(fill='both',expand=1)
		
		f = Frame(fall)
		f.pack(fill='x',side='top',pady=4)
		self.title = Label(f,text='')
		self.title.pack(side='left')
		self.provider = ComboBox(f,label=unicode('设备厂商'),command=self.on_provider_sel)
		self.provider.pack()
		self.product = ComboBox(f,label=unicode('产品类型'),command=self.on_product_sel)
		self.product.pack()
		self.subtype = ComboBox(f,label=unicode('产品子类'),command=self.on_subtype_sel)
		self.subtype.pack()
		self.fbottom = Frame(fall)
		self.fbottom.pack(side='bottom',fill='x',padx=10,pady=10)
		self.apply = IntVar()
		Button(self.fbottom,text=unicode('关 闭'),command = self.onclose).pack(side='right')
		if session.user.has_rights(user.R_SYS_WARNINGLEVEL_SET):
			Button(self.fbottom,text=unicode('设 置'),command = self.onsave).pack(side='right')
		
		#参数的容器面板
		
		#self.fcontext = Frame(fall,relief='sunken',borderwidth=2)
		#self.fcontext.pack(fill='both',padx=10,pady=14)
		
		self.fcontext = ScrolledWindow(fall,scrollbar='auto')
		self.fcontext.pack(fill='both',padx=10,pady=14)
		self.fcontext = self.fcontext.window
		#fill='both',expand=1
		
		
		self.wm_protocol("WM_DELETE_WINDOW", lambda : self.onclose())
		self.wm_title(unicode('设备告警级别设置'))
		#初始设备厂商
		for i  in session.providers:
			self.provider.append_history(i['NAME'])
		self.list=[]
		self.devtype =0 	#当前选择类型
	
	def on_provider_sel(self,item):
		self.product.slistbox.listbox.delete(0,'end')
		providerid = session.match(session.providers,'NAME','STRING',self.provider.cget('value').strip(),'ID')		
		for i in session.products:
			if i['PROVIDER']==providerid:
				self.product.append_history(i['DESCRIPT'].strip())				
				
	def on_product_sel(self,item):		
		self.subtype.slistbox.listbox.delete(0,'end')
		
		
		productid= session.match(session.products,'DESCRIPT','STRING',self.product.cget('value').strip(),'ID')		
		
		for i in session.repeatertype:
			if i['PRODUCT_ID']==productid:				
				desc = constdef.dev_cat[str(i['DEVCAT'])]
				self.subtype.append_history(desc)				
				
	def on_subtype_sel(self,item):
		for i in self.list:
			i[1].destroy()
			i[2].destroy()
		self.list=[]
		
		devcat_id = constdef.dev_cat2[self.subtype.cget('value').strip()]
		productid= session.match(session.products,'DESCRIPT','STRING',self.product.cget('value').strip(),'ID')
		productid = int(productid)
		#4种设备命令参数都一样，不用区分
		self.devtype= session.match(session.repeatertype,'PRODUCT_ID','INT',productid,'TYPE_ID')		
		sql = "select * from warninglevel where repeatertype=%s"%self.devtype
		rs = session.getdata(sql)
		wl0 = 0
		wl1 = 0
		wl2 = 0
		wl3 = 0
		
		if len(rs)==0:
			wl0 = 0
			wl1 = 0
			wl2 = 0
			wl3 = 0
		else:			
			wl1 = rs[0]['NORMAL']
			wl2 = rs[0]['SLIGHT']
			wl3 = rs[0]['SEVERE']
		wl1 = long(wl1)
		wl2 = long(wl2)
		wl3 = long(wl3)
		
		sql = "select * from param_config where repeatertype=%s and is_warning=1 order by paramname"%self.devtype
		rs = session.getdata(sql)
		if len(rs)==0:
			return 
		
		
		for i in range(len(rs)):
			lb = Label(self.fcontext,text=rs[i]['DESCRIPT'])
			lb.grid(column=0,row=i,sticky='w')
			cb = ComboBox(self.fcontext)
			cb.grid(column=1,row=i,sticky='w')
			
			cb.append_history(unicode('屏蔽'))			
			cb.append_history(unicode('一般'))
			cb.append_history(unicode('重要'))
			cb.append_history(unicode('严重'))
			pick_item = 0
			idx = rs[i]['ORD']
			idx = int(idx)-1
			print wl1,rs[i]['ORD']
			print type(wl1),type(idx)
			if wl1&(1<<idx):
				pick_item=1
			elif wl2 & (1<<idx):	
				pick_item=2
			elif wl3 & (1<<idx):	
				pick_item=3
			cb.pick(pick_item)
					
			self.list.append([ rs[i]['PARAMNAME'],lb,cb])
			
			
	def onclose(self):
		session.form_warningflag =None
		self.destroy()
			
	#保存目前设置告警级别
	def onsave(self):
		if self.devtype==0:
			tkMessageBox.showwarning(unicode('警告!'),unicode('请选择设备类型!'))
			return 
	 	wl0 = 0
		wl1 = 0
		wl2 = 0
		wl3 = 0
		sql = "select * from param_config where repeatertype=%s and is_warning=1 order by paramname"%self.devtype
		rs = session.getdata(sql)
		if len(rs)==0:
			return 
		
		for i in range(len(self.list)):
			cb = self.list[i][2]
			item = cb.cget('value').strip()
			idx = rs[i]['ORD']
			idx = int(idx)-1			
			#idx = constdef.alarmflags.index(self.list[i][0])
			
			wl = 1<<idx
			if item==unicode('一般'):
				wl1 |=wl
			if item==unicode('重要'):
				wl2 |=wl
			if item==unicode('严重'):
				wl3 |=wl
		sql ="delete from warninglevel where repeatertype=%s"%self.devtype
		session.dbcnn.Execute(sql)
		sql = "insert into warninglevel (REPEATERTYPE,normal,slight,SEVERE) values(:repeatertype,:normal,:slight,:severe)"
		data=[]
		data.append(['repeatertype',self.devtype])		
		data.append(['normal',wl1])		
		data.append(['slight',wl2])		
		data.append(['severe',wl3])		
		
		try:
			session.dbcnn.Execute2(sql,data)
			log.recLog(str(''),log.LOG_WARNINGLEVEL_MODIFY)	
			tkMessageBox.showwarning('',unicode('告警级别设置成功'))			
		except:
			tkMessageBox.showwarning('',unicode('告警级别设置失败!'))
			return 
		

class PaneSysSet(Toplevel):
	def __init__(self,master):
		Toplevel.__init__(self,master)		
		f = Frame(self)
		f.pack(fill='both',expand=1,padx=10,pady=10)
		
	