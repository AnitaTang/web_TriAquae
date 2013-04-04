from django.shortcuts import render_to_response
from django.http import HttpResponse 
from django.template import RequestContext
#from django.views.generic.simple import direct_to_template
import os


WorkDir = '/usr/local/triAquae2.1.0/conf/server_list'

def dashboard(request):
	
	return render_to_response('iframe.html')
def getCMD(request):
	GroupList = os.listdir(WorkDir)
	ValidList = True 
	if not GroupList:
		ValidList = False
	return render_to_response('runCommand.html',{'ValidList':ValidList,'Groups':GroupList},context_instance=RequestContext(request))
def ShowServerList(request):
	GroupList = os.listdir(WorkDir)
        ValidList = True
        if not GroupList:
                ValidList = False
	

	G_name = request.GET['check']
	GroupFile = '%s/%s' %(WorkDir,G_name)
	server_list = []
	server_list.append('-------------server list of %s ---------------' % G_name)
	f = file(GroupFile)
	while True:
		line = f.readline()
		if len(line) == 0:break
		newLine = line.split()[0:2]
		server_list.append(newLine)
	server_list.insert(1,'Total %s servers'	 % (len(server_list) -1))
	#return render_to_response('server_list.html',{'groupname':GroupFile},context_instance=RequestContext(request)) 
	return render_to_response('runCommand.html',{'ValidList':ValidList,'Groups':GroupList,'groupname':server_list},context_instance=RequestContext(request))


def runCMD(request):
	errors = []
	Groups = os.listdir(WorkDir)
	ChoseGroupList = []
        #Show group list
        GroupList = os.listdir(WorkDir)
        ValidList = True
        if not GroupList:
                ValidList = False


	def ChoseGroups():
		for G_name in Groups:
			if request.POST.get(G_name):
				ChoseGroupList.append(G_name)
		return ChoseGroupList			
	
	if not request.POST.get('command'):
		errors.append('Please input a command!')
		return render_to_response('runCommand.html',{'error':errors,'ValidList':ValidList,'Groups':GroupList},context_instance=RequestContext(request))	
	ChoseGroups()
	#return render_to_response('runCommand.html',{'TEST':ChoseGroups()},context_instance=RequestContext(request))
	
	if not ChoseGroupList:
		errors.append('Please choose a group to proceed!')
                return render_to_response('runCommand.html',{'error':errors,'ValidList':ValidList,'Groups':GroupList},context_instance=RequestContext(request))
	
	ChoseGroupList = [] #Clear the choose group list
        def excute():

		#excute user inputed command
		UserInput = request.POST['command']
		GroupList = ChoseGroups()
		for GroupName in GroupList:
                	Engine = '/usr/local/triAquae2.1.0/bin/JobRunner -r %s "%s" >>/tmp/result.txt' %  (GroupName,UserInput)
			#Engine ='echo %s >> /tmp/result.txt' %GroupName
                	os.system(Engine)
			EndMark = 'echo "-->Excution of %s is done" >>/tmp/result.txt'  % GroupName
			os.system(EndMark)
                os.system('sed -r "s/\x1B\[([0-9]{1,3}((;[0-9]{1,3})*)?)?[m|K]//g" /tmp/result.txt >/tmp/ex-result.txt')
		os.system('echo >/tmp/result.txt')
                f= file('/tmp/ex-result.txt')
                result = []
                while True:
                        line = f.readline()
                        if len(line) ==0:break
                        result.append(line)
                return result
		os.system('echo > /tmp/ex-result.txt')

	#if request.GET['check']:
	#	ShowServerList2()
	return render_to_response('runCommand.html',{'input':excute(),'ValidList':ValidList,'Groups':GroupList},context_instance=RequestContext(request))

	
