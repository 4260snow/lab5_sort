from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from random import randint
from config import TOKEN

arrays = dict()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def gen(user_id):
    arr = list([randint(0, 10) for i in range(10)])
    arrays[user_id] = arr
    return arr


def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    LEFT = [0] * n1
    RIGHT = [0] * n2

    for i in range(0, n1):
        LEFT[i] = arr[l + i]

    for j in range(0, n2):
        RIGHT[j] = arr[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if LEFT[i] <= RIGHT[j]:
            arr[k] = LEFT[i]
            i += 1
        else:
            arr[k] = RIGHT[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = LEFT[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = RIGHT[j]
        j += 1
        k += 1


def merge_sort(arr, left, right):
    if left < right:
        m = left + (right - left) // 2

        merge_sort(arr, left, m)
        merge_sort(arr, m + 1, right)
        merge(arr, left, m, right)


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.answer("Бот для сортировки массивов\n"
                    "/help, чтобы узнать команды")


@dp.message_handler(commands=['help'])
async def start_command(msg: types.Message):
    await msg.answer("/new_array - получить новый массив из 10 случайных элементов\n"
                    "/my_array - посмотреть состояние массива\n"
                    "/swap idx1 idx2 - поменять местами 2 элемента с индексами idx1 и idx2\n"
                    "/merge_sort - сортировка слиянием. Если выполнить без аргументов, то отсортирует имеющийся"
                    " массив. Если передать несколько целых чисел через пробел, то вернёт их отсортированными"
                    "")


@dp.message_handler(commands=['new_array'])
async def start_command(msg: types.Message):
    await msg.answer(str(gen(msg.from_user.id)))


@dp.message_handler(commands=['my_array'])
async def start_command(msg: types.Message):
    if arrays.get(msg.from_user.id, False):
        await msg.answer(str(arrays[msg.from_user.id]))
    else:
        await msg.answer(str(gen(msg.from_user.id)))

@dp.message_handler(commands=['swap'])
async def start_command(msg: types.Message):
    if arrays.get(msg.from_user.id, False):
        tmp = msg.get_args().split()
        if len(tmp) == 2:
            try:
                arrays[msg.from_user.id][int(tmp[0])], arrays[msg.from_user.id][int(tmp[1])] =\
                    arrays[msg.from_user.id][int(tmp[1])], arrays[msg.from_user.id][int(tmp[0])]
                await msg.answer(str(arrays[msg.from_user.id]))
            except:
                await msg.answer("Некорректные аргументы")
        else:
            await msg.answer("Неверное количсество аргументов")
    else:
        await msg.answer(str(gen(msg.from_user.id)))


@dp.message_handler(commands=['merge_sort'])
async def start_command(msg: types.Message):
    if len(msg.get_args().split()):
        arrays[msg.from_user.id] = list(map(int, msg.get_args().split()))
    if not arrays.get(msg.from_user.id, False):
        gen(msg.from_user.id)
    merge_sort(arrays[msg.from_user.id], 0, len(arrays[msg.from_user.id]))
    await msg.answer(str(arrays[msg.from_user.id]))

if __name__ == '__main__':
    executor.start_polling(dp)
