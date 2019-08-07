#!/usr/bin/env python
# coding: utf-8

# In[2]:


from abc import ABC, abstractmethod
import pygame
import random


# In[3]:


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


# In[4]:


class AbstractObject(ABC):
    def __init(self):
        pass
    
    @abstractmethod
    def draw(self, display):
        pass


# In[5]:


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


# In[6]:


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)
        
    def draw(self, display):
        display.draw_object(self.sprite, self.position)


# In[7]:


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 3
        
    def draw(self, display):
        display.draw_object(self.sprite, self.position)


# In[8]:



class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp
        self.exp=xp
        
   
    def interact(self, engine, hero):
        
        
        if random.randint(1,2) == 1:
            hero.hp -= int(self.hp/5)
            engine.notify(f'Enemy hit {int(self.hp/5)} damage')
            if hero.hp > 0:
                hero.exp += self.exp
                for m in hero.level_up():
                    engine.notify(m)
                
                engine.notify(f'You earned {self.exp} expirience')
            else:
                engine.notify("Game Over")
                engine.notify("Please, RESTART the GAME")
                engine.game_process = False
        else:
            hero.exp += self.exp
            for m in hero.level_up():
                engine.notify(m)
           
            engine.notify(f'You earned {self.exp} expirience')
        
 


# In[9]:


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * self.level * 8:
            yield "Level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp
            
            
            
    def level_next(self):
        
            
        self.level += 1
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["luck"] += 2
        self.calc_max_HP()
        self.hp = int(self.max_hp)
        


# In[10]:


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        self.calc_max_HP()
        if self.max_hp < self.hp:
            self.hp = self.max_hp


# In[11]:


class Berserk(Effect):
    def apply_effect(self):
        self.stats["strength"] += 7
        self.stats["endurance"] += 7
        self.stats["intelligence"] += 7
        self.stats["luck"] += 7
        super().apply_effect()
        
        
        


# In[12]:


class Blessing(Effect):
    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["intelligence"] += 2
        self.stats["luck"] += 2
        super().apply_effect()


# In[13]:


class Weakness(Effect):
    def apply_effect(self):
        self.stats["strength"] -= 3 
        self.stats["endurance"] -= 3
        self.stats["intelligence"] -= 3
        super().apply_effect()
        


# In[ ]:





# In[ ]:




