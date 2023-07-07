from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync
from .models import Group
from signin.models import User
from channels.db import database_sync_to_async
from django.db.models import Q
from .models import Group,Collabnote

class MySyncConsumer(SyncConsumer):
    # inherit sync conusmer
    def websocket_connect(self,event):
        print('websocket connect',event)
        
        print('channels layer is.......',self.channel_layer)
        print('channel name is..........',self.channel_name)

        print(self.scope['url_route']['kwargs']['grpname'])
        self.grpname=self.scope['url_route']['kwargs']['grpname']
        self.email=self.scope['url_route']['kwargs']['email']
        # event
        group=Group.getgrpobj(self.email,self.grpname)
        participants=group.participants
        participants_list=participants.split()

        if self.email in participants_list:
            async_to_sync(self.channel_layer.group_add)(
                # 'programer',
                self.grpname,
                self.channel_name
            )
            # add channel to grp
            self.send({
                'type':'websocket.accept'
            })
        else:
            pass



    def websocket_receive(self,event):
        print('msg received',event)
        print('message from client=',event['text']) #string type
        data=json.loads(event['text'])
        
        print('.................................',data,data['msg'])


        group=Group.getgrpobj(self.email,self.grpname)
        note=Collabnote.objects.filter(Q(name=self.grpname) & Q(user__email=self.email)).first()
        if note:
            note.content=data['msg']
            note.save()
        else:
            user=User.user_object(self.email)
            chat=Collabnote(name=self.grpname,content=data['msg'],group=group,user=user)
            chat.save()
        
        async_to_sync(self.channel_layer.group_send)(
            self.grpname,{
            'type':'chat.message',
            'message':event['text']
        })
    
    
    def chat_message(self,event):
        print('event.........',event)   #prints type and message 
        print('actual messagae',event['message'])
        #send msg to client
        self.send({
            'type':'websocket.send',
            'text':event['message']
            #message is already in string
        })
    
    
    
    def websocket_disconnect(self,event):
        print('websocket disconnect',event)
        raise StopConsumer()
    
    