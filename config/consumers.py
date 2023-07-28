import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        from common.chat.models import Room
        from api.chat.message.serializers import MessageCreateSerializer
        validate_data = self.make_serializer_data(data)

        serializer = MessageCreateSerializer(data=validate_data)
        is_valid = serializer.is_valid()

        if is_valid:
            message = serializer.save()
            content = {
                'command': 'new_message',
                'message': self.message_to_json(message)
            }
            room = Room.objects.get(guid=self.room_guid)
            room.messages.add(message)
            room.save()
            return self.send_chat_message(content)
        else:
            return self.send_chat_message({"error": "Failed to send message"})

    def load_messages(self, data):
        from common.chat.models import Message
        from api.chat.message.serializers import MessageListSerializer
        from django.core.paginator import Paginator

        page = data.get('page', 1)
        per_page = data.get('per_page', 50)
        queryset = Message.objects.filter(roomMessages__guid=self.room_guid)

        paginator = Paginator(queryset, per_page)
        paginated_queryset = paginator.get_page(page)
        serializer = MessageListSerializer(paginated_queryset, many=True)
        content = {
            'command': 'load_messages',
            "currentPage": page,
            'hasPrevious': paginated_queryset.has_previous(),
            'hasNext': paginated_queryset.has_next(),
            'messages': serializer.data
        }
        self.send_message(content)

    commands = {
        'new_message': new_message,
        'load_messages': load_messages
    }

    def connect(self):
        # self.user = self.scope["user"]

        self.room_guid = self.scope["url_route"]["kwargs"]["room_guid"]
        self.room_group_name = "chat_%s" % self.room_guid

        # if not self.user.is_authenticated:
        #     self.disconnect(403)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        # messages = Message.objects.filter(roomMessages__guid=self.room_guid)
        # content = {
        # 'command': 'messages',
        # 'messages': self.messages_to_json(messages)
        # }
        # self.send_message(content)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.close()

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def make_serializer_data(self, data):
        context = {
            'sender': data.get('from'),
            'content': data.get('message'),
        }
        return context

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        from api.chat.message.serializers import MessageListSerializer
        return MessageListSerializer(message).data

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message})

    def send_message(self, message):
        self.send(text_data=json.dumps({"message": message}))

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
