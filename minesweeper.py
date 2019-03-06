import sys
import time
from enum import Enum
import pygame
from pygame.locals import *
from mineblock import *
from agent import *

SCREEN_WIDTH = BLOCK_WIDTH * SIZE + 11 * SIZE

SCREEN_HEIGHT = BLOCK_HEIGHT * SIZE



def get_command(x,y):
    if BLOCK_WIDTH + 1 <= x < BLOCK_WIDTH + 5 and BLOCK_HEIGHT // 3 <= y <= BLOCK_HEIGHT // 3 +1:
        return "cover"
    elif BLOCK_WIDTH+6 <= x < BLOCK_WIDTH + 10 and BLOCK_HEIGHT // 3 <= y <= BLOCK_HEIGHT // 3 +1:
        return "uncover"
    elif BLOCK_WIDTH + 1 <= x < BLOCK_WIDTH + 5 and BLOCK_HEIGHT // 3 * 2 <= y <= BLOCK_HEIGHT // 3 * 2 +1:
        return "back"
    elif BLOCK_WIDTH+6 <= x < BLOCK_WIDTH + 10 and BLOCK_HEIGHT // 3 * 2 <= y <= BLOCK_HEIGHT // 3 * 2 +1:
        return "forward"
    else:
        return None

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Minesweeper')

    font1 = pygame.font.Font('resources/a.TTF', SIZE * 2)
    red = (200, 40, 40)

    control_width = int(SIZE * 4)
    control_height = int(SIZE * 2)
    img_cover = pygame.image.load('resources/Cover.bmp').convert()
    img_cover = pygame.transform.smoothscale(img_cover, (control_width, control_height))
    img_uncover = pygame.image.load('resources/Uncover.bmp').convert()
    img_uncover = pygame.transform.smoothscale(img_uncover, (control_width, control_height))
    img_forward = pygame.image.load('resources/forward.bmp').convert()
    img_forward = pygame.transform.smoothscale(img_forward, (control_width, control_height))
    img_back = pygame.image.load('resources/back.bmp').convert()
    img_back = pygame.transform.smoothscale(img_back, (control_width, control_height))

    cover_x = (BLOCK_WIDTH + 1) * SIZE
    cover_y = BLOCK_HEIGHT // 3 * SIZE
    uncover_x = (BLOCK_WIDTH + 6) * SIZE
    uncover_y = BLOCK_HEIGHT // 3 * SIZE
    back_x = (BLOCK_WIDTH + 1) * SIZE
    back_y = BLOCK_HEIGHT // 3 * SIZE * 2
    forward_x = (BLOCK_WIDTH + 6) * SIZE
    forward_y = BLOCK_HEIGHT // 3 * SIZE * 2

    img0 = pygame.image.load('resources/0.bmp').convert()
    img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
    img1 = pygame.image.load('resources/1.bmp').convert()
    img1 = pygame.transform.smoothscale(img1, (SIZE, SIZE))
    img2 = pygame.image.load('resources/2.bmp').convert()
    img2 = pygame.transform.smoothscale(img2, (SIZE, SIZE))
    img3 = pygame.image.load('resources/3.bmp').convert()
    img3 = pygame.transform.smoothscale(img3, (SIZE, SIZE))
    img4 = pygame.image.load('resources/4.bmp').convert()
    img4 = pygame.transform.smoothscale(img4, (SIZE, SIZE))
    img5 = pygame.image.load('resources/5.bmp').convert()
    img5 = pygame.transform.smoothscale(img5, (SIZE, SIZE))
    img6 = pygame.image.load('resources/6.bmp').convert()
    img6 = pygame.transform.smoothscale(img6, (SIZE, SIZE))
    img7 = pygame.image.load('resources/7.bmp').convert()
    img7 = pygame.transform.smoothscale(img7, (SIZE, SIZE))
    img8 = pygame.image.load('resources/8.bmp').convert()
    img8 = pygame.transform.smoothscale(img8, (SIZE, SIZE))
    img_blank = pygame.image.load('resources/blank.bmp').convert()
    img_blank = pygame.transform.smoothscale(img_blank, (SIZE, SIZE))
    img_flag = pygame.image.load('resources/flag.bmp').convert()
    img_flag = pygame.transform.smoothscale(img_flag, (SIZE, SIZE))

    img_mine = pygame.image.load('resources/mine.bmp').convert()
    img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
    img_blood = pygame.image.load('resources/blood.bmp').convert()
    img_blood = pygame.transform.smoothscale(img_blood, (SIZE, SIZE))
    img_error = pygame.image.load('resources/error.bmp').convert()
    img_error = pygame.transform.smoothscale(img_error, (SIZE, SIZE))

    img_dict = {
        0: img0,
        1: img1,
        2: img2,
        3: img3,
        4: img4,
        5: img5,
        6: img6,
        7: img7,
        8: img8
    }

    bgcolor = (225, 225, 225)

    block = MineBlock()
    block.getclue()

    reveal_status = RevealStatus.cover

    testA = Agent()
    testA.Solver(block)
    block.read_agent(testA)

    while True:
        screen.fill(bgcolor)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE
                b1, b2, b3 = pygame.mouse.get_pressed()

            if event.type == MOUSEBUTTONUP:
                if b1:
                    command = get_command(x, y)
                    if command == "cover":
                        reveal_status = RevealStatus.cover
                    elif command == "uncover":
                        reveal_status = RevealStatus.uncover
                    elif command == "back":
                        block.add_back()
                    else:
                        block.add_forward()

        block.reveal_agent(testA, reveal_status)

        flag_count = 0
        opened_count = 0

        for row in block.block:
            for mine in row:
                pos = (mine.x * SIZE, mine.y* SIZE)
                if mine.status == BlockStatus.no_mine:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                    opened_count += 1
                elif mine.status == BlockStatus.bomb:
                    screen.blit(img_blood, pos)
                elif mine.status == BlockStatus.flag:
                    screen.blit(img_flag, pos)
                    flag_count += 1
                elif mine.status == BlockStatus.error:
                    screen.blit(img_error, pos)
                elif mine.status == BlockStatus.no_click:
                    screen.blit(img_blank, pos)
                if reveal_status == RevealStatus.uncover and mine.value and mine.status == BlockStatus.no_click:
                    screen.blit(img_mine, pos)

        print_text(screen, font1, (BLOCK_WIDTH + 4) * SIZE + 10, SIZE-10, '%02d' % (MINE_COUNT - flag_count), red)

        screen.blit(img_cover, (cover_x, cover_y))
        screen.blit(img_uncover, (uncover_x, uncover_y))
        screen.blit(img_back, (back_x, back_y))
        screen.blit(img_forward, (forward_x, forward_y))

        pygame.display.update()


if __name__ == '__main__':
    main()
