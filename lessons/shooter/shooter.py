from fast2d import Window, Text, Sprite, Key, Box, Image
import random

"""
Simple top-down shooter implementation

Graphics by: Andrea De Dominicis
"""

# instantiate the game window
window = Window(800, 600)


class Score(Text):
    """
    The Score object is used for displaying texts
    """
    def update(self):
        if self.ship.destroyed:
            # red
            self.set_color(255, 0, 0)
            self.text = 'GAME OVER - SCORE: {}'.format(self.ship.total_score)
            self.draw()
            return
        # white
        self.set_color(255, 255, 255)
        self.text = 'SCORE: {}'.format(self.ship.total_score)
        self.draw()


class Enemy(Sprite):
    """
    Grunt enemy (low-energy)
    """
    def __init__(self, filename):
        super(Enemy, self).__init__(filename)
        self.enabled = False
        # self.bounding_box = Box(8, 45, self.width-14, self.height-74,
        #                          255, 255, 0, 50)
        self.bounding_box = Box(8, 45, self.width-14, self.height-74)
        self.speed = 100
        self.max_energy = 1
        self.energy = self.max_energy

    def update(self):
        if not self.enabled:
            return

        self.y -= self.speed * window.delta_time

        # disable the enemy when it is out of the screen
        if self.y+self.height < 0:
            self.enabled = False
            return

        self.draw()
        # update the bounding box (required for collisions)
        self.bounding_box.draw(self.x, self.y)


class Boss(Sprite):
    """
    Boss enemy (high-energy)
    """
    def __init__(self, filename):
        super(Boss, self).__init__(filename)
        self.enabled = False
        # self.bounding_box = Box(40, 10, self.width-80, self.height-20,
        #                         255, 255, 0, 50)
        self.bounding_box = Box(40, 10, self.width-80, self.height-20)
        self.speed = 100
        self.max_energy = 5
        self.energy = self.max_energy

    def update(self):
        if not self.enabled:
            return

        self.y -= self.speed * window.delta_time

        if self.y+self.height < 0:
            self.enabled = False
            return

        self.draw()
        # update the bounding box (required for collisions)
        self.bounding_box.draw(self.x, self.y)


class EnemySpawner(object):
    """
    This class manages the spawn of enemies (included bosses)
    """

    def __init__(self):
        self.enemies = []
        for i in range(0, 10):
            self.enemies.append(Enemy('enemy.png'))
        self.boss = Boss('boss.png')
        # add the boss to the list of enemies for allowing
        # it t be checked by the collision system
        self.enemies.append(self.boss)
        self.frequency = 1
        # counter for managing the spawn time
        self.t = 0
        # this is incresed at every enemy spawn
        self.spawns = 0
        self.enemies_speed = 100

    def update(self):
        if self.t > 0:
            self.t -= window.delta_time

        if self.t > 0:
            return

        # check for boss
        if self.spawns > 0 and self.spawns % 30 == 0:
            # the boss is till on the stage
            # wait a bit
            if self.boss.enabled:
                return
            self.boss.speed = self.enemies_speed/3
            self.boss.x = random.randint(0, window.width-self.boss.width)
            self.boss.y = window.height
            self.boss.energy = self.boss.max_energy
            self.boss.enabled = True

        for enemy in self.enemies:
            # avoid spawning a boss
            if enemy == self.boss:
                continue
            if enemy.enabled:
                continue
            # increase enemies speed every 20 spawns
            if self.spawns % 20 == 0:
                self.enemies_speed += 50
            enemy.speed = self.enemies_speed
            enemy.x = random.randint(0, window.width-enemy.width)
            enemy.y = window.height
            enemy.energy = enemy.max_energy
            enemy.enabled = True
            self.spawns += 1
            # reset the timer
            self.t = self.frequency
            return


class Bullet(Sprite):
    """
    This class implements a single Bullet shot by the Ship
    """
    def __init__(self, filename):
        super(Bullet, self).__init__(filename)
        self.enabled = False
        # self.bounding_box = Box(2, 4, self.width-6, self.height-8,
        #                         255, 255, 0, 50)
        self.bounding_box = Box(2, 4, self.width-6, self.height-8)

    def update(self):
        if not self.enabled:
            return

        speed = 400
        self.y += speed * window.delta_time

        if self.y > window.height:
            self.enabled = False
            return

        self.draw()
        self.bounding_box.draw(self.x, self.y)

        if self.check_collisions():
            self.enabled = False

    def check_collisions(self):
        for enemy in self.owner.enemies:
            if not enemy.enabled:
                continue
            if enemy.bounding_box.intersects(self.bounding_box):
                enemy.energy -= 1
                # destroy enemy when energy reaches 0 and increse score
                if enemy.energy <= 0:
                    enemy.enabled = False
                    self.owner.total_score += 1
                return True
        return False


class Ship(Sprite):
    """
    The Player class
    """
    def __init__(self, filename):
        super(Ship, self).__init__(filename)
        # use a pool of bullets
        self.bullets = []
        for i in range(0, 10):
            self.bullets.append(Bullet('shot.png'))
        # cooldown is required for avoiding bullets storm
        self.cool_down = 0.15
        self.cool_down_t = 0

        # frames for right/left movements
        self.right = Image('ship_right.png')
        self.left = Image('ship_left.png')

        # self.bounding_box = Box(25, 10, self.width-50, self.height-18,
        #                         255, 255, 0, 50)
        self.bounding_box = Box(25, 10, self.width-50, self.height-18)

        # when True, we have a game over
        self.destroyed = False

        self.total_score = 0

    def fix_position(self):
        """
        Ensure the ship is not out of window bounds
        """
        if self.x < 0:
            self.x = 0
        if self.x+self.width > window.width-1:
            self.x = window.width-self.width-1
        if self.y < 0:
            self.y = 0
        if self.y+self.height > window.height-1:
            self.y = window.height-self.height-1

    def manage_shot(self):

        if self.cool_down_t > 0:
            self.cool_down_t -= window.delta_time

        if self.cool_down_t > 0:
            return

        if not window.get_key(Key.SPACE):
            return

        # manage pool
        for bullet in self.bullets:
            if bullet.enabled:
                continue
            bullet.x = self.x + self.width/2 - bullet.width/2
            bullet.y = self.y + self.height/2
            bullet.enabled = True
            self.cool_down_t = self.cool_down
            return

    def update(self):
        if self.destroyed:
            return

        speed = 200

        # default image
        image = self

        if window.get_key(Key.RIGHT):
            self.x += speed * window.delta_time
            image = self.right
        if window.get_key(Key.LEFT):
            self.x -= speed * window.delta_time
            image = self.left
        if window.get_key(Key.UP):
            self.y += speed * window.delta_time
        if window.get_key(Key.DOWN):
            self.y -= speed * window.delta_time

        self.manage_shot()

        self.fix_position()

        self.draw(image)

        self.bounding_box.draw(self.x, self.y)

        if self.check_collisions():
            self.destroyed = True

    def check_collisions(self):
        for enemy in self.enemies:
            if not enemy.enabled:
                continue
            if enemy.bounding_box.intersects(self.bounding_box):
                return True
        return False

# the list of game objects
game_objects = []

# spawn the ship
ship = Ship('ship.png')
game_objects.append(ship)

# spawn the spawner and the enemies
spawner = EnemySpawner()
game_objects.append(spawner)
for enemy in spawner.enemies:
    game_objects.append(enemy)

# allocate the bullets
for bullet in ship.bullets:
    game_objects.append(bullet)
    # set the bullet owner, one day we could have a second player
    bullet.owner = ship

# instantiate the score
score = Score()
score.ship = ship
game_objects.append(score)

# hold the list of enemies
ship.enemies = spawner.enemies


# the game loop
def game_loop():
    window.clear(0, 0, 0)
    for game_object in game_objects:
        game_object.update()

window.run(game_loop)
