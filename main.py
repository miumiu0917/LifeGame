import copy
import os
import random
import time
import sys
from PIL import Image
from tqdm import tqdm
import numpy as np

FIELD_HEIGHT = 100
FIELD_WIDTH = 100

STEP = 500

FRIEND = 'o'
ENEMY = 'x'


def row():
  return ['*'] + [FRIEND if i >= FIELD_WIDTH / 2 else ENEMY for i in range(FIELD_WIDTH)] + ['*']


def field():
  top = ['*' for _ in range(FIELD_WIDTH + 2)]
  bottom = ['*' for _ in range(FIELD_WIDTH + 2)]
  return [top] + [row() for _ in range(FIELD_HEIGHT)] + [bottom]

def main():
  f = field()
  for i in tqdm(range(STEP)):
    f = _next(f)
    output_field(f, step=i)
  os.system('convert -delay 5 -loop 0 ./tmp/*.png ./output/movie.gif')
  os.system('rm ./tmp/*.png')
    

def _next(f):
  n = copy.deepcopy(f)
  for i in range(1, FIELD_HEIGHT+1):
    for j in range(1, FIELD_WIDTH+1):
      n[i][j] = next_state(f, i, j)
  return n


def next_state(f, i, j):
  s = f[i][j]
  e = environment(f, i, j)
  if all(map(lambda x: x == s, e)):
    return s
  else:
    num_friend = len(list(filter(lambda x: x == s, e)))
    num_enemy = len(list(filter(lambda x: x != s, e)))
    prob = 50 + (num_friend - num_enemy) * 6
    alive = random.randint(0, 100) < prob
    if alive:
      return FRIEND if s == FRIEND else ENEMY
    else:
      return ENEMY if s == FRIEND else FRIEND


def _prob(s):
  return 55 if s == FRIEND else 45


def output_field(f, step):
  f = list(filter(lambda x: not all(list(map(lambda e: e == '*', x))) , f))
  f = list(map(lambda x: list(filter(lambda e: e != '*', x)), f))
  f = list(map(lambda x: list(map(object2color ,x)) ,f))
  arr = np.array(f, dtype=np.int8)
  image = Image.fromarray(arr.astype('uint8'))
  image.save('./tmp/' + '%07d.png' % step) 

def object2color(x):
  if x == ENEMY:
    return [255, 0, 0]
  else:
    return [0, 255, 0]  


def environment(f, i, j):
  e = []
  for _i in range(i-1, i+2):
    for _j in range(j-1, j+2):
      if _i == i and _j == j:
        continue
      e.append(f[_i][_j])
  return list(filter(lambda x: x != '*', e))

if __name__ == '__main__':
  main()