from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

connected_clients = []

@app.websocket('/ws') # 标记endpoint为websocket
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() # async wait client's handshake, prepare to send message, 如果不accept, client can not build websocket connection 
    # handshake builded, print message below 
    print('Client Connected')
    
    connected_clients.append(websocket)
    try: 
        while True:
            data = await websocket.receive_text() # 等待client message并apply to data 
            message = json.loads(data)
            print(f'message received {message}')

            for client in connected_clients: # 可能有多个client连接当前server, 所以
                await client.send_json({ # 发送消息给当前连接的clients 否则是发给单一的client 
                    "type": "message",
                    "text": message['text']
                })
    except Exception as e:
        print('error', e)
    
    finally:
        connected_clients.remove(websocket)
        
        for client in connected_clients:
                await client.send_json({
                    "type": "notification",
                    "text": "A client left"
                })
        

app.mount("/", StaticFiles(directory="static", html=True), name="static")