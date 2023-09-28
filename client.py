import websockets
import asyncio
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

async def message():
    async  with websockets.connect("ws://192.168.0.152:8765") as socket:
        msn = input("Digite uma mensagem: ")
        hash_object = hashlib.sha256()
        hash_object.update(msn.encode('utf-8'))
        hash_hex = hash_object.hexdigest()
        await socket.send(msn)
        print(await socket.recv())

        #Preparando criptografia
        key = os.urandom(32)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        msn_bytes = msn.encode('utf-8')
        padder = padding.PKCS7(128).padder()
        msn_bytes_padded = padder.update(msn_bytes) + padder.finalize()

        # ENCRIPTOGRAFANDO A MENSAGEM
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(msn_bytes_padded) + encryptor.finalize()

        users = {
            "sandro": "123456",
            "pedro": "987654",
            "jose": "010203",
        }

        def get_input(prompt):
            try:
                return input(prompt)
            except (EOFError, KeyboardInterrupt):
                return None

        def verify_user(user):
            return user in users

        def verify_password(user, password):
            return users[user] == password

        for _ in range(3):
            user = get_input("Digite o usuário: ")
            if user is not None:
                user = user.lower().strip()

            if verify_user(user):
                for _ in range(3):
                    password = get_input("Digite a senha: ")

                    if password is not None and verify_password(user, password.strip()):
                        print("Acesso autorizado!")
                        access = True
                        break
                    else:
                        print("Senha incorreta! Você tem mais {} tentativas.".format(2 - _))
                else:
                    print("Você excedeu o número de tentativas. Sistema encerrado!")
                    access = False
                    break
                break
            else:
                print("Usuário não encontrado! Você tem mais {} tentativas.".format(2 - _))
        else:
            print("Você excedeu o número de tentativas. Sistema encerrado!")
            access = False

        if access:
            decryptor = cipher.decryptor()
            plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(plaintext_padded) + unpadder.finalize()
            decodetext = plaintext.decode('utf-8')

            hash_object = hashlib.sha256()
            hash_object.update(decodetext.encode('utf-8'))
            hash_hex_rec = hash_object.hexdigest()
            if hash_hex_rec == hash_hex:
                print("Mensagem recebida integra")
                print(decodetext)
            else:
                print("Mensagem comprometida")


while True:
    asyncio.get_event_loop().run_until_complete(message())