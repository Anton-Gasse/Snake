# Snake

## Test it out
https://anton-gasse.de/snake

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
Play against AI Snake
* Use the AI Button to activate the AI opponent
* When the AI opponent is activatet you can switch between 2 Gamemodes (chasing the same or different apple)

## How to run it
1. Install the requirements:
```sh
pip install -r requirements.txt
```
2. Run the main script in the frontend folder:
```sh
cd frontend
```
```sh
python3 main.py
```

## How to run it in web browser
1. Adapt the URL in the [webmodel](./frontend/webmodel.py) class to your ip and port where you will run the Flask Server:
* It will be the same as in the [app.run()](./backend/app.py) method

2. Get the build folder of the app in the frontend folder:
```sh
cd frontend
```
```sh
python3 -m pygbag --build --ume_block 0 --can_close 1 --title snake --app_name snake main.py
```
3. Add [this script tag](./frontend/add-to-html.txt) to the [this body tag](./frontend/build/web/index.html#L349)
4. Run the Flask Server in the snake folder:
```sh
cd ..
```
```sh
python3 ./backend/app.py
```

## How to Dockerize the web app
1. Run the build command:
```sh
docker build -t snake .
```
2. Run the run command:
```sh
docker run --name snake -p <port>:<port> snake
```

