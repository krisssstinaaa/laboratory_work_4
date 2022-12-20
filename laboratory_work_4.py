import random

from PIL import Image, ImageDraw

def neighbors(p):

    x, y = p
    return (
        (x+1, y+1),
        (x+1, y-1),
        (x-1, y-1),
        (x-1, y+1),
        (x+1, y),
        (x-1, y),
        (x, y-1),
        (x, y+1)
    )

width, height = (960, 540)

file = open('DS0.txt')

dataset = []

for line in file.readlines():
    p = tuple(map(int, line.split()))[::-1]
    dataset.append(p)
file.close()
s = set(dataset)

groups = []

while len(s) != 0:
    queue = []
    v = set()

    el = next(iter(s))

    queue.append(el)
    v.add(el)
    s.remove(el)

    while len(queue) != 0:
        q = queue.pop(0)
        for p in neighbors(q):
            if p not in v:
                if p in s:
                    v.add(p)
                    queue.append(p)
                    s.remove(p)

    groups.append(v)

colors = dict()
for group in groups:
    x, y = 0.0, 0.0
    for p in group:
        x += p[0]/len(group)
        y += p[1]/len(group)
    
    avg = int(x), int(y)
    colors[avg] = (
        random.randint(70, 210),
        random.randint(70, 210),
        random.randint(70, 210)
    )
    
image = Image.new('RGBA', (width, height), (255,255,255,255))
image_draw = ImageDraw.Draw(image)

for j in range(0, height):
    for i in range(0, width):
        closest = min(colors.keys(), key=
            lambda x: (i - x[0]) ** 2 + (j - x[1]) ** 2)
        image.putpixel((i, j), colors[closest])

for el in colors.keys():
    x, y = el
    image_draw.ellipse(
        (x-2.5, y-2.5, x+2.5, y+2.5),
        (0, 0, 0, 255)
    )

image2 = Image.new('RGBA', (width, height), (0,0,0,0))

for el in dataset:
    image2.putpixel(el, (0, 0, 0, int(0.1 * 255)))
    
result = Image.alpha_composite(image, image2)
result.save('image4.png')