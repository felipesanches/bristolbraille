import pygame, sys
from PIL import Image
pygame.init()
import pickle

state_file = 'coords'
crop = 200
offset=400

def displayImage(screen, px, topleft, prior):
    # ensure that the rect always has positive width, height
    x, y = topleft
    width =  pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)

def setup(path):
    img = Image.open(input_loc)
    (x,y)=img.size
    img = img.crop(( x/2-crop,y/2-crop+offset,x/2+crop,y/2+crop+offset))
    crop_loc="cropped.jpg"
    img.save(crop_loc)
    px = pygame.image.load(crop_loc)
    print px.get_rect()
    (width,height) = px.get_rect()[2:]
    #bg = pygame.transform.scale(px, (width/scaling,height/scaling))
    screen = pygame.display.set_mode( px.get_rect()[2:] )
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px, (x,y)

def mainLoop(screen, px):

    topleft = bottomright = prior = None
    n=0
    while n!=1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = event.pos
                else:
                    bottomright = event.pos
                    n=1
        if topleft:
            prior = displayImage(screen, px, topleft, prior)
    return ( topleft + bottomright )

if __name__ == "__main__":
    input_loc = 'capt0000.jpg'
    output_loc = 'out.png'
    screen, px, (x,y) = setup(input_loc)
    print px
    dim = mainLoop(screen, px)
    f=open(state_file,'w')
    new_dim = [ dim[0]+x/2-crop,
        dim[1]+y/2-crop+offset,
        dim[2]+x/2-crop,
        dim[3]+y/2-crop+offset, ]
    print new_dim
    pickle.dump(new_dim,f)
    """
    # ensure output rect always has positive width, height
    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower
    im = Image.open(input_loc)
    #multiply by 2 to make up for the scale
    im = im.crop(( left*2, upper*2, right*2, lower*2))
    im = pygame.transform.rotate(im, 90)

    im.save(output_loc)
    """
    pygame.display.quit()
