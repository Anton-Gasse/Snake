import sys
import os
import platform
import asyncio
import json


class Webmodel():
    def __init__(self) -> None:
        self.is_emscripten = sys.platform == "emscripten"
        self.url = "https://192.168.0.239:443/prediction"
        POST = "POST"
        if self.is_emscripten:
            self._js_code = """
window.Fetch = {}
// generator functions for async fetch API
// script is meant to be run at runtime in an emscripten environment
// Fetch API allows data to be posted along with a POST request
window.Fetch.POST = function * POST (url, data)
{
    // post info about the request
    //console.log('POST: ' + url + 'Data: ' + data);
    var request = new Request(url, {headers: {'Accept': 'application/json','Content-Type': 'application/json'},
        method: 'POST',
        body: data});
    var content = 'undefined';
    fetch(request)
   .then(resp => resp.text())
   .then((resp) => {
        //console.log(resp);
        content = resp;
   })
   .catch(err => {
         // handle errors
         console.log("An Error Occurred:")
         console.log(err);
    });
    while(content == 'undefined'){
        yield;
    }
    yield content;
}
// Only URL to be passed
// when called from python code, use urllib.parse.urlencode to get the query string
window.Fetch.GET = function * GET (url)
{
    console.log('GET: ' + url);
    var request = new Request(url, { method: 'GET' })
    var content = 'undefined';
    fetch(request)
   .then(resp => resp.text())
   .then((resp) => {
        console.log(resp);
        content = resp;
   })
   .catch(err => {
         // handle errors
         console.log("An Error Occurred:");
         console.log(err);
    });
    while(content == 'undefined'){
        // generator
        yield;
    }

    yield content;
}
            """
            try:
                platform.window.eval(self._js_code)
            except AttributeError:
                self.is_emscripten = False
                print("mist")


    async def predict(self, obs:tuple[int, int, int, int, int, int, int]) -> int:
        data = {'obs': obs}
        action = await self.post(data=data) 
        return action
    
    async def post(self, data:dict=None):
        if data is None:
            data = {}
        if self.is_emscripten:
            await asyncio.sleep(0)
            content = await platform.jsiter(platform.window.Fetch.POST(self.url, json.dumps(data, ensure_ascii=False)))
            result = content
            
            return result
        return ""