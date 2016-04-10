

###
#   包括系统基础信息的维护
####

from Tix import *
import Pmw
import tkMessageBox
import re
import constdef
import login
import net_train
import ado
import session
import user
import log
####################################################################################
class PaneDevInfo(Pmw.MegaToplevel):
	'''设备信息'''			
	save_to_close=0	# 标示选择保存而关闭窗体
	def __init__(self,master):
		Pmw.MegaToplevel.__init__(self,master)
		tp = self.component('hull')
		tp.title(unicode('设备信息'))
		self.nb = NoteBook(tp)
		self.nb.pack(fill='both',side='top',expand=1,padx=10,pady=10)
		self.p1 = self.nb.add('status',label=unicode('基础信息'))
		#self.p2 = self.nb.add('control',label=unicode('告警使能标志'))
		
		f=Frame( self.p1)
		f.pack(fill='both',padx=10,pady=10)
		
		Label(f,text=unicode('设备名称:'),anchor='e').grid(column=0,row=0,sticky='e')		
		self.devname= Pmw.EntryField(f,validate={'max':20})
		self.devname.grid(column=1,row=0,sticky='w',padx=10) 

#		Label(f,text=unicode('直放站编号:'),anchor='e').grid(column=0,row=1,sticky='e',pady=2)						
#		self.devno= Pmw.EntryField(f,validate={'max':10000,'min':0,'validator':'integer'})
#		self.devno.grid(column=1,row=1,sticky='w',padx=10) 
		
		Label(f,text=unicode('设备厂商:'),anchor='e').grid(column=0,row=2,sticky='e',pady=2)		
		self.manufaturer= ComboBox(f,command=self.onselprovider)
		self.manufaturer.grid(column=1,row=2,sticky='w',padx=6) 
		Label(f,text=unicode('设备型号:'),anchor='e').grid(column=0,row=3,sticky='e',pady=2)		
		self.devtype = ComboBox(f)
		self.devtype.grid(column=1,row=3,sticky='w',padx=6) 
		
#		Label(f,text=unicode('设备编号:'),anchor='e').grid(column=0,row=4,sticky='e',pady=2)		
#		self.subdevno= Pmw.EntryField(f,validate={'max':10000,'min':0,'validator':'integer'})
#		self.subdevno.grid(column=1,row=4,sticky='w',padx=10) 
		
		Label(f,text=unicode('隶属区域:'),anchor='e').grid(column=0,row=5,sticky='e',pady=2)
		self.area = ComboBox(f)
		self.area.grid(column=1,row=5,sticky='w',padx=6) 
		
		Label(f,text=unicode('放置地点:'),anchor='e').grid(column=0,row=6,sticky='e',pady=2)
		self.site= Pmw.EntryField(f,validate={'max':50})
		self.site.grid(column=1,row=6,sticky='ew',padx=10) 


		Label(f,text=unicode('运行日期:'),anchor='e').grid(column=0,row=7,sticky='e',pady=2)
		self.runtime= Pmw.EntryField(f,value='2000/01/01',validate = {'validator' : 'date',
                        'min' : '1900/1/1', 'max' : '2010/12/31',
                        'minstrict' : 0, 'maxstrict' : 0,
                        'format' : 'ymd'})
		self.runtime.grid(column=1,row=7,sticky='ew',padx=10) 

		
#		Label(f,text=unicode('通信模式:'),anchor='e').grid(column=0,row=8,sticky='e',pady=2)
#		self.commtype = ComboBox(f)
#		self.commtype.grid(column=1,row=8,sticky='w',padx=6) 

		Label(f,text=unicode('设备电话:'),anchor='e').grid(column=0,row=9,sticky='e',pady=2)
		self.devphone= Pmw.EntryField(f,validate={'max':'999999999999999','validator':'integer'})		
		self.devphone.grid(column=1,row=9,sticky='w',padx=10)

#		Label(f,text=unicode('监控中心查询电话:'),anchor='e').grid(column=0,row=10,sticky='e',pady=2)
#		self.queryphone= Pmw.EntryField(f,validate={'max':'999999999999999','validator':'integer'})
#		self.queryphone.grid(column=1,row=10,sticky='w',padx=10)
#		Label(f,text=unicode('监控中心告警电话:'),anchor='e').grid(column=0,row=11,sticky='e',pady=2)
#		self.alertphone= Pmw.EntryField(f,validate={'max':'999999999999999','validator':'integer' })
#		self.alertphone.grid(column=1,row=11,sticky='w',padx=10)
		
		Label(f,text=unicode('轮询时间(分钟):'),anchor='e').grid(column=0,row=12,sticky='e',pady=2)
		self.query_interval= Pmw.EntryField(f,validate={'max':10000,'min':0,'validator':'integer'})
		self.query_interval.grid(column=1,row=12,sticky='w',padx=10) 
		f = Frame(tp)
		f.pack(fill='x')
		
		if session.user.has_rights(user.R_DEV_MODIFY) or session.user.has_rights(user.R_DEV_ADD):			
			Button(f,text=unicode('存储'),command=self.onsave).grid(column=0,row=1)
		Button(f,text=unicode('关闭'),command = lambda : self.destroy()).grid(column=1,row=1)
		#--------------------------------------------------------------
		#加载数据
#		for (k,v) in session.query_interval.items():			
#			self.query_interval.append_history(k+'-'+str(v))
#		self.query_interval.pick(0)
		
		for i in session.providers:
			self.manufaturer.append_history(i['NAME'].strip())
		
#		self.manufaturer.pick(0)
		
		for i in session.areas:
			self.area.append_history(i['NAME'].strip())
		self.area.pick(0)
		
#		for (k,v) in constdef.COMM_MODE_BY_ID.items():
#			self.commtype.append_history(v)
#		self.commtype.pick(0)
		
		
		self.devinfo =None
		#self.show(3474)
		
	def onselprovider(self,val):
		providerid = session.match(session.providers,'NAME','STRING',self.manufaturer.cget('value').strip(),'ID')
		self.devtype.slistbox.listbox.delete(0,'end')
		for i in session.products:
			if i['PROVIDER']==providerid:
				self.devtype.append_history(i['DESCRIPT'].strip())				

		
	def show(self,devid):
		''' 显示指定的设备信息，只显示主设备信息 '''
		sql ="select * from repeaterinfo where id =%s"%devid
		devs = session.getdata(sql)
		if len(devs)==0:
			return
		self.devinfo = devs[0]
		
		self.devname.setentry(self.devinfo['NAME'].strip())		
		#self.devno.setentry(self.devinfo['REPEATER_ID'])		
		self.manufaturer.configure(value=session.match(session.providers,'ID','INT',self.devinfo['PROVIDER_ID'],'NAME'))
		#显示指定厂商的产品型号
		
		self.devtype.slistbox.listbox.delete(0,'end')		
		for i in session.products:
			if self.devinfo['PROVIDER_ID']==i["PROVIDER"]:
				self.devtype.append_history(i['DESCRIPT'])	
				if 	self.devinfo['PRODUCT_ID']==i['ID']:
					self.devtype.configure(value= i['DESCRIPT'])
		
		
		#self.subdevno.setentry( self.devinfo['EQUIPMENT_ID'] )
		self.area.configure(value=session.match(session.areas,'ID','INT',self.devinfo['AREA_ID'],'NAME'))
		self.site.setentry(self.devinfo['SITE'])
		time = self.devinfo['RUN_DATE']
		time = time.Format('%Y/%m/%d')
		self.runtime.setentry(time)	
		#self.commtype.config(value =  constdef.COMM_MODE_BY_ID[str(self.devinfo['COMM_MODE'])] )
		self.devphone.setentry(self.devinfo['REPEATER_PHONE'].strip())
		#self.queryphone.setentry(self.devinfo['QUERY_PHONE'].strip()) 
		#self.alertphone.setentry(self.devinfo['ALARM_PHONE'].strip()) 
		self.query_interval.setentry(self.devinfo['QUERY_INTERVAL'] )
		
		pass
		
		
	#检测数据是否有效
	def check(self,type):
		
		if self.devname.getvalue().strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('设备名称不能为空!'))				
			return 0
#		if self.devno.getvalue().strip()=='':
#			tkMessageBox.showwarning(unicode('警告!'),unicode('直放站编号不能为空!'))				
#			return 0
		
		if self.manufaturer.cget('value').strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('设备厂商不能为空!'))				
			return 0
		
		if self.devtype.cget('value').strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('设备型号不能为空!'))				
			return 0
		if self.area.cget('value').strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('隶属区域不能为空!'))				
			return 0
		
#		if self.subdevno.getvalue().strip()=='':
#			tkMessageBox.showwarning(unicode('警告!'),unicode('设备名称不能为空!'))				
#			return 0
		if self.area.cget('value').strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('设备编号不能为空!'))				
			return 0
		
		if self.site.getvalue().strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('放置地点不能为空!'))				
			return 0
		if self.runtime.getvalue().strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('运行日期不能为空!'))				
			return 0
#		if self.commtype.cget('value').strip()=='':
#			tkMessageBox.showwarning(unicode('警告!'),unicode('通信模式不能为空!'))				
#			return 0
			
		if self.devphone.getvalue().strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('设备电话不能为空!'))				
			return 0
#		if self.queryphone.getvalue().strip()=='':
#			tkMessageBox.showwarning(unicode('警告!'),unicode('监控中心查询电话不能为空!'))				
#			return 0
#		if self.alertphone.getvalue().strip()=='':
#			tkMessageBox.showwarning(unicode('警告!'),unicode('监控中心告警电话不能为空!'))				
#			return 0
		if self.query_interval.getvalue().strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('轮询时间不能为空!'))				
			return 0
		
		
		
		
		sql =''
		#--------------------------------------------------------------			
		if type.upper().strip()=='INSERT':
			sql ="select count(*) as cnt from repeaterinfo where parent_id=0 and name='%s' "%self.devname.getvalue().strip()
		elif type.upper().strip()=='UPDATE':
			sql ="select count(*) as cnt from repeaterinfo where parent_id=0 and name='%s' and id<>%s"%(self.devname.getvalue().strip(),self.devinfo['ID'])	
		rs = session.getdata(sql)
		rs =rs[0]
		
		if int(rs['CNT'])!=0:
			tkMessageBox.showwarning(unicode('警告!'),unicode('相同设备名称存在!'))				
			del rs
			return 0
			
		return 1
		
	#----------------------------------------------------------------			
	def onsave(self):
		'''数据储存'''
		save_to_close=1
		sql =''
		data=[]
		id =0
		
		
		
		if self.devinfo!=None:
			if self.check('UPDATE')==0:
				return 
			else:
				# do update 
				sql = """
						update repeaterinfo  set 
						NAME=:NAME,
						REPEATERTYPE=:REPEATERTYPE,						
						AREA_ID=:AREA_ID,						
						RUN_DATE=:RUN_DATE,
						REPEATER_PHONE=:REPEATER_PHONE,						
						PRODUCT_ID=:PRODUCT_ID,
						PROVIDER_ID=:PROVIDER_ID,
						QUERY_INTERVAL=:QUERY_INTERVAL,
						SITE=:SITE 
						where id=%s 
						"""%self.devinfo['ID']
		else:
			if self.check('INSERT')==0:
				return 		
			else:
				sql ="""
						insert into repeaterinfo 
						(ID,NAME,REPEATERTYPE,AREA_ID,
						RUN_DATE,REPEATER_PHONE,
						PRODUCT_ID,PROVIDER_ID,
						QUERY_INTERVAL,SITE) 
						values(:ID,:NAME,:REPEATERTYPE,:AREA_ID,
						:RUN_DATE,:REPEATER_PHONE,
						:PRODUCT_ID,:PROVIDER_ID,
						:QUERY_INTERVAL,:SITE)
					"""
				id = session.getsequence()
				data.append(['ID',id])
				
		data.append(['NAME',self.devname.getvalue().strip()])
		providerid = session.match(session.providers,'NAME','STRING',self.manufaturer.cget('value').strip(),'ID')
		productid =   session.match(session.products,'DESCRIPT','STRING',self.devtype.cget('value').strip(),'ID')
		repeatertype = 0
		devcat =0
		subdevno =0 #设备编号
		for i in session.repeatertype:#查找设备类别
			if providerid==i['PROVIDER'] and productid==i['PRODUCT_ID']:				
				repeatertype=i['TYPE_ID']
				devcat =8
					
		data.append(['REPEATERTYPE',int(repeatertype)])
		
		area_id = session.match(session.areas,'NAME','STRING',self.area.cget('value').strip(),'ID')
		data.append(['AREA_ID',int(area_id)])
		
		data.append(['RUN_DATE',self.runtime.getvalue()])
		data.append(['REPEATER_PHONE',self.devphone.getvalue()])
		data.append(['PRODUCT_ID',productid])
		data.append(['PROVIDER_ID',providerid])
		data.append(['QUERY_INTERVAL',int(self.query_interval.getvalue())])
		data.append(['SITE',self.site.getvalue()])
		#print data
		try:
			session.dbcnn.Execute2(sql,data)		
		except:
			tkMessageBox.showwarning(unicode('警告'),unicode('数据操作失败 !'))				
			return
		


		if self.devinfo!=None:
			id = int(self.devinfo['ID'])

		#更新当前记录
		sql ="select * from repeaterinfo where id =%s"%id
		devs = session.getdata(sql)
		self.devinfo = devs[0]

		#更新设备缓存信息
		session.user.load_repeaters()


		# send updatelist package to mss 
		str ="0,1,2,3,%s,4,5,6,7,8"%constdef.cmd_list["UPDATE_DEV_LIST"]
		
		if net_train.send2mss(str)==0:
			tkMessageBox.showwarning(unicode('设备更新'),unicode('通知MSS失败!'))				
			return 
		
			
		

		#窗口关闭
		self.destroy()

		



