import sys
import os
#import numpy as np
import platform
import asyncio
import json

class Webmodel():
    def __init__(self) -> None:
        self.is_emscripten = sys.platform == "emscripten"
        self.url = "https://127.0.0.1:443/prediction"
        if self.is_emscripten:
            
            self._js_code = """
window.Fetch = {}
// generator functions for async fetch API
// script is meant to be run at runtime in an emscripten environment
// Fetch API allows data to be posted along with a POST request
window.Fetch.EMIT = function* EMIT (obs)
{
    socket = window.init.socket;
    socket.emit("prediction", {obs: obs}); 
}
window.Fetch.CHECK_UPDATE = function* CHECK_UPDATE ()
{
    if (window.init.next_move != "nothing"){
        tmp = window.init.next_move;
        window.init.next_move = "nothing";
        yield tmp;
    }
    else {
        yield "nothing";
    }
}
            """
            try:
                platform.window.eval(self._js_code)
                
                
            except AttributeError:
                self.is_emscripten = False
                print("mist")

            

    async def emit(self, obs:tuple[int, int, int, int, int, int, int]) -> int:
        #data = {'obs': np.array([[obs]]).astype(np.float32)}
        action = 1#await self.post(data=data) 
        await platform.jsiter(platform.window.Fetch.EMIT(json.dumps(obs, ensure_ascii=False)))
        
    
    async def check_update(self):
        next_move = await platform.jsiter(platform.window.Fetch.CHECK_UPDATE())
        return next_move
    
    async def post(self, data:dict=None):
        if data is None:
            data = {}
        if self.is_emscripten:
            await asyncio.sleep(0)
            content = await platform.jsiter(platform.window.Fetch.POST(self.url, json.dumps(data, ensure_ascii=False)))
            result = content
            
            return result
        return ""
