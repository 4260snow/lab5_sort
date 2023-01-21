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


def merge(arr, start, mid, end):
    start2 = mid + 1

    if arr[mid] <= arr[start2]:
        return

    while start <= mid and start2 <= end:

        if arr[start] <= arr[start2]:
            start += 1
        else:
            value = arr[start2]
            index = start2

            while index != start:
                arr[index] = arr[index - 1]
                index -= 1

            arr[start] = value

            start += 1
            mid += 1
            start2 += 1


def merge_sort(arr, left, right):
    if left < right:
        m = left + (right - left) // 2

        # Sort first and second halves
        merge_sort(arr, left, m)
        merge_sort(arr, m + 1, right)

        merge(arr, left, m, right)


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.reply("Бот для сортировки массивов\n"
                    "/help, чтобы узнать команды")


@dp.message_handler(commands=['help'])
async def start_command(msg: types.Message):
    await msg.reply("/new_array - получить новый массив из 10 случайных элементов\n"
                    "/my_array - посмотреть состояние массива\n"
                    "/swap idx1 idx2 - поменять местами 2 элемента с индексами idx1 и idx2\n"
                    "/bubble_sort - сортировка пузырьком. Если выполнить без аргументов, то отсортирует имеющийся"
                    " массив. Если передать несколько целых чисел через пробел, то вернёт из отсортированными"
                    "")


@dp.message_handler(commands=['new_array'])
async def start_command(msg: types.Message):
    await msg.reply(str(gen(msg.from_user.id)))


@dp.message_handler(commands=['my_array'])
async def start_command(msg: types.Message):
    if arrays.get(msg.from_user.id, False):
        await msg.reply(str(arrays[msg.from_user.id]))
    else:
        await msg.reply(str(gen(msg.from_user.id)))

@dp.message_handler(commands=['swap'])
async def start_command(msg: types.Message):
    if arrays.get(msg.from_user.id, False):
        tmp = msg.get_args().split()
        if len(tmp) == 2:
            try:
                arrays[msg.from_user.id][int(tmp[0])], arrays[msg.from_user.id][int(tmp[1])] =\
                    arrays[msg.from_user.id][int(tmp[1])], arrays[msg.from_user.id][int(tmp[0])]
                await msg.reply(str(arrays[msg.from_user.id]))
            except:
                await msg.reply("Некорректные аргументы")
        else:
            await msg.reply("Неверное количсество аргументов")
    else:
        await msg.reply(str(gen(msg.from_user.id)))


@dp.message_handler(commands=['merge_sort'])
async def start_command(msg: types.Message):
    if len(msg.get_args().split()):
        arrays[msg.from_user.id] = list(map(int, msg.get_args().split()))
    if not arrays.get(msg.from_user.id, False):
        gen(msg.from_user.id)
    merge_sort(arrays[msg.from_user.id], 0, len(arrays[msg.from_user.id]))
    await msg.reply(str(arrays[msg.from_user.id]))

if __name__ == '__main__':
    executor.start_polling(dp)
