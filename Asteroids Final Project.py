from designer import *
from random import randint
# This is the world dictionary, everything that is going to be visible in the game will be put in here
World = { 'background': DesignerObject,
          'spaceship': DesignerObject,
          'spaceship speed': int,
          'direction': str,
          'asteroids': [DesignerObject],
          'score': int,
          'counter': DesignerObject,
          'star': [DesignerObject],
          'lasers': [DesignerObject],
          'aliens': [DesignerObject],
          'astronauts': [DesignerObject],
          'highscore': int,
          'highscore display': DesignerObject}

#Background
def create_background() -> DesignerObject:
    '''
    This function creates the backround image of space in the game. It turns the string 'space.jpg' into an image by using the image()
    function and an image that I chose in the same directory. It then scales the image to 0.3 an returns the image
    '''
    space = image('space.jpg')
    space['scale'] = 0.3
    return space

#Spaceship Movement
def create_spaceship() -> DesignerObject:
    '''
    This function creates the spaceship that will be used to fly around and collect points, it uses the same proccess as the
    create_background function except it also sets the y position to 500
    '''
    spaceship = image("spaceship.png")
    spaceship['scale'] = 0.08
    spaceship['y'] = 500
    return spaceship
#This is the speed of the spaceship which when done making all the helper functions will be 12.5 pixels per update
speed = 12.5
def movement(world: World):
    '''
    This function checks checks what the direction of the spaceship is and uses the go_right, go_left, go_up, go_down helper functions
    to move the spaceship the speed of the spaceship with each update
    '''
    if world['direction'] == 'right':
        go_right(world)
    elif world['direction'] == 'left':
        go_left(world)
    elif world['direction'] == 'up':
        go_up(world)
    elif world['direction'] == 'down':
        go_down(world)
    
def flip_spaceship(world: World, key: str):
    '''
    This function takes the key input from the player and sets the direction to that key, then uses helper functions to move the spaceship
    '''
    if key == 'up':
        world['direction'] = key
        go_up(world)
    elif key == 'down':
        world['direction'] = key
        go_down(world)
    elif key == 'right':
        world['direction'] = key
        go_right(world)    
    elif key == 'left':
        world['direction'] = key
        go_left(world)

def go_right(world: World):
    '''
    This is a helper function used to increase the x position each time making the spaceship go right
    '''
    world['spaceship']['x'] += world['spaceship speed']

def go_left(world: World):
    '''
    This is a helper function used to decrease the x position each time making the spaceship go left
    '''
    world['spaceship']['x'] -= world['spaceship speed']    

def go_up(world: World):
    '''
    This is a helper function used to decrease the y position each time making the spaceship go up
    '''
    world['spaceship']['y'] -= world['spaceship speed']

def go_down(world: World):
    '''
    This is a helper function used to increase the y position each time making the spaceship go down
    '''
    world['spaceship']['y'] += world['spaceship speed']

def wrap_around(world: World):
    '''
    This function checks the position of the spaceshp and if it is past the dimentions of the screen it will mae it wrap around the
    other side by set it to a new position.
    '''
    if world['spaceship']['x'] > 800:
        world['spaceship']['x'] = 0
    elif world['spaceship']['x'] < 0:
        world['spaceship']['x'] = 800
    elif world['spaceship']['y'] > 600:
        world['spaceship']['y'] = 0
    elif world['spaceship']['y'] < 0:
        world['spaceship']['y'] = 600

#Obstacles
#Asteroids
'''
There are three different sized asteroids, large, medium, and small, the asteroids will get smaller each time its shot with a laser.
Once a small asteroid is shot it will be destroyed. If the spaceship hits an asteroid at any time the game will end.
'''
#The speed is set so the asteroids will fall 1.5 pixels every update
asteroid_speed = 1.5
def create_asteroid() -> DesignerObject:
    '''
    This function creates the asteroids in the same way it created the spaceship and background. The asteroids will spawn at y = 0,
    and I imported the randint function to have the asteroids spawn on the x axis anywhere from 0 to the max width of the screen.
    '''
    asteroid = image('asteroid.png')
    asteroid['scale'] = 0.15
    asteroid['y'] = 0
    asteroid['x'] = randint(0, get_width())
    return asteroid

def make_asteroids(world: World):
    '''
    This function makes the asteroids actually appear in the world. It doesn't allow any more than 5 asteroids appear at a time.
    It puts asteroids in the world by appending it to a list. Using the randint function I set the chance of an asteroid spawning at
    1 out of 25
    '''
    not_too_many_asteroids = len(world['asteroids']) <= 4
    random_chance = randint(1, 25) == 1
    if not_too_many_asteroids and random_chance:
        world['asteroids'].append(create_asteroid())

def make_asteroids_fall(world: World):
    '''
    This function is what actually makes the asteroids fall down the screen with by changing the postion with each update.
    '''
    for asteroid in world['asteroids']:
        asteroid['y'] += asteroid_speed
        
def asteroid_off_screen(world):
    '''
    This function removes an asteroid in the world if it falls below the screen. It does this by checking if the asteroid is on the
    screen, if it is it appends the asteroid to a new list on_screen and sets world['asteroids'] to on_screen
    '''
    on_screen = []
    for asteroid in world['asteroids']:
        if asteroid['y'] < get_height():
            on_screen.append(asteroid)
    world['asteroids'] = on_screen

#Alien
'''
Aliens will randomly fly from the left side of the screen less often than asteroids but they are faster and come without warning.
If your spaceship hits an alien the game is over.
'''
def create_alien()->DesignerObject:
    '''
    This function creates alien the same way it created the other images in the game. It sets the x position to 0 and the y positon
    to anywhere from 0 to the max height of the screen
    '''
    alien = image('alien.png')
    alien['scale'] = 0.2
    alien['y'] = randint(0, get_height())
    alien['x'] = 0
    return alien

def spawn_alien(world: World):
    '''
    This function is what actually spawns the aliens in the game, just like it spawns asteroids. It won't let any more than 2 aliens be
    on the screen at one time. The chance of an alien spawning is 1 in 200.
    '''
    max_spawn = len(world['aliens']) <= 1
    random_chance = randint(1, 200) == 1
    if max_spawn and random_chance:
        world['aliens'].append(create_alien())

def move_alien(world: World):
    '''
    This function is what make the alien move with each update. The speed of an alien is 30 pixels every update
    '''
    for alien in world['aliens']:
        alien['x'] += 30

def destroy_alien(world):
    '''
    This function destroys aliens that are off screen.
    '''
    on_screen = []
    for alien in world['aliens']:
        if alien['x'] < get_width():
            on_screen.append(alien)
    world['aliens'] = on_screen

#Astronaut
'''
Astronauts are collectables that give you 5 points if collected, they spawn less often than stars and fly from the right side.
'''
def create_astronaut()->DesignerObject:
    '''
    This function creates the astronaut the same way the space, spacehship, asteroids, and alien were created.
    It set the y to 0 and the x position anywhere from 0 to the max height of the screen
    '''
    astronaut = image('astronaut.png')
    astronaut['scale'] = 0.5
    astronaut['y'] = randint(0, get_height())
    astronaut['x'] = get_width()
    return astronaut

def spawn_astronaut(world: World):
    '''
    This function is what spawns the astornaut in the world. It works the exact same way as the spawn_alien and make_asteroids function
    The chance of an astornaut spawning is 1 in 200 with every update. Only 2 astronauts can be in the world at once.
    '''
    max_spawn = len(world['astronauts']) <= 1
    random_chance = randint(1, 200) == 1
    if max_spawn and random_chance:
        world['astronauts'].append(create_astronaut())
        
def move_astronaut(world: World):
    '''
    This function moves the astronaut by updating its positon with each update. The speed of an astronaut is 15 pixels every update
    '''
    for astronaut in world['astronauts']:
        astronaut['x'] -= 15
        
def destroy_astronaut(world: World):
    '''
    This function destroys an astronaut once it leaves the screen the exact same way the destroy_alien function does
    '''
    on_screen = []
    for astronaut in world['astronauts']:
        if astronaut['x'] > 0:
            on_screen.append(astronaut)
    world['astronauts'] = on_screen

#Stars
'''
Stars are collectables that spawn and give you 1 point if collected
'''
def create_star() -> DesignerObject:
    '''
    This function creates the stars the same way every other image was created. The y and x coordinated are both random using the randint
    function and can spawn anywhere on the screen
    '''
    star = image('star.png')
    star['scale'] = 0.02
    star['y'] = randint(50, 550)
    star['x'] = randint(50, 750)
    return star

def spawn_star(world: World):
    '''
    This function spawns a star the same way the asteroids, aliens, and astronauts were spawned in. No more than 21 stars will be on the
    screen at once.
    '''
    star_limit = len(world['stars']) <= 20
    random_chance = randint(1, 50) == 1
    if star_limit and random_chance:
        world['stars'].append(create_star())

#Projectile
#The speed of the laser is 25 pixels per update
laser_speed = 25
def create_laser()->DesignerObject:
    '''
    This function creates the image for the laser that same way all other image were created.
    '''
    laser = image("laser.png")
    laser['scale'] = 0.3
    return laser

def shoot_laser(world: World, key: str):
#    This function allows for the user to shoot a laser out of the spaceship when the space bar is pressed, it uses the helper move_above
#    function to make the laser continuously move once shot
        if key == 'space':
            new_laser = create_laser()
            move_above(new_laser, world['spaceship'])
            world['lasers'].append(new_laser)

def move_above(bottom: DesignerObject, top: DesignerObject):
#    This function will make the laser continously move upwards and give it the apperance of being shot out of the spaceship by updating
#    its position to above its previous position with each update
        bottom['y'] = top['y']
        bottom['x'] = top['x'] 

def make_lasers_move(world):
    '''
    This function is what make the laser move upwards with each update
    '''
    for laser in world['lasers']:
        laser['y'] -= laser_speed

def laser_off_screen(world):
    '''
    This function destroys a laser once it if offscreen the same way it does for the asteroids, aliens, and astronauts
    '''
    on_screen = []
    for laser in world['lasers']:
        if laser['y'] < 0:
            on_screen.append(laser)
    world['lasers'] = on_screen
            
#Colliding
'''
These functions create the intereaction between the different objects in the world
'''
def collide_spaceship_asteroid(world:World):
    '''
    This function creates the interaction between asteroids and the spaceship. If the spaceship and asteroid collide both will be
    destroyed and the game will end
    '''
    destroyed_asteroid = []
    for asteroid in world['asteroids']:
        if colliding(world['spaceship'], asteroid):
            destroyed_asteroid.append(asteroid)
            world['asteroids'] = filter_from(world['asteroids'], destroyed_asteroid)
            world['spaceship']['visible'] = False
            pause()
                
def collide_spaceship_star(world: World):
    '''
    This function creates the interaction between the spaceship and stars, if the spaceship and a star collide the star will be destroyed
    and the score will go up by one.
    '''
    destroyed_star = []
    for star in world['stars']:
        if colliding(world['spaceship'], star):
            destroyed_star.append(star)
            world['stars'] = filter_from(world['stars'], destroyed_star)
            world['score'] += 1

def collide_laser_asteroid(world: World):
    '''
    This function creates the interaction between asteroids and lasers, if a laser collides with a large asteroid, it will scale down
    to a medium asteroid, which them it hit again will scale down to a small asteroid, which will be destoryed if  hit once more. Each
    time a laser collides with an asteroid, the laser is destroyed.
    '''
    destroyed_asteroid = []
    destroyed_laser = []
    for laser in world['lasers']:
        for asteroid in world['asteroids']:
            if colliding(laser, asteroid):
                destroyed_laser.append(laser)
                world['lasers'] = filter_from(world['lasers'], destroyed_laser)
                asteroid['scale'] = 0.1
                if colliding(laser, asteroid):
                    destroyed_laser.append(laser)
                    world['lasers'] = filter_from(world['lasers'], destroyed_laser)
                    asteroid['scale'] = 0.05
                    if colliding(laser, asteroid):
                        destroyed_laser.append(laser)
                        world['lasers'] = filter_from(world['lasers'], destroyed_laser)
                        destroyed_asteroid.append(asteroid)
                        world['asteroids'] = filter_from(world['asteroids'], destroyed_asteroid)
                
def collide_alien_spaceship(world: World):
    '''
    This function creates the interaction between the aliens and the spaceship. If an alien and spaceship collide they are both destroyed
    and the game ends
    '''
    destroyed_alien = []
    for alien in world['aliens']:
        if colliding(alien, world['spaceship']):
            destroyed_alien.append(alien)
            world['aliens'] = filter_from(world['aliens'], destroyed_alien)
            world['spaceship']['visible'] = False
            pause()
            
def collide_astronaut_spaceship(world: World):
    '''
    This function creates the interaction between the astronaut and spaceship. If they collide the astronaut is destroyed and the score
    goes up by 5
    '''
    destroyed_astronaut = []
    for astronaut in world['astronauts']:
        if colliding(astronaut, world['spaceship']):
            destroyed_astronaut.append(astronaut)
            world['astronauts'] = filter_from(world['astronauts'], destroyed_astronaut)
            world['score'] += 5

def filter_from(old_list: list, elements_to_not_keep: list) -> list:
    '''
    This is a helper function inspired from the firefighter game lesson, it removes any items in the new list, which are destoryed items,
    from the world
    '''
    new_values = []
    for item in old_list:
        if item not in elements_to_not_keep:
            new_values.append(item)
    return new_values

#Counter
def update_counter(world):
    '''
    This function is the update counter and updates the score with each update
    '''
    world['counter']['text'] = str(world['score'])
    
highscore = 0
def high_score(world):
    if world['score'] >= world['highscore']:
        world['highscore'] = world['score']
        world['highscore display']['text'] = world['highscore']
    

#World
def create_world() ->World:
    '''
    This function creates the world that we see and play the game in, it uses the same dictionary as the World that I made at the top of my code
    '''
    return {'background': create_background(),
            'spaceship': create_spaceship(),
            'spaceship speed': speed,
            'direction': '',
            'asteroids': [],
            'score': 0,
            'counter': text('white', '', 40, 50, 550),
            'stars': [],
            'lasers': [],
            'aliens': [],
            'astronauts': [],
}
#Start Game
'''
These when functions are what make the game actually start and run, it runs the function we created with each update or when a key is
pressed depending on what is specified.
'''
when('starting', create_world)
when('updating', movement)
when('typing', flip_spaceship)
when('updating', wrap_around)
when('updating', make_asteroids)
when('updating', make_asteroids_fall)
when('updating', asteroid_off_screen)
when('updating', spawn_star)
when('updating', spawn_alien)
when('updating', move_alien)
when('updating', destroy_alien)
when('updating', spawn_astronaut)
when('updating', move_astronaut)
when('typing', shoot_laser)
when('updating', make_lasers_move)
when('updating', collide_spaceship_asteroid)
when('updating', collide_spaceship_star)
when('updating', collide_laser_asteroid)
when('updating', collide_alien_spaceship)
when('updating', collide_astronaut_spaceship)
when('updating', update_counter)
start() 