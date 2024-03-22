# Snake

## Test it out
https://anton-gasse.github.io/Snake/

![standard map](https://github.com/Anton-Gasse/Snake/blob/main/frontend/utils/readme_snake.png?raw=true)

## How to Play
* Keyboard: use WASD or Arrow-Keys to change the direction of the Snake
* Touch: tap the area of the screen in which direction the snake should go

## Customize
You can customize the map by clicking the edit button (top-left-corner)
* Left Click to add/delete a border
* When the Snake goes off the map it teleports to the other side (don't forget to open it)

![custom map](https://github.com/Anton-Gasse/Snake/blob/main/frontend/utils/readme_snake_custom.png?raw=true)

## AI Snake
Play against AI Snake (just local)
* Use the AI Button to activate the AI opponent (top-right corner)
* When the AI opponent is activatet you can switch between 2 Gamemodes (chasing the same or different apple)

## How to run it
Install the requirements:
```sh
pip install -r requirements.txt
```
Run the main script in the frontend folder:
```sh
cd frontend
```
```sh
python3 main.py
```

## How to run it in browser
Adapt the URL in the [webmodel](./frontend/webmodel.py) class to your ip and port where you will run the Flask Server:
* It will be the same as in the [app.run()](./backend/app.py) method

Get the build folder of the app in the frontend folder:
```sh
cd frontend
```
```sh
python3 -m pygbag --build --app_name snake main.py
```
Run the Flask Server:
```sh
python3 ./backend/app.py
```

## How to Dockerize it
Run the build command:
```sh
docker build -t snake .
```
Run the run command:
```sh
docker run --name snake -p <port>:<port> snake
```

## Coming Soon
Play in web against AI Snake
