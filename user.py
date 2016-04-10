


#############################################
#
#	用户功能管理
#
#
import string
import session
import ado
from Tix import *
import Pmw
import tkMessageBox
import constdef
import copy


###################################################################
#	1	设备告警使能标志设置
#	2	设备控制
#	3	设备网管参数查询
#	4	设备状态查询
#	5	告警通知设置
#	6	用户账号管理
#	7	登录密码修改
#	8	设备告警级别设置
#	9	网管中心信息修改
#	10	系统运行参数设置
#	11	区域添加
#	12	区域修改
#	13	区域删除
#	41	设备添加
#	42	设备修改
#	43	设备删除
#	21	日志-设备状态查询
#	22	日志-设备告警查询
#	23	日志-设备控制查询
#	31	日志-管理员登录查询
#	32	日志-管理员历史操作查询
#
###################################################################
R_DEV_ALARM_FLAG_SET=1
R_DEV_CONTROL=2
R_DEV_PARAM_QUERY=3
R_DEV_STATUS_QUERY=4
R_USER_MANAGE=6
R_USER_CHANGE_PSW=7
R_SYS_WARNINGLEVEL_SET=8
R_NETCENTER_SET=9
R_SYS_RUN_PARAM_SET = 10
R_AREA_ADD=11
R_AREA_MODIFY=12
R_AREA_DEL=13
R_DEV_ADD=41
R_DEV_MODIFY=42
R_DEV_DEL=43
R_LOG_STAUTS=21
R_LOG_ALARM=22
R_LOG_CONTROL=23
R_LOG_LOGIN=31
R_LOG_USER_OPERATION=32




class User:
	def __init__(self,id):
		pado = ado.PAdo(session.dbcnnstr)
		self.id = None
		self.login_name=None
		self.psw =None
		self.real_name =None
		self.tel =None
		self.provider = None
		self.set={}
		#print 'select * from userinfo where id=%s'%id
		#读取用户信息
		rs = pado.Select('select * from userinfo where id=%s'%id)		
		while not rs.EOF:		
			self.id = rs.Fields.Item('id').Value			
			self.login_name=rs.Fields.Item('LOGIN_NAME').Value				
			self.psw = rs.Fields.Item('PSW').Value	
			self.real_name = rs.Fields.Item('REAL_NAME').Value			
			self.tel = rs.Fields.Item('TEL').Value			
			self.provider = rs.Fields.Item('PROVIDER').Value			
			self.set={'login_name':self.login_name,'psw':self.psw,'real_name':self.real_name,'tel':self.tel,'provider':self.provider}
			rs.MoveNext()
		rs = None
		self.load_area_rights()
		self.load_repeaters()
		#print sql
	def load_area_rights(self):
		#取可操作区域	
		
		sql = 	"select a.area_id as id,b.name from userarea a,area b,userinfo c \
				where a.user_id=%s  and a.user_id=c.id and a.area_id = b.id "%self.id
		if self.login_name=='admin' or self.login_name=='super' or self.provider!=0:
			sql = "select * from area"
		sql =sql.upper()
		#print sql
		self.areas = None
		self.areas = session.getdata(sql)
		#print self.areas
		
		sql ="select a.rights_id as id,b.name from userrights a, rights b,userinfo c where a.user_id=%s  and a.user_id=c.id and a.rights_id = b.id "%self.id		
		
		if self.login_name=='admin' or self.login_name=='super':
			sql = "select * from rights"
		sql =sql.upper()
		self.rights = session.getdata(sql)
		##########################
	#加载当前用户管理的设备列表
	def load_repeaters(self):
		self.repeaters=None
		if self.provider==0:	#区域管理员
			case =[]
			for i in self.areas:
				case.append("area_id="+str(i['ID']))
				
			
			sql ="SELECT * FROM REPEATERINFO  WHERE "
			sql+=" parent_id in "
			sql+="(select id from repeaterinfo where parent_id=0 and (%s)) "
			sql+=" or (%s)"
			sql+=" ORDER BY NAME "
			sql = sql%(string.join(case," or "),string.join(case," or "))
			

		else:#厂商管理员
			sql = "select * from repeaterinfo a "
			sql+=" where a.parent_id in (select id from repeaterinfo where parent_id=0 and provider_id=%s) " 
			sql+="		or  a.provider_id=%s"
			sql = sql%(self.provider,self.provider)
		self.repeaters =None
		self.repeaters = session.getdata(sql)
		
	
	def has_rights(self,id):
		for i in self.rights:
			
			if int(i['ID'])==int(id):
				return 1
		return 0
		
		
	def get_areas(self):
		return self.areas
		
	def get_rights(self):
		return self.rights


#------------------------------------------------------------------------------------------------
#'''当前用户修改登录密码'''
class PaneChangePsw(Pmw.MegaToplevel):
	'''当前用户修改登录密码'''
	def __init__(self,master):
		Pmw.MegaToplevel.__init__(self,master)
		self.master = master
		self.user =None
#		self.master = master		
#		########################################################
#		#标题栏
#		frmtitle =Frame(self)
#		frmtitle.pack(side='top')
#		
#		########################################################3
		tp = self.component('hull')
		tp.title(unicode('登录密码修改'))
		f = Frame(tp)
		f.pack(fill='x',side='bottom',expand=1,padx=10,pady=4)
		self.usr = Pmw.EntryField(f,labelpos = 'w',label_text=unicode('当前登录用户:'),validate={'max':20})
		self.usr.pack(pady=2)
		self.oldpsw = Pmw.EntryField(f,labelpos = 'w',label_text=unicode('旧密码:'),validate={'max':20})
		self.oldpsw.pack(pady=2)
		self.oldpsw.component('entry').config(show='*')
		self.newpsw = Pmw.EntryField(f,labelpos = 'w',label_text=unicode('新密码:'),validate={'max':20})
		self.newpsw.pack(pady=2)
		self.newpsw.component('entry').config(show='*')
		self.newpsw2 = Pmw.EntryField(f,labelpos = 'w',label_text=unicode('确认新密码:'),validate={'max':20})
		self.newpsw2.pack(pady=2)
		self.newpsw2.component('entry').config(show='*')
		Pmw.alignlabels((self.usr,self.oldpsw,self.newpsw,self.newpsw2))
		
		f = Frame(f)
		f.pack(pady=10)
		Button(f,text=unicode('关闭'),command=lambda :self.destroy()).pack(side='right',padx=4)
		Button(f,text=unicode('修改'),command=self.save).pack(side='right',padx=4)
		
		#print self.master.winfo_geometry()
		
	def show_user(self,user):	
		self.user = user	
		self.usr.setentry(self.user.login_name)
		#print self.master.winfo_geometry()
	def save(self):
		#校验数据
		
		if self.oldpsw.getvalue()!=self.user.psw:
			tkMessageBox.showwarning(unicode('警告!'),unicode('请输入正确的原始密码'))
			return
		if self.newpsw.getvalue()!=self.newpsw2.getvalue():
			tkMessageBox.showwarning(unicode('警告!'),unicode('新密码与确认密码不一致'))
			return
		sql = "update userinfo set psw=? where id=%s"%self.user.id		
		try:
			session.dbcnn.Execute(sql,[ ['psw',ado.STRING,self.newpsw.getvalue()] ])		
		except:
			tkMessageBox.showwarning(unicode('警告!'),unicode('操作失败!'))
			return
		tkMessageBox.showwarning(unicode(''),unicode('密码修改成功!'))	
		self.destroy()			
		pass
		
#------------------------------------------------------------------------------------------------
class myCheckList(ScrolledHList):
	def __init__(self,master):
		ScrolledHList.__init__(self,master,options='hlist.columns 2')
		self.master = master
		self.ck_ar=[]
		
	def add(self,path,caption):
		ckvar=IntVar()
		ck = Checkbutton(self.hlist,variable=ckvar,font=('宋体',4),background='SystemWindow')
		self.ck_ar.append([path,ck,ckvar])
		self.hlist.add(path,itemtype='window',window=ck)
		self.hlist.item_create(path,1,itemtype='text',text=caption)
		
	def setstatus(self,path,status='on'):
		hlist = self.hlist
		w_ck = hlist.tk.call(hlist,'entrycget',path,'-window')
		
		st = 0
		if status=='on':
			st=1
		for ck in self.ck_ar:
			if str(ck[1])==w_ck:
				ck[2].set(st)
				break
	def getselection(self):
		selected =[]
		for i in self.ck_ar:
			if i[2].get()==1:
				selected.append(i[0])
		return selected 	
	
#'''用户信息维护'''

class PaneCareUser(Frame):
	'''用户信息维护'''
	def __init__(self,master):
		Frame.__init__(self,master)
		
		self.allusers=[]
		
		self.create_widgets()
		
		
	
	def create_widgets(self):
		#tp = self.component('hull')
		#tp.option_add('*Font',('宋体',10))
		
		fbottom = Frame(self)
		fbottom.pack(side='bottom',fill='x',expand=1)
		
		fcmd = Frame(fbottom)
		fcmd.pack(side='bottom',fill='x',pady=8)
		Button(fcmd,text=unicode('删除'),width=6,command= self.ondel).grid(column=0,row=0,padx=4)
		#Button(fcmd,text=unicode('新增'),width=6).grid(column=1,row=0,padx=4)
		Button(fcmd,text=unicode('存储'),width=6,command=self.onsave).grid(column=2,row=0,padx=4)


		ftop = Frame(self)
		ftop.pack(fill='both',padx=10,pady=10)
		#======================================
			

		
#		flist = Frame(f)
#		flist.pack(fill='both',expand=1)
		self.shl = ScrolledHList(ftop,scrollbar='both')
		self.shl.hlist.config(command =self.onseluser) 
		self.shl.pack(side='left',fill='y',expand=1)
		#global pi
		self.pi =PhotoImage(file='./rc/icon.gif')
		####显示当前所有用户列表
		sql = "select * from userinfo where login_name<>'admin' and login_name<>'super' order by real_name"
		sql = sql.upper()
		self.userlist = session.getdata(sql)
		for i in self.userlist:
			self.shl.hlist.add(str(i['ID']),itemtype='imagetext',image=self.pi,text=i['REAL_NAME'])
			
		#===============================================
		
		fright = Frame(ftop)
		fright.pack(fill='both',expand=1,padx=10)
		
		
		
		f = Frame(fright)		
		f.pack(fill='both',expand=1,padx=8,pady=10)
		
		self.login_name = Pmw.EntryField(f,labelpos='w',label_text=unicode('登录用户:'),
									validate = {'validator' : 'alphanumeric', 'max' :20})
		self.login_name.pack(fill='x',pady=2)
		self.psw = Pmw.EntryField(f,labelpos='w',label_text=unicode('登录密码:'),
							validate = {'validator' : 'alphanumeric', 'max' :20})
		self.psw.pack(fill='x',pady=2)
		
		self.real_name = Pmw.EntryField(f,labelpos='w',label_text=unicode('用户实名:'),
							validate = { 'max' :20})
							
		self.real_name.pack(fill='x',pady=2)
		
		self.tel= Pmw.EntryField(f,labelpos='w',label_text=unicode('联系电话:'),
						validate = { 'max' :20})
		self.tel.pack(fill='x',pady=2)
		
		ftype = Frame(f)
		ftype.pack(fill='x')
		self.user_type = ComboBox(ftype,label=unicode('用户类别:'),command=self.onseltype)		
		self.user_type.pack(side='left')
		self.user_type.append_history(unicode('区域管理员'))
		self.user_type.append_history(unicode('厂商管理员'))
		
		self.provider= ComboBox(ftype,label=unicode('设备厂商:'))		
		self.provider.pack(side='top',padx=10)
		#显示设备厂商
		sql = "select * from provider order by name"
		sql = sql.upper()
 		self.provider_list = session.getdata(sql)
		for i in self.provider_list:
			self.provider.append_history(i['NAME'])
			
			
		
		
		
		farea_right = Frame(f)
		farea_right.pack(fill='both',expand=1,pady=6)
		
		self.areaframe =LabelFrame(farea_right,label=unicode('管辖区域=>'))
		#self.areaframe.pack(side='left',fill='x',padx=4,pady=5)
		f = Frame(self.areaframe.frame)
		f.pack(fill='both',expand=1,pady=4,padx=4)
		self.sel_areas=myCheckList(f)
		self.sel_areas.pack(side='left',fill='x')
		
		
		
		self.rightsframe = LabelFrame(farea_right,label=unicode('操作权限=>'))
		self.rightsframe.pack(side='left',fill='y',padx=4,pady=5)
		f = Frame(self.rightsframe.frame)
		f.pack(fill='both',expand=1,pady=4,padx=4)		
		self.sel_rights = myCheckList(f)
		self.sel_rights.pack(side='left',fill='y',expand=1)
		
		#加载区域和权限列表
		sql = "select * from area"
		self.area_list = session.getdata(sql)
		textstyle =DisplayStyle('imagetext',  refwindow=self.sel_areas,font=('宋体',10))
		for i in self.area_list:
			
			self.sel_areas.add(str(i['ID']),i['NAME'].strip())		
			self.sel_areas.setstatus(str(i['ID']),'off')
			pass
		
		#		
		sql = "select * from rights"
		self.rights_list = session.getdata(sql)
		
		for i in self.rights_list:			
			self.sel_rights.add(str(i['ID']),i['NAME'].strip())
			self.sel_rights.setstatus(str(i['ID']),'off')
			pass
			

	def onseltype(self,val):
		if self.user_type.cget('value')==unicode('厂商管理员'):
			self.areaframe.forget()
			self.provider.pack(side='left')
		else:
			self.areaframe.pack(side='left')
			self.provider.forget()
		
	
	##################################################################					
	def onsave(self):
		'''  用户信息存储 '''
		if self.login_name.getvalue().strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('请输入登录用户名'))		
			return 
		if self.psw.getvalue().strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('请输入登录密码 '))		
			return 				
		if self.user_type.cget('value').strip()=='':
			tkMessageBox.showwarning(unicode('警告!'),unicode('请选择用户类别!'))		
			return 
		if self.user_type.cget('value').strip()==unicode('厂商管理员'):
			if self.provider.cget('value').strip()=='':
				tkMessageBox.showwarning(unicode('警告!'),unicode('请选择设备厂商'))		
				return 
		##########################################3
		login_name = self.login_name.getvalue().strip()
		psw = self.psw.getvalue().strip()
		real_name = self.real_name.getvalue().strip()
		tel = self.tel.getvalue().strip()
		user_type = self.user_type.cget('value').strip()
		provider = self.provider.cget('value').strip()
		
		#取用户管辖厂商
		if user_type==unicode('区域管理员'):
			provider =0
		else:
			for p in self.provider_list:
				if provider == p['NAME'].strip():
					provider = int(p['ID'])
		
		
		found = 0
		found_user =None
		for i in self.userlist	:
			if i['LOGIN_NAME']==login_name:
				found = i['ID']
				found_user = i
				break
			
		# get user's rights and areas
		
		rights = self.sel_rights.getselection()
		areas = self.sel_areas.getselection()
		if provider:	#if provider manager ,no areas  cannt  prowl
				areas=[]


		#-------------------------------		
		data =[]
		data.append(['login_name',ado.STRING ,login_name])
		data.append(['psw',ado.STRING ,psw])
		data.append(['real_name',ado.STRING ,real_name])
		data.append(['tel',ado.STRING ,tel])
		data.append(['provider',ado.INT ,provider])

		if found :
			#do update
			print 'do update'
					
			#-- delete all area and rights as user,and insert all
			sql ='delete from userarea where user_id=%s'%found_user['ID']
			session.dbcnn.Execute(sql)
			sql ='delete from userrights where user_id=%s'%found_user['ID']
			session.dbcnn.Execute(sql)
				
			for i in rights:
				sql = 'insert into userrights (user_id,rights_id) values(%s,%s)'%(found_user['ID'],i)
				#print sql
				session.dbcnn.Execute(sql)
				
			for i in areas:
				sql = 'insert into userarea (user_id,area_id) values(%s,%s)'%(found_user['ID'],i)
				#print sql
				session.dbcnn.Execute(sql)
										
			sql = "update userinfo set login_name=?,psw=?,real_name=?,tel=?,provider=? where id = %s"%found
			sql = sql.upper()
			
			try:

				session.dbcnn.Execute(sql,data)				
				self.shl.hlist.tk.call(self.shl.hlist,'entryconfigure',found_user['ID'],'-text',real_name)
				tkMessageBox.showwarning(unicode(''),unicode('修改用户信息成功!'))		
			except:
				tkMessageBox.showwarning(unicode('警告!'),unicode('修改用户信息失败!'))		
				return
			
			#print sql
		
		else:
			# do insert
			print 'do insert'
			try:
				sql = 'insert into userinfo (id,login_name,psw,real_name,tel,provider) values(?,?,?,?,?,?)'
				id = session.getsequence()			
				data.insert(0,['id',ado.INT,int(id)])
				session.dbcnn.Execute(sql,data)
				
				for i in rights:
					if i.strip()=='':
						continue
					sql = 'insert into userrights (user_id,rights_id) values(%s,%s)'%(id,i)
					#print sql
					session.dbcnn.Execute(sql)
				print "areas:"
				print areas
				for i in areas:
					if i.strip()=='':
						continue
					sql = 'insert into userarea (user_id,area_id) values(%s,%s)'%(id,i)
					print sql
					#print sql
					session.dbcnn.Execute(sql)

				print "begin to update hlist"
				self.shl.hlist.add(str(id),itemtype='imagetext',image=self.pi,text=real_name)				
				tkMessageBox.showwarning(unicode(''),unicode('添加用户成功!'))		
			except:
				tkMessageBox.showwarning(unicode('警告!'),unicode('添加用户失败!'))		
				return 
				pass
				
		#更新当前用户列表
		sql = "select * from userinfo where login_name<>'admin' and login_name<>'super' order by real_name"
		sql = sql.upper()
		self.userlist = session.getdata(sql)
							
		
	def ondel(self):
		''' 删除用户账号 '''
		if len(self.shl.hlist.info_selection())==0:
			tkMessageBox.showwarning(unicode('警告!'),unicode('请选择用户！'))			
			return
		cur_sel = self.shl.hlist.info_selection()[0]
			
		if tkMessageBox.askyesno(unicode('提示!'),unicode('是否真的要删除选择用户?'))==0:
			return 
		
		try:
			sql = 'delete from userinfo where id=%s '%cur_sel
			session.dbcnn.Execute(sql)
			sql = 'delete from userarea where user_id=%s '%cur_sel
			session.dbcnn.Execute(sql)
			sql = 'delete from userrights where user_id=%s '%cur_sel
			session.dbcnn.Execute(sql)
			
			self.shl.hlist.delete_entry(cur_sel)
			self.reset()	#清除现有的界面用户信息
		except:
			tkMessageBox.showwarning(unicode('警告!'),unicode('删除用户失败！'))			
		
			
		
	def reset(self):
		self.login_name.setentry("")
		self.psw.setentry('')		
		self.real_name.setentry('')		 	
		self.tel.setentry('')		 	
		#清除对象状态
		for item in self.sel_rights.hlist.info_children():
			self.sel_rights.setstatus(item,'off')
		for item in self.sel_areas.hlist.info_children():
			self.sel_areas.setstatus(item,'off')

		

	#选择当前用户 
	def onseluser(self,path):
		'''当前选择的用户 '''
		for i in self.userlist	:
			if i['ID']==int(path):
				self.show_single(i)
				
					
	def show_single(self,user):
		'''显示用户信息'''
		self.login_name.setentry(user['LOGIN_NAME'].strip())
		self.psw.setentry(user['PSW'].strip())		
		self.real_name.setentry(user['REAL_NAME'].strip())		 	
		self.tel.setentry(user['TEL'].strip())		 	
		#清除对象状态
		for item in self.sel_rights.hlist.info_children():
			self.sel_rights.setstatus(item,'off')
		for item in self.sel_areas.hlist.info_children():
			self.sel_areas.setstatus(item,'off')
		u = User(user['ID'])		
		#设置状态	
		
		for r in u.rights:
			self.sel_rights.setstatus(str(r['ID']),'on')
		for a in u.areas:
			self.sel_areas.setstatus(str(a['ID']),'on')

		if user['PROVIDER']!=0:#is provider
			self.user_type.pick(1)
			self.provider.pack(side='left')			
			for i in  self.provider_list:
				if user['PROVIDER']==i['ID']:
					self.provider.configure(value=i['NAME'])
		else:
			self.user_type.pick(0)
			self.provider.forget()
				
			
				
	