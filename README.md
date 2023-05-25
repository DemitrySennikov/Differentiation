# Differentiation
UrFU, FIIT, Python.task-23
Сенников Дмитрий, Хейфец Сергей

### Синтаксис
Запись выражений для вычисления производной основана на LaTeX с некоторыми отличиями для более удобной проверки. 
* Выражение записывается без символов '$' и иных указателей на границах выражения
* В произведении функций общий вещественных коэффициент записывается слева 
* В выражении разрешено использовать фигурные скобки не только для указаний аргументов функций, но и в качестве круглых скобок
* Как и в LaTeX, возведение в степень производится либо в первый символ после '^', либо в выражение в фигурных скобках сразу после '^'
* Ввиду редкого использования символа '/' для деления, его использование исключено. Для записи дроби используйте "\frac{числитель}{знаменатель}"
* Допустимо использование "\lg" для $\log_10$, "\ln" для $\log_e$

* Формат записи тригонометрической (в т.ч. обратных) функции (на примере $\sin(5x+2)$):
    * "\sin{5x+2}"
* Формат записи логарифма (например, $\log_6{12x^2}$):
    * "\log{6}{12x^2}"
* Формат записи выражения под корнем (например, $\sqrt[4]{x+5}$):
    * "\sqrt{4}{x+5}"
* При возведении результата функции в степень, последняя указывается сразу после названия функции (например, для $(\arctan(4\pi x))^3$):
    * "\arctan^{3}{4\pix}"



