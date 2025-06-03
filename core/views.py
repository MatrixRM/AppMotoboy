import openai
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from twilio.rest import Client
from .models import Motoboy, Escala
import os
from dotenv import load_dotenv



load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")


def gerar_resposta_chatgpt(mensagem):
    prompt = f"""
    Você é um assistente que ajuda a montar escalas de motoboys.
    Com base na seguinte mensagem: '{mensagem}', gere uma escala estruturada com nome, data e turno.
    """
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return resposta.choices[0].message['content']

def enviar_resposta_twilio(mensagem, numero_destino):
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
    client.messages.create(
        body=mensagem,
        from_='whatsapp:+14155238886',  # número oficial da Twilio
        to=numero_destino
    )

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        msg = request.POST.get('Body')
        sender = request.POST.get('From')
        resposta = gerar_resposta_chatgpt(msg)
        enviar_resposta_twilio(resposta, sender)
        return JsonResponse({"status": "Mensagem processada com sucesso"})
    return JsonResponse({"error": "Método não permitido"}, status=405)
