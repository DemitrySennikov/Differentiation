# Differentiation
UrFU, FIIT, Python.task-23
Сенников Дмитрий, Хейфец Сергей

## Концепция
Консольное приложение, которое умеет брать частную производную от указанной функции по указанной переменной
$$f'_x (x, y, z)$$
$$f'_y (x, y, z)$$ 
$$f'_z (x, y, z)$$

### Формат ввода
*`main.py` [-h , --help] FUNCTION*

-h, --help - Вызов помощи

FUNCTION - Функция от x, y, z, записанная в кавычках

### Формат вывода
*FUNCTION\** - Ваша функция, записанная без пробелов, с указанием переменных, от которых зависит

*[δ FUNCTION / δ x]*

*[δ FUNCTION / δ y]*

*[δ FUNCTION / δ z]*

Частные производные по тем переменным, от которых выражение зависит

*TYPE_ERROR IND:MISTAKE* - описание ошибки в выражении: синтаксическая, арифметическая и др., с указанием индекса ошибки в выражении FUNCTION\*

### Функционал
* Умеет брать частные производные по функциям от 3 переменных
* В функциях могут быть задействованы стандартные арифметические операции, а также функции синуса, косинуса и натурального логарифма

### Структура файлов
