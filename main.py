import random
import math
import sys
import pygame
import keyboard

# ===================ЦВЕТА==============================================================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (64, 128, 255)
RED = (150, 0, 0)
ORANGE = (255, 147, 28)

# ======================================================================================================================

# ==========ПРОГРАММНЫЕ ВХОДНЫЕ ДАННЫЕ==================================================================================

x = 0
y = 0

fps = 1600

screen_size = (1200, 800)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Evo")
pygame.mouse.set_visible(True)

creations = {}
res = {}
number_of_creations = 0
number_of_res = 0

# ======================================================================================================================

# ==========НАСТРАИВАЕМЫЕ СВОЙСТВА =====================================================================================

global_range_of_visibility = 25  # глобальный радиус видимости
solar_activity = 1  # начальная активность солнца
temp = 1  # начальная температура (НЕ ТРОГАТЬ!)
panic_threshold = 2000  # порог паники
hibernation_threshold = 100  # порог впадения в спячку


# ======================================================================================================================

# ==========ФУНКЦИИ=====================================================================================================

def write(Text, coords, main_color, style='standard', size=20, save=True):  # вывод текста на экран
    if style == 'standard':
        font = pygame.font.SysFont('arial', size)
    elif style == 'bold':
        font = pygame.font.SysFont('arialполужирный', size)
    elif style == 'italic':
        font = pygame.font.SysFont('arialкурсив', size)
    elif style == 'bold-italic':
        font = pygame.font.SysFont('arialполужирныйкурсив', size)
    else:
        sys.exit('Неверные параметры шрифта!')

    text = font.render(str(Text), True, main_color)
    screen.blit(text, (coords[0], coords[1]))


def cr_creation(number=1):  # создание существ
    global creations, number_of_creations
    r = 0
    while r < number:
        x = random.randint(1, 1199)
        y = random.randint(1, 799)
        creations.update({number_of_creations: [[x, y], [x, y], [['M', 2000]], {'eat': [-1, -1],
                                                                                'danger': [-1, -1]}, 25, 1000, 0, 0,
                                                False, 0, 0]})
        number_of_creations += 1
        r += 1


def draw_agent(color, coords, size=2): # отрисовка существ
    pygame.draw.rect(screen, color, [coords[0] - (size / 2), coords[1] - (size / 2), size, size])


def resourses(amount, number=1):  # создание деревьев
    global number_of_res, res
    r = 0
    x1 = random.randint(1, 1199)
    y1 = random.randint(1, 799)
    while r < number:
        if r == 0:
            res.update({number_of_res: [[x1, y1], amount, amount]})
        else:
            xn = random.randint(x1 - 200, x1 + 200)
            yn = random.randint(y1 - 200, y1 + 200)
            if xn > 1198 or xn < 2:
                xn = random.randint(x1 - 200, x1 + 200)
            if yn > 798 or yn < 2:
                yn = random.randint(y1 - 200, y1 + 200)
            res.update({number_of_res: [[xn, yn], amount, amount]})
        number_of_res += 1
        r += 1


def dis(obj1, obj2):  # подсчёт расстояния
    diferend_x = abs(obj1[0] - obj2[0])
    diferend_y = abs(obj1[1] - obj2[1])
    dis = math.sqrt(diferend_x ** 2 + diferend_y ** 2)
    return dis


# =======================================================================================================================

# ========ЭВОЛЮЦИОННЫЕ ВВОДНЫЕ==========================================================================================

cr_creation(15)  # количество существ
resourses(50, 15)  # ресурс/количество деревьев

# ======================================================================================================================

done = False
stop = False
cycles = 0

# =========ГЛАВНЫЙ ЦИКЛ=================================================================================================

while not done and (len(creations.keys()) > 0):

    screen.fill(BLACK)

    # =====ФУНКЦИИ ВЫХОДА===============================================================================================

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            restart_on_exit = False

    while keyboard.is_pressed('ESC'):
        if keyboard.is_pressed('ESC'):
            pygame.time.delay(500)
            if keyboard.is_pressed('ESC'):
                pygame.time.delay(500)
                if keyboard.is_pressed('ESC'):
                    pygame.time.delay(500)
                    if keyboard.is_pressed('ESC'):
                        pygame.time.delay(500)
                        done = True
                        break
                    else:
                        break
                else:
                    break
            else:
                break
        else:
            break

    # ==================================================================================================================

    # =========УСЛОВИЕ ПОБЕДЫ===========================================================================================

    if len(creations.keys()) == 1:
        for i in range(max(creations.keys()) + 1):
            # print(i)
            try:
                current_cr = creations[i]
            except:
                continue
            if current_cr[10] == 1:
                draw_agent(ORANGE, [current_cr[0][0], current_cr[0][1]], 10)
            elif current_cr[10] == 2:
                draw_agent(LIGHT_BLUE, [current_cr[0][0], current_cr[0][1]], 10)
            else:
                draw_agent(WHITE, [current_cr[0][0], current_cr[0][1]], 10)
            write('WINNER!!!', [400, 400], RED, size=100)
            write(str(current_cr[2]), [0, 700], WHITE, size=20)
            write(str('Cycle: ' + str(cycles)), [0, 750], WHITE, size=20)
            pygame.draw.circle(screen, RED, current_cr[0], 50, 10)
            pygame.display.flip()
            # print('stop')

        continue

    # ==================================================================================================================

    # ========ИЗМЕНЕНИЕ АКТИВНОСТИ СОЛНЦА И ТЕМПЕРАТУРЫ ================================================================

    if cycles > 1000:
        if cycles % 250 == 0 and solar_activity > 0:
            solar_activity -= 0.01

    if cycles < 200000:
        temp = math.cos(0.0001 * cycles)
    else:
        temp = -1

    # ==================================================================================================================

    # =====ГЛАВНЫЙ ПОДЦИКЛ (манипуляции с существами)===================================================================

    for i in range(max(creations.keys()) + 1):
        try:
            current_cr = creations[i]
        except:
            continue

        energy = False
        current_energy = current_cr[6]
        current_cr[6] = 0
        new_energy = 0

        # ==============УСЛОВИЕ РАЗМНОЖЕНИЯ=============================================================================

        if current_cr[6] >= 10000 and current_cr[5] > 50:
            cr_creation(1)

        # ==============================================================================================================

        # ==============УСЛОВИЕ РЕГЕНЕРАЦИИ=============================================================================

        if current_cr[6] >= 1000 and current_cr[5] < 100:
            current_cr[5] += 1

        # ==============================================================================================================

        # ==============ЗАПОМИНАНИЕ ПОЛОЖЕНИЯ ЕДЫ (WIP)=================================================================

        for h in range(len(res.keys())):
            c_res = res[h]
            if dis(current_cr[0], c_res[0]) < current_cr[4] and c_res[1] > 0:
                if dis(c_res[0], current_cr[3]['eat']) > 30:
                    if random.random() < 0.5:
                        current_cr[3]['eat'] = c_res[0]

        # ==============================================================================================================

        # ==============МАНИПУЛЯЦИИ С ГЕНОМОМ===========================================================================

        for c in range(len(current_cr[2])):
            cell = current_cr[2][c]
            if cell[1] > 0:

                # ===========РАСХОД ЭНЕРГИИ В СПЯЧКЕ====================================================================

                if current_cr[8]:
                    if current_cr[9] % 500 == 0:
                        cell[1] -= 1

                # ======================================================================================================

                energy = True

                # ============================ПЕРЕХОД===================================================================

                if current_cr[0] != current_cr[1] and not current_cr[8]:
                    a = random.randint(0, 1)
                    if a == 0:
                        if current_cr[0][0] > current_cr[1][0] or (
                                random.uniform(0, 10) > 8 and dis(current_cr[0], current_cr[1]) > current_cr[4]):

                            current_cr[0][0] -= 1
                        elif current_cr[0][0] < current_cr[1][0] or (
                                random.randint(0, 10) > 8 and dis(current_cr[0], current_cr[1]) > current_cr[4]):

                            current_cr[0][0] += 1
                    else:
                        if current_cr[0][1] > current_cr[1][1] or (
                                random.randint(0, 10) > 8 and dis(current_cr[0], current_cr[1]) > current_cr[4]):

                            current_cr[0][1] -= 1
                        elif current_cr[0][1] < current_cr[1][1] or (
                                random.randint(0, 10) > 8 and dis(current_cr[0], current_cr[1]) > current_cr[4]):

                            current_cr[0][1] += 1
                    cell[1] -= 1

                # ======================================================================================================

                new_energy += cell[1]

            # ==========УСЛОВИЯ ГЕНОМА==================================================================================

            if cell[0] == 'F':  # ген фотосинтеза
                cell[1] = cell[1] + int(4 * solar_activity)

            elif cell[0] == 'G' and temp > 0:  # ген термальной генерации энергии
                cell[1] = cell[1] + int(4 * temp)

            elif cell[0] == 'L':  # ген биолюминесценции (WIP)
                for cc in range(len(current_cr[2])):
                    cl = current_cr[2][cc]
                    if cl[1] >= 2:
                        current_cr[4] = global_range_of_visibility + 20
                        cl[1] -= 2

            elif cell[0] == 'H':  # ген желудка
                P = False
                T = False
                for cc in range(len(current_cr[2])):
                    cl = current_cr[2][cc]
                    if cl[0] == 'T':
                        T = True
                    elif cl[0] == 'P':
                        P = True

                # ==========УСЛОВИЕ ПЛОТОЯДНОСТИ========================================================================

                if cell[2] < 2 and P:
                    for ii in range(max(creations.keys()) + 1):
                        try:
                            any_ag = creations[ii]
                            if any_ag == current_cr:
                                continue
                            if dis(current_cr[0], any_ag[0]) < 15:
                                any_ag[5] -= 10
                                cell[2] += 1
                        except:
                            continue

                # ======================================================================================================

                # ===========УСЛОВИЕ ТРАВОЯДНОСТИ=======================================================================

                if cell[2] < 2 and T:
                    for h in range(len(res.keys())):
                        c_res = res[h]
                        if dis(current_cr[0], c_res[0]) < current_cr[4]:
                            c_res[1] -= 1
                            cell[2] += 1

                # ======================================================================================================

                # ==========ПЕРЕВАРИВАНИЕ ПИЩИ==========================================================================

                if cell[2] > 0 and cell[1] < 9:
                    cell[1] += random.randint(2, 3)
                    cell[2] -= 1

                # ======================================================================================================

            current_cr[6] += cell[1]

        current_cr[7] = current_energy - new_energy - 2  # дельта энергии

        if not energy:  # если нет энергии - отнимаем хп
            current_cr[5] -= 1

        # ==========ИДЕНТИФИКАЦИЯ СУЩЕСТВ===============================================================================

        for cc in range(len(current_cr[2])):
            cl = current_cr[2][cc]
            # print(cl)
            if cl[0] == 'T':
                current_cr[10] = 1
            elif cl[0] == 'P':
                current_cr[10] = 2

        # ==============================================================================================================

        # =========ПАНИКА ПРИ НЕХВАТКА ЭНЕРГИИ==========================================================================

        if current_cr[6] < panic_threshold and current_cr[7] < 0:
            solar_power = 4 * solar_activity * random.random()
            termal_power = 5 * temp * random.random()
            if len(current_cr[2]) < 10:
                if (current_cr[7] + solar_power) > 0:
                    current_cr[2].append(['F', 0])
                elif (current_cr[7] + termal_power) > 0:
                    current_cr[2].append(['G', 0])
                else:
                    dist_r = []
                    dist_c = []
                    T = False
                    P = False
                    H = False
                    for h in range(len(res.keys())):
                        c_res = res[h]
                        dist_r.append(dis(current_cr[0], c_res[0]))
                    for ii in range(max(creations.keys()) + 1):
                        try:
                            any_ag = creations[ii]
                            if any_ag == current_cr:
                                continue
                        except:
                            continue
                        dist_c.append(dis(current_cr[0], any_ag[0]))
                    for cc in range(len(current_cr[2])):
                        cl = current_cr[2][cc]
                        if cl[0] == 'T':
                            T = True
                        elif cl[0] == 'P':
                            P = True
                        elif cl[0] == 'H':
                            H = True
                    if (min(dist_c) < min(dist_r)) and not P:
                        current_cr[2].append(['P', 0])
                        if len(current_cr[2]) < 10:
                            if not H:
                                current_cr[2].append(['H', 0, 0])

                    if (min(dist_c) > min(dist_r)) and P:
                        current_cr[2].append(['T', 0])
                        if len(current_cr[2]) < 10:
                            if not H:
                                current_cr[2].append(['H', 0, 0])

                    if (min(dist_c) < min(dist_r)) and T:
                        current_cr[2].append(['P', 0])
                        if len(current_cr[2]) < 10:
                            if not H:
                                current_cr[2].append(['H', 0, 0])

                    if (min(dist_c) > min(dist_r)) and not T:
                        current_cr[2].append(['T', 0])
                        if len(current_cr[2]) < 10:
                            if not H:
                                current_cr[2].append(['H', 0, 0])

        # ==============================================================================================================

        # ========СПЯЧКА/СТАЗИС=========================================================================================

        if (current_cr[6] < hibernation_threshold) and current_cr[7] < 0:
            current_cr[8] = True
            current_cr[9] += 1
        else:
            current_cr[8] = False

        # ==============================================================================================================

        # ========УБЕГАНИЕ ОТ ХИЩНИКОВ==================================================================================

        for ii in range(max(creations.keys()) + 1):
            try:
                any_ag = creations[ii]
                if any_ag == current_cr:
                    continue
            except:
                continue

            if dis(current_cr[0], any_ag[0]) < current_cr[4]:
                for cc in range(len(any_ag[2])):
                    cl = any_ag[2][cc]
                    if cl[0] == 'P':
                        try:
                            if any_ag[0][0] <= current_cr[0][0]:
                                alpha = math.acos((abs(any_ag[0][0] - current_cr[0][0])) / (
                                        math.sqrt(abs(any_ag[0][0] - current_cr[0][0]) ** 2) + (
                                        abs(any_ag[0][1] - current_cr[0][1]) ** 2)))
                            else:
                                alpha = math.acos((abs(any_ag[0][0] - current_cr[0][0])) / (
                                        math.sqrt(abs(any_ag[0][0] - current_cr[0][0]) ** 2) + (
                                        abs(any_ag[0][1] - current_cr[0][1]) ** 2))) + (math.pi / 2)

                            if ((current_cr[0][0] + current_cr[4] * math.cos(alpha)) > 1199) or (
                                    (current_cr[0][0] + current_cr[4] * math.cos(alpha)) < 1) or (
                                    (current_cr[0][1] + current_cr[4] * math.cos(alpha)) > 799) or (
                                    (current_cr[0][1] + current_cr[4] * math.cos(alpha)) < 1):
                                current_cr[1] = [
                                    int(current_cr[0][0] + current_cr[4] * math.cos(alpha + (math.pi / 2))),
                                    int(current_cr[0][1] + current_cr[4] * math.sin(alpha + (math.pi / 2)))]

                            current_cr[1] = [int(current_cr[0][0] + current_cr[4] * math.cos(alpha)),
                                             int(current_cr[0][1] + current_cr[4] * math.sin(alpha))]
                        except:
                            pass

        # ==============================================================================================================

        # =========ВЫБОР ЦЕЛИ/ПРЕСЛЕДОВАНИЕ=============================================================================

        if current_cr[0] == current_cr[1]:
            Tar = False
            Pl = False
            for ii in range(max(creations.keys()) + 1):
                try:
                    any_ag = creations[ii]
                    if any_ag == current_cr:
                        continue
                except:
                    continue
                for cc in range(len(current_cr[2])):
                    cl = current_cr[2][cc]
                    if cl[0] == 'P':
                        Pl = True

                if dis(current_cr[0], any_ag[0]) < current_cr[4] and Pl:
                    current_cr[1] = any_ag[0]
                    Tar = True
            if not Tar:
                current_cr[1] = [random.randint(2, 1198), random.randint(2, 798)]

        # ==============================================================================================================

        # =======УСЛОВИЕ СМЕРТИ=========================================================================================

        if current_cr[5] <= 0:
            print(str(cycles) + ' ' + str(current_cr))
            creations.pop(i)

        # ==============================================================================================================

        # ===========================ОТРИСОВКА СУЩЕСТВ==================================================================

        if current_cr[10] == 1:
            draw_agent(ORANGE, [current_cr[0][0], current_cr[0][1]], 10)
        elif current_cr[10] == 2:
            draw_agent(LIGHT_BLUE, [current_cr[0][0], current_cr[0][1]], 10)
        else:
            draw_agent(WHITE, [current_cr[0][0], current_cr[0][1]], 10)

        # ==============================================================================================================

    # =========ОТРИСОВКА ДЕРЕВЬЕВ=======================================================================================

    for r in range(len(res.keys())):
        cur_res = res[r]
        if cur_res[1] > 0:
            pygame.draw.rect(screen, (0, int(cur_res[1] / (cur_res[2] / 255)), 0),
                             [cur_res[0][0] - 7, cur_res[0][1] - 7, 14, 14])

    # ==================================================================================================================

    # =========УПРАВЛЕНИЕ СИМУЛЯЦИЕЙ (WIP)==============================================================================

    if keyboard.is_pressed('Space'):  # пробел для остановки симуляции
        stop = True
    while stop:
        if keyboard.is_pressed('Return'):  # enter для возобновления
            stop = False
        if keyboard.is_pressed('right'):  # стрелка в право для по кадрового режима (при паузе)
            break

    if keyboard.is_pressed('up'):  # стрелка вверх для увеличения скорости симуляции
        fps += 5
    elif keyboard.is_pressed('down') and fps > 6:  # стрелка вниз для уменьшения скорости симуляции
        fps -= 5

    # ==================================================================================================================

    # =============ОБНОВЛЕНИЕ КАДРА=====================================================================================

    pygame.display.flip()

    clock.tick(fps)
    cycles += 1

    # ==================================================================================================================
