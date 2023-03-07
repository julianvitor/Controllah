# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import requests
from cryptography.fernet import Fernet
from mfrc522 import SimpleMFRC522
import datetime
import time
import Adafruit_CharLCD as LCD
import pygame

# Define os pinos do display LCD
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 4

# Define as dimensões do display LCD
lcd_columns = 16
lcd_rows = 2

# Inicializa o display LCD
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

# Define a chave de criptografia
key = Fernet.generate_key()
fernet = Fernet(key)

# Lê o nome da tag RFID
reader = SimpleMFRC522()
nome = reader.read()

# Define a hora atual do sistema
hora_atual = datetime.datetime.now().strftime('%H:%M')

# Cria a mensagem a ser enviada, incluindo a chave criptografada e a hora atual
mensagem = f'nome={nome}&hora={hora_atual}'.encode()
mensagem_criptografada = fernet.encrypt(mensagem)
chave_criptografada = key.decode()

# Define a URL do servidor e envia a requisição POST
url = 'http://localhost:5000/algum_endpoint'
data = {'mensagem': mensagem_criptografada, 'chave': chave_criptografada}
response = requests.post(url, data=data)

# Verifica a resposta do servidor
if response.text == 'autorizado':
    # Aciona a tranca
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)  # Liga o relé
    time.sleep(1)  # Aguarda 1 segundo
    GPIO.output(18, GPIO.LOW)  # Desliga o relé
    GPIO.cleanup()  # Limpa as configurações da GPIO
    lcd.clear()
    lcd.message('Autorizado')
    pygame.mixer.init()
    pygame.mixer.music.load('autorizado.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    print('Fechadura acionada')
else:
    lcd.clear()
    lcd.message('Nao autorizado')
    pygame.mixer.init()
    pygame.mixer.music.load('nao_autorizado.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    print('Acesso negado')
