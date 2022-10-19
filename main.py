import json
import requests
import time as ttttt
import os
import random

master=['1855411421'] ##此处填写主人的ID,是python列表格式,不知道如何填写的话请看: https://www.runoob.com/python3/python3-tutorial.html
token='' ##此处填写机器人的Token,单引号不能删
board='https://raw.githubusercontent.com/wzk0/sendmsg_bot/main/board' ##此处填写/help指令时获取内容的url
ckn_up=30 ##此处填写签到时获得的随机积分的上限
ckn_down=20 ##此处填写下限

def send_msg(user_id,text):
	global token
	url='https://api.telegram.org/bot%s/'%token
	params={'chat_id':user_id,'text':text,'parse_mode':'markdown'}
	r=requests.post(url+'sendMessage',params=params)

def tree(user_id):
	os.system('mkdir .data/%s'%str(user_id))
	os.system('touch .data/%s/point'%str(user_id))
	os.system('touch .data/%s/last_time'%str(user_id))

def wrt(user_id,point,time):
	with open('.data/%s/point'%str(user_id),'w')as f:
		f.write(str(point))
	with open('.data/%s/last_time'%str(user_id),'w')as l:
		l.write(time)

def reg(user_id):
	global ckn_up,ckn_down
	point=random.randint(ckn_down,ckn_up)
	time=str(ttttt.strftime("%Y-%m-%d", ttttt.localtime()))
	if '.data' not in os.listdir('.'):
		os.system('mkdir .data')
		tree(user_id)
		wrt(user_id,point,time)
		return True
	else:
		if user_id in os.listdir('.data'):
			return False
		else:
			tree(user_id)
			wrt(user_id,point,time)
			return True

def ckn(user_id):
	global ckn_up,ckn_down
	point=random.randint(ckn_down,ckn_up)
	time=str(ttttt.strftime("%Y-%m-%d", ttttt.localtime()))
	if '.data' not in os.listdir('.'):
		os.system('mkdir .data')
		tree(user_id)
		wrt(user_id,point,time)
		return True,point
	else:
		if str(user_id) not in os.listdir('.data'):
			tree(user_id)
			wrt(user_id,point,time)
			return False,point
		else:
			with open('.data/%s/last_time'%str(user_id),'r')as f:
				if time==str(f.read()):
					return False,0
				else:
					with open('.data/%s/point'%str(user_id),'r')as f:
						now_point=str(int(f.read())+point)
					wrt(user_id,now_point,time)
					return True,point

def ifo(user_id):
	with open('.data/%s/last_time'%str(user_id),'r')as f:
		time=f.read()
	with open('.data/%s/point'%str(user_id),'r')as l:
		point=l.read()
	return [time,point]

def snd(text,condition):
	ok=[]
	for uid in os.listdir('.data'):
		with open('.data/%s/point'%uid,'r')as f:
			point=int(f.read())
		if point>=condition:
			ok.append(uid)
		else:
			pass
	return ok

def shw():
	dic={}
	for user_id in os.listdir('.data'):
		with open('.data/%s/point'%user_id,'r')as f:
			dic[user_id]=f.read()
	return dic

def is_master(user_id):
	global master
	if len(master)==1:
		if str(user_id)==str(master[0]):
			return True
		else:
			return False
	else:
		if str(user_id) in master:
			return True
		else:
			return False

def command(cmd,user_id):
	if '/register' in cmd:
		if reg(user_id):
			send_msg(user_id,'注册成功🥳🎉!')
		else:
			send_msg(user_id,'已经注册过啦🌈🦄!')
	if '/checkin' in cmd:
		condition,point=ckn(user_id)
		if condition:
			send_msg(user_id,'签到成功🥳🎉!获得%s积分!'%point)
		else:
			if point!=0:
				send_msg(user_id,'不注册就签到是不好的习惯,但还是为你自动注册啦🥳🎉!获得%s积分!'%point)
			else:
				send_msg(user_id,'已经签到过啦,明天再来吧🥳🎉!')
	if '/info' in cmd:
		ls=ifo(user_id)
		send_msg(user_id,'💖我的ID:%s\n🔥最近一次签到日期:%s\n✨我的积分:%s'%(user_id,ls[0],ls[1]))
	if '/admin' in cmd:
		if '/admin'==cmd:
			send_msg(user_id,'❌用法错误!')
		else:
			if is_master(user_id)!=True:
				send_msg(user_id,'❌不是主人!')
			else:
				text=cmd.split(' ')[1]
				condition=int(cmd.split(' ')[-1])
				ls=snd(text,condition)
				if len(ls)==0:
					send_msg(user_id,'❌无法找到符合条件的用户!')
				else:
					send_msg(user_id,'💯符合条件的用户列表如下:\n%s'%'\n'.join(ls))
					for uid in ls:
						send_msg(uid,text)
	if '/chat' in cmd:
		cht(user_id)
	if '/help' in cmd:
		global board
		r=requests.get(board)
		send_msg(user_id,r.text)
	if '/start' in cmd:
		send_msg(user_id,'感谢使用🥳🎉!')
	if '/log' in cmd:
		if is_master(user_id)!=True:
			send_msg(user_id,'❌不是主人!')
		else:
			with open('.log','r')as f:
				send_msg(user_id,f.read())
	if '/give' in cmd:
		if '/give'==cmd:
			send_msg(user_id,'❌用法错误!')
		else:
			if is_master(user_id)!=True:
				send_msg(user_id,'❌不是主人!')
			else:
				getor=cmd.split(' ')[1]
				point=cmd.split(' ')[-1]
				if getor in os.listdir('.data'):
					with open('.data/%s/point'%str(getor),'r')as f:
						old_point=f.read()
						if old_point=='':
							old_point=0
					with open('.data/%s/point'%str(getor),'w')as l:
						l.write(str(int(old_point)+int(point)))
					send_msg(user_id,'给用户%s加分成功🥳🎉!'%getor)
				else:
					send_msg(user_id,'❌用户%s不在已注册用户中!'%getor)
	if '/show' in cmd:
		if is_master(user_id)!=True:
			send_msg(user_id,'❌不是主人!')
		else:
			dic=shw()
			ls=list(dic.keys())
			text=[]
			for d in ls:
				text.append(d+' - '+dic[d])
			send_msg(user_id,'💯用户ID和对应积分的列表如下:\n%s'%'\n'.join(text))
	
	elif cmd not in ['/log','/register','/checkin','/info','/admin','/chat','/help','/show','/start']:
		errorls=['/admin','/give']
		if errorls[0] in cmd.split(' ')[0] or errorls[1] in cmd.split(' ')[0]:
			pass
		else:
			r=requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg='+cmd)
			send_msg(user_id,json.loads(r.text)['content'].replace('{br}','\n'))
		
def roll(condition):
	if not os.path.exists('.temp'):
		with open('.temp','w')as f:
			f.write(str(condition))
		return True
	else:
		with open('.temp','r')as f:
			file=f.read()
		if str(file)==str(condition):
			return False
		else:
			with open('.temp','w')as l:
				l.write(str(condition))
			return True

def get(url,part,params):
	r=requests.get(url+part,params=params)
	return json.loads(r.text)

def begin(token):
	base_url='https://api.telegram.org/bot%s/'%token
	time=str(ttttt.strftime("%Y-%m-%d %H:%M:%S", ttttt.localtime()))
	try:
		if not os.path.exists('.offset'):
			with open('.offset','w')as f:
				param={}
				new=get(base_url,'getUpdates',param)
				f.write(str(new['result'][-1]['update_id']))
				offset=new['result'][-1]['update_id']
		else:
			with open('.offset','r')as f:
				offset=f.read()
			with open('.offset','w')as l:
				l.write(offset)
		params={'offset':offset}
		new=get(base_url,'getUpdates',params)
		msg=new['result'][-1]['message']
		user_id=str(msg['from']['id'])
		user_name=msg['from']['username']
		file_type=list(msg.keys())
		if roll(user_id+str(new['result'][-1]['update_id']))!=True:
			pass
		else:
			if 'text' not in file_type:
				print(time+' - '+user_id+' - @'+user_name+' - '+'这是一个%s消息!'%file_type[-1])
				with open('.log','a')as f:
					f.write(time+' - '+user_id+' - @'+user_name+' - '+'这是一个%s消息!'%file_type[-1]+'\n')
				send_msg(user_id,'怎么了,给我发这个%s,想和我聊天嘛?'%file_type[-1])
			else:
				command(msg['text'],user_id)
				with open('.log','a')as f:
					f.write(time+' - '+user_id+' - @'+user_name+' - '+msg['text']+'\n')
				print(time+' - '+user_id+' - @'+user_name+' - '+msg['text'])
	except:
		ttttt.sleep(3)

while True:
	begin(token)
