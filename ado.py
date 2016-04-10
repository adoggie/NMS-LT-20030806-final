

############################################
# 功能: ado数据访问包装
# 日期：2003-01-10
# 创建：runonce
# 历史:	
#	2003-01-10  创建
#	20030419  增加Execute2方法,Execute2支持bcb数据访问模式(name=:name),支持sql数据集返回
##############################################

from win32com.client import *
import pythoncom 
import string
import tkMessageBox
import re
from adoconst import *
from Tix import *

#定义参数类型
STRING = adVarChar
INT = adInteger
DOUBLE = adDouble


	
class PAdo:
	""" Ado数据访问包装类
	"""
	def __init__(self,cnnstr='',bOpen=1):
		"cnnstr--ado 数据连接字符串,bopen--是否自动打开"
		self.cnnstr =cnnstr
		self.adoConn=None
		self.rs=None
		self.adoConn = Dispatch('ADODB.Connection')
		self.rs=Dispatch('ADODB.Recordset')
		if bOpen==1 :
			self.adoConn.Open(cnnstr)
			
	def Close(self):
		self.adoConn=None
		self.rs=None
		
	def	getTables(self):
		" 获取数据库所有表名称"
		
		adoRs = self.adoConn.OpenSchema(20)  #取数据库所有表
		adoRs.MoveFirst()
		ar=[]
		while not adoRs.EOF:
		    ar.append(str(adoRs.Fields.Item('TABLE_NAME')))
		    adoRs.MoveNext()
		return ar
		
	def getFields(self,rs): #recordset
		"取记录集字段信息"
		fds=[]
		for i in range(0,rs.Fields.Count):
			fds.append(rs.Fields.Item(i).Name)
		return fds
	
	def Select(self,sql):
		"""执行查询操作，多参引入
			不采用参数占位符方式，传入的sql直接执行	
		03.0109 
		"""
		sql = sql.upper()
		#print sql
		self.rs=Dispatch('ADODB.Recordset')
		self.rs.Open(sql,self.adoConn,-1,-1,-1)
		#
		#ar=[]
		#while not self.rs.EOF:
		#	print self.rs.Fields.Item('NAME').Value
		#	ar.append(self.rs.Fields.Item('NAME').Value)
		#	self.rs.MoveNext()
		
		return self.rs
		
		
	def Execute(self,sql,params=None):
		"""
			sql-- sql执行语句，如果是带参数则形式为 insert into tablename (name) values(:name),同bcb
			params --params是列表类型,包含数据的参数，每个参数是一个3元组，代表参数的具体信息 ，(name,type,value) ,撤销size,成为3元组合
					
			params=None,指定sql为正常sql(不带参数占位符号)
		使用方法:
			ado.Execute('insert into basicinfo (name,type,dt,v2) values(?,?,?,?)',['name',STRING,'11'],
			['type',STRING,'类型'],['dt',STRING,'2002-01-12 12:12:01'],['v2',DOUBLE,111111111.231])


		--未进行错误保护
		
		"""
		
		sql = string.upper(sql)
		#print sql
		
		param = Dispatch('ADODB.Parameter')
		cmd = Dispatch('ADODB.Command')
		cmd.ActiveConnection = self.adoConn
		cmd.CommandText= sql
		
		if(params !=None):
			for ele in params:  #len(params) 个参数字段带入
				#print ele
				#print ele[0],ele[1],ele[2]
				if ele[1]==STRING:
					size = len(str(ele[2]))
					print size
				if ele[1]==INT:
					size = 4
				if ele[1]==DOUBLE:
					size =8
				cmd.Parameters.Append(cmd.CreateParameter(ele[0],ele[1],1,size,ele[2]))
		cmd.Execute()
		
	
	def Execute2(self,sql,params=None):
		""" 
			sql-- sql执行语句，如果是带参数则形式为 insert into tablename (name) values(:name),同bcb
			params --params是列表类型,包含数据的参数，每个参数是一个3元组[参数名,值,类型]					
			params=None,指定sql为正常sql(不带参数占位符号)
		<<使用方法:>>			
			sql = 'insert userinfo (id,login_name) values(:id,:login_name)'
			data=[]
			data.append([' loGin_name ','test1'])
			data.append(['ID',101])
			rs = ado.Execute2(sql,data)

		--未进行错误保护		
		"""
		
		_sql = string.upper(sql)
		#print _sql
		#step1: 查找参数
		ps = re.findall(':(\w+)',_sql)
		#step1: 生成ado sql 语句  ,例如: insert into a (a1,a2) values(?,?)
		_sql = re.sub(':(\w+)','?',_sql)
		#step3: 校对带入参数是否与sql中的参数匹配
		if params:
			for i in params:
				p = i[0].upper().strip()
				try:					
					ps.index(p)
				except:
					tkMessageBox.showinfo('warning!',unicode('parameter error:')+p)
					return 						
		
		
		param = Dispatch('ADODB.Parameter')
		cmd = Dispatch('ADODB.Command')
		cmd.ActiveConnection = self.adoConn
		cmd.CommandText= _sql
		#print _sql
		
		if(params !=None):
			for p in ps:				
				for ele in params:  #len(params) 个参数字段带入
								
					if ele[0].upper().strip() == p:
						_type=0
						size =0
						#print type(ele[1]),type('string')
						if type(ele[1])==type(1): #integer
							size = 4
							_type = INT
							#print 'int '
						if type(ele[1])==type(1.1): #double
							size = 8
							_type = DOUBLE
							#print 'double'
						if type(ele[1])==type(unicode('string')) or type(ele[1])==type('string'): #string
							size = len(str(ele[1]))
							if size==0:
								size=1
								ele[1]=" "
							_type = STRING
							print 'string '
						#print p,_type,size,ele[1]
						cmd.Parameters.Append(cmd.CreateParameter(p,_type,1,size,ele[1]))
		(rs,ret) = cmd.Execute()
		#print "execute return value==>",ret
		return rs
		
	def GetRecordCount(self,adors):
		"取记录集记录总数"
		adors.MoveFirst()
		cnt=0
		while not adors.EOF:
			cnt+=1
			adors.MoveNext()
		adors.MoveFirst()
		return cnt
		
#################################################################################################################

#if __name__=="__main__":
	
#	ado = PAdo('Provider=SQLOLEDB.1;Persist Security Info=False;User ID=sa;Initial Catalog=NMSDB_CM;Data Source=localhost')    
#	#ado =PAdo('''Provider=Microsoft.Jet.OLEDB.4.0;User ID=Admin;Data Source=E:\DevDoc\Database\人口统计.mdb;
#		Mode=Share Deny None;Extended Properties="";Jet OLEDB:System database="";Jet OLEDB:Registry Path=;
#		Jet OLEDB:Database Password=;Jet OLEDB:Engine Type=4;Jet OLEDB:Database Locking Mode=0;Jet OLEDB:Global Partial Bulk Ops=2;Jet OLEDB:Global Bulk Transactions=1;Jet OLEDB:New Database Password="";Jet OLEDB:Create System Database=False;Jet OLEDB:Encrypt Database=False;Jet OLEDB:Don't Copy Locale on Compact=False;Jet OLEDB:Compact Without Replica Repair=False;Jet OLEDB:SFP=False''')
#	
#	rs = ado.Select('select * from area')
#	
#	print ado.getFields(rs)	
#	print rs.Fields.Count
##	sql = 'insert userinfo (id,login_name) values(:id,:login_name)'
#	data=[]
#	data.append([' loGin_name ','test1'])
#	data.append(['ID',101])
#	
#	
#	rs = ado.Execute2(sql,data)
		
	
	
	
	
