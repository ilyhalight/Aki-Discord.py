import pypresence
import time
# C+P FILE
# Сделал чтобы это работало 24/7 (возможно таймер будет сбрасываться каждые 24 часа)


try: # Ошибка врзникает если нету приложения, нет интернета, не включен дискорд. Этим я и пользуюсь
    status = pypresence.Presence('CLIENT ID') # CLIENT ID
    status.connect() # Проверка на подключение
    connection = True # Это значит что с подключением все ок
    print('Статус запущен')
except Exception:
    connection = False # Это значит что все плохо с подрубом к дс
    print('Все плохо. Проблемы у тебя. Фикси сам')

while connection:
    status.update(
        state = 'Started hosting',
        details = None,
        start = time.time(), # таймкод начала. можно вытащить из модуля time
        end = None, # тиаймкод конца. тоже есть в модуле time. про это я писать не буду. разберетесь сами
        large_image = 'bot2', # Это название картинки которую вы хотите сделать большой
        large_text = 'Aki',
        small_image = 'infinity', # Это название картинки которую вы хотите сделать маленькой
        small_text = 'CPU - i5 4440 | RAM - 16GB | SSD - 240GB ', # Что будет написано при наведение на маленькую картинку
        party_id = None, # айди комнаты с игроками. незнаю что оно делает
        party_size = None, # список с числами. первое - количество игроков в комнате. второе - максималка игроков в комнате.
        join = None, # айди приглашения. тоже незнаю что оно делает
        spectate = None, # айди наблюдательного приглашения. беспонятия что оно делает
        match = 'Host',
        instance = True # не ну тут реально не понимаю
        )
    time.sleep(86400) # Can only update rich presence every 15 seconds


