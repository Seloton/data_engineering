"""
Given a Tic-Tac-Toe 3x3 board (can be unfinished).
Write a function that checks if the are some winners.
If there is "x" winner, function should return "x wins!"
If there is "o" winner, function should return "o wins!"
If there is a draw, function should return "draw!"
If board is unfinished, function should return "unfinished!"

Example:
    [[-, -, o],
     [-, x, o],
     [x, o, x]]
    Return value should be "unfinished"

    [[-, -, o],
     [-, o, o],
     [x, x, x]]

     Return value should be "x wins!"

"""

from typing import List


def tic_tac_toe_checker(board: List[List]) -> str:
    # Выписываем все строки которые надо проверить
    lines = board + [[*i] for i in zip(*board)] + [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]
    # Ищем победителя у которого все значения в строке уникальны и который не "-"
    win = [i for i in lines if len(set(i)) == 1 and '-' not in i]

    if win:
        return f'{win[0][0]} wins!'
    return "unfinished!" if any('-' in row for row in board) else "draw!"
