# Evo
RU:
Requirements:
Python 3.8.(5)
PyGame 2.0.1 (SDL 2.0.14)
Версии остальных модулей не имеют значения

Данная программа демонстрирует симуляцию эволюционных процессов и позволяет рассмотреть их при разных вводных.
Пользователю представляется возможность гибко настроить сцену, на которой будет идти симуляция

Параметры настроики сцены (с указанием строк в программе):
-глобальный радиус видимости (41) - радиус, на котором существа будут видеть друг друга
-начальная активность солнца (42) - начальный коэфицент активности солнца. Чем выше, тем дольше будут жить базовые существа
-порог паники (44) - если уровень жизненной энергии у существа упадёт ниже этого парога, то запустится процесс ускоренного адаптирования
-порог впадения в спячку (45) - если уровень жизненной энергии у существа упадёт ниже этого парога, то оно впадёт в спячку
-количество существ (116) - изначальное число существ на сцене
-ресурс/количество деревьев (117) - изначальный количество деревьев на сцене и ресурс (вместимость) каждого из них

По умолчанию параметрам заданы наиболее подходящие значения для более плавного процесса эволюции

При запуске программы появится окно pygame, в котором будет проводиться симуляция.

Разбор сцены:
-зелёные большие квадраты - деревья
-белые/оранжевые/голубые точки - существа (цвет зависит от способа питания: оранжевые - хищники, голубые - травоядные, белые - с иным способом получения энергии (фотосинтез/геотермальная энергия))

Если у существа кончается жизненная энергия - оно умирает, поэтому они будут всеми доступными способами стараться поддерживать его на достаточном уровне.
Существа могут поедать друг друга, а могут питаться деревьями или получать энергию из света или тепла, выбор за ними.

Симуляция заканчивается, если остаётся только одно существо, которое считается победившим. Его геном и количество прожитых циклов можно увидеть в левом нижнем углу.

По любым вопросам можете писать мне на почту kirillzh470@gmail.com


EN:
Requirements:
Python 3.8.(5)
PyGame 2.0.1 (SDL 2.0.14)
Versions of other modules do not matter

This program demonstrates the simulation of evolutionary processes and allows you to consider them with different inputs.
The user is given the opportunity to flexibly configure the scene on which the simulation will take place.

Scene settings parameters (with indication of lines in the program):
-global visibility radius (41) - the radius at which creatures will see each other
-initial solar activity (42) - initial solar activity coefficient. The higher, the longer the base creatures will live
-panic threshold (44) - if the level of vital energy of the creature falls below this par, then the process of accelerated adaptation will start
- hibernation threshold (45) - if the creature's vital energy level drops below this threshold, it will hibernate
-number of creatures (116) - the initial number of creatures on the stage
-resource/number of trees (117) - the initial number of trees on the scene and the resource (capacity) of each of them

By default, the parameters are set to the most appropriate values for a smoother evolution process.

When you start the program, the pygame window will appear, in which the simulation will be carried out.

Scene analysis:
-green large squares - trees
-white/orange/blue dots - creatures (color depends on the mode of nutrition: orange - predators, blue - herbivores, white - with a different way of obtaining energy (photosynthesis / geothermal energy))

If a creature runs out of life energy, it dies, so they will try to keep it at a sufficient level by all available means.
Creatures can eat each other, or they can eat trees or get energy from light or heat, the choice is theirs.

The simulation ends if there is only one creature left that is considered the winner. Its genome and the number of cycles lived can be seen in the lower left corner.

For any questions, you can write to me at kirillzh470@gmail.com
