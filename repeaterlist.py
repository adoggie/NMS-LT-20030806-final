

from Tix import *
import tkMessageBox
import Pmw

import devinfo
import constdef
import login
import net_train
import ado
import session
import user
import systemset
import dev_inner_params

##
#class PaneCareSubDev(Pmw.MegaToplevel):
#	def __init__(self,master):
#		Pmw.MegaToplevel.__init__(self,master)
#		self.master = master
#		f =Frame(self.component('hull'))
#		f.pack(fill='x',side='bottom',padx=4,pady=4)
#		Button(f,text=unicode('确定'),command= self.onsave).grid(column=0,row=0)
#		Button(f,text=unicode('取消'),command=lambda :self.destroy()).grid(column=1,row=0)
#		f = Frame(self.component('hull'))
#		f.pack(fill='both',padx=4,pady=4)
#		self.enArea = Pmw.EntryField(f,labelpos = 'w',label_text=unicode('设备编号:'),validate = {'validator' : 'integer',
#                        'min' : 0, 'max' : 6, 'minstrict' : 0})
#
#		
#		self.enArea.pack(fill='x',expand=1)
#		self.enSite = Pmw.EntryField(f,labelpos = 'w',label_text=unicode('放置地点:'),validate = {'max':50})		
#		self.enSite.pack(fill='x')
#		self.status =''
#		self.parentid =0	#主设备编号
#		
#	def new(self,parentid):
#		self.parentid = parentid
#		self.status ='new'
#		self.component('hull').title(unicode('新增设备'))
#		pass 
#	def onsave(self):
#		if not self.enArea.valid():
#			tkMessageBox.showwarning(unicode('警告!'),unicode('设备编号无效!'))			
#			return 
#		
#		equipmentid = int(self.enArea.getvalue())
#		#设备安装地点
#		site = self.enSite.getvalue()
#		#检测设备号是否存在
#		sql ="select count(*) as cnt from repeaterinfo where parent_id=%s and equipment_id=%s"%(self.parentid,equipmentid)
#		rs = session.getdata(sql)
#		if rs[0]['CNT']!=0:
#			tkMessageBox.showwarning(unicode(''),unicode('设备编号已存在!'))						
#			return 
#		####
#		
#		sql = "select * from repeaterinfo where id=%s"%self.parentid
#		rs = session.getdata(sql)
#		parentdev = rs[0]
#		
#		repeatertype=0
#		devcat = 0
#		if parentdev['DEVCAT']==1:
#			devat=2
#		if parentdev['DEVCAT']==5:
#			devcat=6
#		parentid = self.parentid
#		
#		query_interval = parentdev['QUERY_INTERVAL']
#		
#		sql = "select type_id from repeatertype where product_id=%s and  devcat=%s"%(parentdev['PRODUCT_ID'],devcat)
#		rs = session.getdata(sql)
#		repeatertype = int(rs[0]['TYPE_ID'])
#		id = session.getsequence()
#		
#		sql = "insert into repeaterinfo  (id,repeatertype,parent_id,equipment_id,devcat,query_interval,site) values(:id,:repeatertype,:parent_id,:equipment_id,:devcat,:query_interval,:site)"
#		
#		
#		data =[]
#		data.append(['id',id])
#		data.append(['repeatertype',repeatertype])
#		data.append(['parent_id',parentid])
#		data.append(['equipment_id',equipmentid])
#		data.append(['devcat',devcat])
#		data.append(['query_interval',query_interval])
#		data.append(['site',site])
#		
#		try:
#			session.dbcnn.Execute2(sql,data)
#			tkMessageBox.showwarning(unicode(''),unicode('设备添加成功!'))						
#			session.user.load_repeaters()
#			str ="0,1,2,3,%s,4,5,6,7,8"%constdef.cmd_list["UPDATE_DEV_LIST"]		
#			if net_train.send2mss(str)==0:
#				tkMessageBox.showwarning(unicode('警告'),unicode('通知MSS失败!'))				
#
#		except:
#			tkMessageBox.showwarning(unicode('警告!'),unicode('操作失败，无法添加设备!'))			
#		self.destroy()
#		

		


#单设备
class SingleDev(Button):
	def __init__(self,owner,data,master):
	
		Button.__init__(self,owner)
		
		#读取单个设备
		self.master = master
		self.data = data
		
		#设置告警颜色
		self.config(state='normal')
		self.config(fg='white')
		warningtype = session.get_warning_type(data['ID'])
		if warningtype==None:
			warningtype=0
		self.config(background=constdef.WCOLOR[str(warningtype)])
		self.pi = PhotoImage(file='./rc/alert_%s.gif'%warningtype)
		if self.data['PARENT_ID']==0:				
			self.config(image =self.pi)						
			pass
		else:
			self.config(font=('宋体',8))
			self.config(text=self.data['EQUIPMENT_ID'])							
			self.config(fg='black')							
			
		
		self.config(command=lambda: self.onlmouse(self))
		self.config(relief='raised')
		
		pass

	def onsel(self):
		tkMessageBox.showwarning('','error')		
		
	#左键安下
	def onlmouse(self,ev):
		
		self.menu_info =Menu(self,selectcolor='red',tearoff=0)	
		s = self.data['REPEATER_ID']
			
		if s==None:
			s=''
		else:
			s = str(s)
			self.menu_info.add_command(label=(unicode('直放站编号:')+s))
			
		s = self.data['REPEATER_PHONE']
		if s==None:
			s=''
		else:
			s = s.strip()
			self.menu_info.add_command(label=(unicode('设备电话:')+s))		

		site = self.data['SITE']
		if site==None:
			site =""
		else:
			site = site.strip()
		self.menu_info.add_command(label=(unicode('放置地点:')+site))
		self.menu_info.add_separator()
		self.menu_info.add_command(label=unicode('刷新'),command=lambda:self.master.reload(self.data['ID']))
		self.menu_info.add_command(label=unicode('设备信息'),command=self.onmodify)
		
		if session.user.has_rights(user.R_DEV_DEL):
			self.menu_info.add_command(label=unicode('删除'),command= self.ondel)	
		
		self.menu_info.add_separator()
		if session.user.has_rights(user.R_DEV_STATUS_QUERY):
			self.menu_info.add_command(label=unicode('发送状态查询'),command=lambda :session.query_it(self.data['ID']))		
		if session.user.has_rights(user.R_DEV_PARAM_QUERY):
			self.menu_info.add_command(label=unicode('发送系统参数查询'),command= lambda:session.query_netparam(self.data['ID']))		
		self.menu_info.add_separator()
		self.menu_info.add_command(label=unicode('状　态'),command=self.onstatus)		
		self.menu_info.add_command(label=unicode('系统设置'),command=self.onsysset)		


		self.menu_info.post(self.winfo_pointerx(),self.winfo_pointery())
		

	
		
	def onsysset(self):
		if session.form_sys_set==None:
			session.form_sys_set =dev_inner_params.PaneInnerParams(session.root)
#		session.form_warningflag.deiconify()
#		session.form_warningflag.transient(self)
		session.form_sys_set.lift()
		session.form_sys_set.show(int(self.data['ID']))
	
		
	#显示状态信息		
	def onstatus(self):
		if session.form_status==None:
			session.form_status =systemset.PaneStatus(session.root)
#		session.form_status.deiconify()
#		session.form_status.transient(self)
		session.form_status.lift()
		session.form_status.show_status(int(self.data['ID']))
	
		
	#删除设备
	def ondel(self):
		masterdevid = 0
		sql =  ""
		if self.data['PARENT_ID']==0:
			if tkMessageBox.askyesno(unicode('警告!'),unicode('直放站包含多个设备,本次操作将删除所有子设备,是否真的删除?')) ==0:
				return
			
			masterdevid = self.data['ID']
		else:
			masterdevid = self.data['PARENT_ID']		
		
		sql = "delete from repeaterinfo where id=%s or parent_id=%s"%(self.data['ID'],self.data['ID'])					
		try:
			session.dbcnn.Execute2(sql)				
			session.user.load_repeaters()	#重新加载用户管理设备清单
			
		except:
			tkMessageBox.showinfo(unicode('警告!'),unicode('删除失败'))
			return
		#print "ondel()==",masterdevid
		self.master.reload(masterdevid)
	#修改设备信息

	def onmodify(self):
		pdi = devinfo.PaneDevInfo(session.root)
		pdi.show(self.data['ID'])
		pdi.activate()
		if pdi.save_to_close:
			self.master.reload(self.data['ID'])

class Repeater(Frame):
	def __init__(self,owner,devid,master):
		Frame.__init__(self,owner)
		self.master = master
		self.devid = devid
		self.name =''
		self.devs=[]	
		self.dev=None	#主设备	
		self.desc =None
		self.fslaves =None	
			
		self.reload(self.devid)
		
	def __del__(self):
		self.clear()
		self.destroy()		
			
		

	#晴空所有设备信息
	def clear(self):
		for  w in self.devs:
			w.destroy()
			w=None
		if self.dev:
			self.dev.destroy()
			self.dev =None
		if self.desc:
			self.desc.destroy()
			self.desc =None
		
	#加载设备信息
	def reload(self,id):
		self.clear()	#删除所有子部件

		data=None		

		for i in session.user.repeaters:	
			if i['ID']==id:
				data = i


				
		#当用户手动删除主机的时候，刷新设备列表区域
		if data==None:
			self.master.reflash()
			return
		
		
		self.name = data['NAME']
		self.name = self.name.strip()
		
		dev = SingleDev(self,data,self)
		self.devs.append(dev)
		dev.pack()		#加主设备
		
		
		self.desc = Label(self,text=self.name,font=(unicode('宋体'),9))
		self.desc.pack()


								

class RepeaterList(Frame):
	def __init__(self,master):		
		Frame.__init__(self,master)
		self.sb =Scrollbar(self)
		self.sb.pack(side='left',fill='y')
		self.tl = TList(self,orient='horizontal',padx=10,pady=10,yscrollcommand=self.sb.set )
		self.tl.pack(side='left',fill='both',expand=1)
		self.sb['command']=self.tl.yview
		self.devlist =[]
		self.area_id =0		#显示区域
		self.warningtype =0 #显示告警类别
		
#		for i in range(100):
#			self.tl.insert('end',itemtype='window',window=Repeater(self.tl))
#			
	def show(self,area_id,warningtype,show_no_response=0):
		''' 显示设备信息  '''
		
		self.area_id = area_id
		self.warningtype = warningtype
		self.show_no_response = show_no_response
		#删除所有显示的设备
		dev_cnt = self.tl.tk.call(self.tl,'info','size')
		for i in range(int(dev_cnt)):
			w = self.tl.tk.call(self.tl,'entrycget',i,'-window')
			w = self.nametowidget(w)
			w.__del__()
			w.destroy()
			
		self.tl.delete(0,'end')
		self.devlist=[]
		
		list=[]
		for i in session.user.repeaters:			
			if i['AREA_ID']==area_id:				
				list.append(i)
		if warningtype ==-1:  #显示所有的设备，不区分是否告警
			if show_no_response==0:	#选择了显示区域的按钮
				self.devlist = list
			else:	#显示响应超时设备
				for i in session.user.repeaters:					
					if i['AREA_ID']==area_id:										
						if session.is_timeout(i['ID']): 
							self.devlist.append(i)
				
		else:
		#判断设备告警级别,选择了4种告警类型之一
			for i in list:
				wl=0
				for i2 in session.current_dev_statuses:
					if i['ID']==i2['REPEATER_ID']:
						if i2['WARNINGLEVEL']==None:
							wl =0	#由于状态表告警类别为NUll
						else:
							wl = i2['WARNINGLEVEL']
				if wl==warningtype:
					self.devlist.append(i)
		#print "devs cnt %s by warningtype"%len(self.devlist)							
		
		for i in self.devlist:
			r = Repeater(self.tl,i['ID'],self)	#添加设备		
			self.tl.insert('end',itemtype='window',window=r)
		
			
	def reflash(self):
		''' reflash all repeaters status '''
		
		self.show(self.area_id,self.warningtype,self.show_no_response)
		
		
		
		

 