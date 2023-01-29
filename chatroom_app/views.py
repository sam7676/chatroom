from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
import datetime
import json

from chatroom_app.models import *

def index(request):
    return render(request,'mainpage.html')

def chat(request):
    removeOldChats()
    removeOldUsers()
    removeUnusedServers()

    #getting data from page
    try:
        name = request.POST["name"]
        room = request.POST["room"]
        pw = request.POST["password"]
    except:
        return HttpResponseRedirect(reverse('index'))
    #Pre-fetch validation
    if name=='' or room=='':
        messages.success(request,"Error: Empty string")
        return HttpResponseRedirect(reverse('index'))
    elif name.lower().strip()=='admin':
        messages.success(request,"Error: Invalid name")
        return HttpResponseRedirect(reverse('index'))
    elif len(name) > 16:
        messages.success(request,"Error: Name too long")
        return HttpResponseRedirect(reverse('index'))
    elif len(room) > 16:
        messages.success(request,"Error: Room name too long")
        return HttpResponseRedirect(reverse('index'))

    else:
        #Get server
        try:
            serv = ServerList.objects.get(server=room)
        except:
            serv = None
        #If server doesn't exist, create it
        if serv==None:
            s = ServerList(server=room,lockStatus=False,lastUpdate=datetime.datetime.now().astimezone(),password='none')
            s.save()
            #Add user to server
            u = UserList(username=name,server=s,time=datetime.datetime.now().astimezone())
            u.save()
            #Show that user joined
            c = Chats(server=s,username='admin',message=f"{name} joined the chat.",time=datetime.datetime.now().astimezone())
            c.save()
        else:
            #if server is locked, deny
            if serv.lockStatus==True:
                
                #if password needed
                if serv.password!='none':
                    if serv.password!=pw:
                        messages.success(request,"Error: Password needed")
                        return HttpResponseRedirect(reverse('index'))
                else:
                    messages.success(request,"Error: Room is locked")
                    return HttpResponseRedirect(reverse('index'))

            #if user in server, deny
            try:
                u = UserList.objects.get(server=serv,username=name)
            except:
                u = None
            if u!=None:
                messages.success(request,"Error: Name in use for server")
                return HttpResponseRedirect(reverse('index'))
            #Add user to server
            u = UserList(username=name,server=serv,time=datetime.datetime.now().astimezone())
            u.save()
            #Show that user joined
            c = Chats(server=serv,username='admin',message=f"{name} joined the chat.",time=datetime.datetime.now().astimezone())
            c.save()
            
            #Validation done, ready to connect
        c = {
            "room":room,
            "name":name,
        }
        return render(request,'chatpage.html',context=c)   

def sendmsg(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request) #Get data from POST request
        msg = data_from_post.get("message")
        room = data_from_post.get("room")
        name = data_from_post.get("name")
        last = data_from_post.get("last")
        if len(msg) > 0 and len(msg) < 100000:
            time = datetime.datetime.now().astimezone()
            serv = ServerList.objects.filter(server=room)[0]
            c = Chats(server=serv,username=name,message=msg,time=time)
            c.save()
            UserList.objects.filter(server=room,username=name).update(time=time)
            ServerList.objects.filter(server=room).update(lastUpdate=time)

            removeOldChats()
            removeOldUsers()
            removeUnusedServers()

            
            data = {}
            for i in Chats.objects.filter(server=room).order_by('time').values():
                if i["chatID"] > int(last):
                    time = str(i["time"]).split(" ")[1].split(".")[0]
                    data[i["chatID"]] = [i["username"],i["message"],time]

            return JsonResponse(data)
        return JsonResponse({})  

def sendcmd(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        js = json.load(request)
        
        command = js.get("command").lower()
        serv = js.get("room")
        
        if command=="leave":
            return JsonResponse({'response':'home'})

        elif command=="unlock":
            s = ServerList.objects.get(server=serv)
            if s.lockStatus==True:
                ServerList.objects.filter(server=serv).update(lockStatus=False)
                c = Chats(server=ServerList.objects.get(server=serv),username='admin',message="Server unlocked.",time=datetime.datetime.now().astimezone())
                c.save()
            return JsonResponse({})
        
        elif command=="close":
            removeOldUsers()
            #if users = 1
            u = UserList.objects.filter(server=serv).values()
            if len(u)==1:
                s = ServerList.objects.get(server=serv)
                for i in Chats.objects.filter(server=s).values():
                    chatID = i.get("chatID")
                    c = Chats.objects.get(chatID=chatID)
                    c.delete()
                s.delete()
                return JsonResponse({'response':'home'})
            else:
                c = Chats(server=ServerList.objects.get(server=serv),username='admin',message="Chatroom could not be closed.",time=datetime.datetime.now().astimezone())
                c.save()
            return JsonResponse({})

        command=command.split(" ")

        if command[0]=='lock':

            if len(command)==1:
                s = ServerList.objects.get(server=serv)
                if s.lockStatus==False:
                    ServerList.objects.filter(server=serv).update(lockStatus=True,password="none")
                    c = Chats(server=ServerList.objects.get(server=serv),username='admin',message="Server locked.",time=datetime.datetime.now().astimezone())
                    c.save()
                
            else:
                pw = command[1]
                if len(pw)>16:
                    c = Chats(server=ServerList.objects.get(server=serv),username='admin',message=f"Server password too long.",time=datetime.datetime.now().astimezone())
                    c.save()
                
                elif pw!=ServerList.objects.get(server=serv).password:
                    ServerList.objects.filter(server=serv).update(lockStatus=True,password=pw)
                    c = Chats(server=ServerList.objects.get(server=serv),username='admin',message=f"Server password set: {pw}",time=datetime.datetime.now().astimezone())
                    c.save()
            
            return JsonResponse({})
            
        return JsonResponse({})

def getchats(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request) #Get data from POST request
        room = data_from_post["room"]
        name = data_from_post["name"]
        last = data_from_post["last"]

        #update user
        UserList.objects.filter(server=room,username=name).update(time=datetime.datetime.now().astimezone())

        data = {}
        for i in Chats.objects.filter(server=room).order_by('time').values():
            if i["chatID"] > int(last):
                time = str(i["time"]).split(" ")[1].split(".")[0]
                data[i["chatID"]] = [i["username"],i["message"],time]
        return JsonResponse(data)  

def removeOldUsers():
    #Updating users from server
    for i in UserList.objects.all().order_by('time').values():
        id = i.get('userID')
        name = i.get('username')
        time = i.get('time')
        serv = ServerList.objects.get(server=i.get('server_id'))
        timeout = datetime.datetime.now().astimezone() - datetime.timedelta(seconds=30)
        if time <= timeout:
            UserList.objects.filter(userID=id).delete()
            #Show that user left
            c = Chats(server=serv,username='admin',message=f"{name} left the chat.",time=datetime.datetime.now().astimezone())
            c.save()
        else:
            break

def removeOldChats():
    #removing items over 1d old
    for i in Chats.objects.all().order_by('time').values():
        id = i.get("chatID")
        time = i.get("time")
        yesterday = datetime.datetime.now().astimezone() - datetime.timedelta(days=1)
        if time <= yesterday:
            Chats.objects.filter(chatID=id).delete()
        else:
            break

def removeUnusedServers():
    for i in ServerList.objects.all().order_by('lastUpdate').values():
        id = i.get("server")
        time = i.get("lastUpdate")
        lock = i.get("lockStatus")
        server = ServerList.objects.get(server=id)
        sixH = datetime.datetime.now().astimezone() - datetime.timedelta(hours=1)
        chats = Chats.objects.filter(server=server).values()
        users = UserList.objects.filter(server=server).values()
        if time <= sixH and len(chats)==0 and len(users)==0:
            server.delete()
        elif len(users)==0 and lock==True:
            #delete all msgs
            for j in Chats.objects.filter(server=server).values():
                chatID = j.get("chatID")
                c = Chats.objects.get(chatID=chatID)
                c.delete()
            server.delete()
            
def getusers(request):
    removeOldUsers()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request) #Get data from POST request
        room = data_from_post["room"]
        data = {'user_num':len(UserList.objects.filter(server=ServerList.objects.get(server=room)).values())}
        return JsonResponse(data)

