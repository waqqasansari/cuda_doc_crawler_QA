from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatInputSerializer, ChatOutputSerializer
from .chatbot_logic import ChatbotLogic
import uuid

# class ChatbotView(APIView):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.chatbot_logic = ChatbotLogic()

#     def post(self, request):
#         serializer = ChatInputSerializer(data=request.data)
#         if serializer.is_valid():
#             user_input = serializer.validated_data['user_input']
            
#             # Get or create a session ID
#             session_id = request.session.get('chatbot_session_id')
#             if not session_id:
#                 session_id = str(uuid.uuid4())
#                 request.session['chatbot_session_id'] = session_id

#             # Process the message
#             response = self.chatbot_logic.process_message(session_id, user_input)

#             output_serializer = ChatOutputSerializer({'ai_response': response['answer']})
#             return Response(output_serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatbotView(APIView):
    chatbot_logic = None

    @classmethod
    def get_chatbot_logic(cls):
        if cls.chatbot_logic is None:
            print("Initializing ChatbotLogic...")
            cls.chatbot_logic = ChatbotLogic()
        return cls.chatbot_logic

    def post(self, request):
        serializer = ChatInputSerializer(data=request.data)
        if serializer.is_valid():
            user_input = serializer.validated_data['user_input']
            
            # Get or create a session ID
            session_id = request.session.get('chatbot_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['chatbot_session_id'] = session_id

            # Use the shared ChatbotLogic instance
            chatbot = self.get_chatbot_logic()
            
            # Process the message
            response = chatbot.process_message(session_id, user_input)

            output_serializer = ChatOutputSerializer({'ai_response': response['answer']})
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)