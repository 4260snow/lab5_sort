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


def merge(alist, start, mid, end):
    left = alist[start:mid]
    right = alist[mid:end]
    k = start
    i = 0
    j = 0
    while start + i < mid and mid + j < end:
        if left[i] <= right[j]:
            alist[k] = left[i]
            i = i + 1
        else:
            alist[k] = right[j]
            j = j + 1
        k = k + 1
    if start + i < mid:
        while k < end:
            alist[k] = left[i]
            i = i + 1
            k = k + 1
    else:
        while k < end:
            alist[k] = right[j]
            j = j + 1
            k = k + 1


def merge_sort(alist, start, end):
    if end - start > 1:
        mid = (start + end)//2
        merge_sort(alist, start, mid)
        merge_sort(alist, mid, end)
        merge(alist, start, mid, end)


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
                    " массив. Если передать несколько целых чисел через пробел, то вернёт из отсортированными"
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
