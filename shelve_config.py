

# 察看修改配置文件信息
# 配置文件都是hash结构存储，必须用shelve进行操作
#

from Tix import *
import tkFileDialog
import shelve
import re
import tkMessageBox



inifile =''
def onselfile():
	global file
	f = tkFileDialog.askopenfilename()
	
	file.set(f)
	
	if file=='' :
		return
	db = shelve.open(f)
	items.listbox.delete(0,'end')
	for i in db.keys():
		items.listbox.insert('end',unicode(i)+'-->'+unicode(db[i]))
	db.close()
	
	
def onselitem():
	print items.listbox.get(items.listbox.curselection())
	item =  re.split('-->',items.listbox.get(items.listbox.curselection()))
	key.set(item[0])
	val.set(item[1])
	
	pass

def onsave():
	global file,enval,enkey
	
	if enfile.get()=='' or key.get()=='':
		return
	
	 
	
	db = shelve.open(enfile.get())
	db[enkey.get()] = enval.get()
	
	print db[enkey.get()]
	#tkMessageBox.showinfo(unicode(db[key.get()]))
	items.listbox.delete(0,'end')
	for i in db.keys():
		items.listbox.insert('end',i+'-->'+db[i])
		print i,db[i]
	db.close()

def ondel():
	if len(items.listbox.curselection())==0:
		return
	item =  re.split('-->',items.listbox.get(items.listbox.curselection()))
	db = shelve.open(enfile.get())
	del db[enkey.get()]	
	#tkMessageBox.showinfo(unicode(db[key.get()]))
	items.listbox.delete(0,'end')
	for i in db.keys():
		items.listbox.insert('end',i+'-->'+db[i])
		print i,db[i]
	db.close()
	
	
if __name__=='__main__':
	rt = Tk()
	rt.option_add('*Font',('宋体',14))
	f = Frame(rt)
	f.pack(fill='x')
	file = StringVar()
	enfile = Entry(f,textvariable = file)
	enfile.pack(side = 'left')
	btnselfile = Button(f,text =unicode('选择配置文件..'),command = onselfile)
	btnselfile.pack()
	
	f = Frame(rt)
	f.pack(fill='both',expand=1)
	
	items = ScrolledListBox(f,scrollbar='auto',browsecmd =onselitem)
	items.pack(fill='both',expand=1)
	
	key = StringVar()
	enkey = Entry(f,textvariable=key,width=20)
	enkey.pack(side='left',fill='x')
	val = StringVar()
	enval = Entry(f,textvariable=val,width=30)
	enval.pack(side='left',fill='x',expand=1)
	
	btnsave = Button(rt,text=unicode('保存'),command=onsave)
	btnsave.pack(side='left')
	
	btndel = Button(rt,text=unicode('删除'),command = ondel)
	btndel.pack()
	rt.mainloop()