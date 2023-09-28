import websockets
import asyncio


#Função chamada quando o cliente se conectar
async def response(websockets, path):
    msn =await websockets.recv()
    print(f'Mensagem recebida: {msn}')
    await websockets.send("Mensagem recebida!")

start_server = websockets.serve(response, '0.0.0.0', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()