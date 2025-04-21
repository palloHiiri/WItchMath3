import math

class IntegralCalculator:
    def __init__(self):
        self.functions = {
            1: ("-x^3-x^2+x+3", lambda x: -x ** 3 - x ** 2 + x + 3),
            2: ("sin(x)", lambda x: math.sin(x)),
            3: ("e^x", lambda x: math.exp(x)),
            4: ("tg(x)*cos(x)+x", lambda x: math.tan(x) * math.cos(x) + x),
        }

        self.methods = {
            1: ("Метод левых прямоугольников", self.left_rectangle),
            2: ("Метод правых прямоугольников", self.right_rectangle),
            3: ("Метод средних прямоугольников", self.midpoint_rectangle),
            4: ("Метод трапеций", self.trapezoidal),
            5: ("Метод Симпсона", self.simpson)
        }

        self.improper_functions = {
            1: ("1/sqrt(x) (разрыв в 0)", lambda x: 1 / math.sqrt(x), 0),
            2: ("1/(1-x)^2 (разрыв в 1)", lambda x: 1 / (1 - x) ** 2, 1),
            3: ("ln(x) (разрыв в 0)", lambda x: math.log(x), 0),
            4: ("1/x (разрыв в 0)", lambda x: 1 / x if x != 0 else float('inf'), 0)
        }

    def calculate_integral(self, func, a, b, method, epsilon, max_iter=1000):
        n = 4
        prev_value = method(func, a, b, n)

        for _ in range(max_iter):
            n *= 2
            current_value = method(func, a, b, n)

            if abs(current_value - prev_value) < epsilon:
                return current_value, n

            prev_value = current_value

        return current_value, n

    def left_rectangle(self, func, a, b, n):
        h = (b - a) / n
        return sum(func(a + i * h) for i in range(n)) * h

    def right_rectangle(self, func, a, b, n):
        h = (b - a) / n
        return sum(func(a + (i + 1) * h) for i in range(n)) * h

    def midpoint_rectangle(self, func, a, b, n):
        h = (b - a) / n
        return sum(func(a + (i + 0.5) * h) for i in range(n)) * h

    def trapezoidal(self, func, a, b, n):
        h = (b - a) / n
        return (func(a) + func(b) + 2 * sum(func(a + i * h) for i in range(1, n))) * h / 2

    def simpson(self, func, a, b, n):
        h = (b - a) / n
        sum_odd = sum(func(a + (2 * i - 1) * h) for i in range(1, n // 2 + 1))
        sum_even = sum(func(a + 2 * i * h) for i in range(1, n // 2))

        return (func(a) + func(b) + 4 * sum_odd + 2 * sum_even) * h / 3

    def check_improper_convergence(self, func_idx, a, b):
        func_info = self.improper_functions[func_idx]
        func = func_info[1]
        break_point = func_info[2]

        if break_point == 0 and a < 0:
            return False
        if break_point == 1 and b > 1:
            return False

        if break_point == a:
            test_value = self.calculate_improper(func, a, a + 0.1, 1e-6, self.trapezoidal)
            if abs(test_value[0]) > 1e6:
                return False
        elif break_point == b:
            test_value = self.calculate_improper(func, b - 0.1, b, 1e-6, self.trapezoidal)
            if abs(test_value[0]) > 1e6:
                return False
        else:
            test1 = self.calculate_improper(func, a, break_point, 1e-6, self.trapezoidal)
            test2 = self.calculate_improper(func, break_point, b, 1e-6, self.trapezoidal)
            if abs(test1[0]) > 1e6 or abs(test2[0]) > 1e6:
                return False

        return True

    def calculate_improper(self, func, a, b, epsilon, method):
        if math.isinf(func(a)) or math.isnan(func(a)):
            return self.calculate_improper_left(func, a, b, epsilon, method)
        elif math.isinf(func(b)) or math.isnan(func(b)):
            return self.calculate_improper_right(func, a, b, epsilon, method)
        else:
            mid = (a + b) / 2
            step = (b - a) / 100
            for x in [a + i * step for i in range(101)]:
                try:
                    val = func(x)
                    if math.isinf(val) or math.isnan(val):
                        mid = x
                        break
                except:
                    mid = x
                    break

            left_part = self.calculate_improper_right(func, a, mid, epsilon / 2, method)
            right_part = self.calculate_improper_left(func, mid, b, epsilon / 2, method)
            return (left_part[0] + right_part[0], left_part[1] + right_part[1])

    def calculate_improper_left(self, func, a, b, epsilon, method):
        delta = (b - a) / 100
        current_a = a + delta
        prev_value = method(func, current_a, b, 4)

        for i in range(1, 20):
            new_a = a + delta / (2 ** i)
            current_value = method(func, new_a, b, 4 * (2 ** i))

            if abs(current_value - prev_value) < epsilon:
                return current_value, 4 * (2 ** i)

            prev_value = current_value

        return prev_value, 4 * (2 ** 19)

    def calculate_improper_right(self, func, a, b, epsilon, method):
        delta = (b - a) / 100
        current_b = b - delta
        prev_value = method(func, a, current_b, 4)

        for i in range(1, 20):
            new_b = b - delta / (2 ** i)
            current_value = method(func, a, new_b, 4 * (2 ** i))

            if abs(current_value - prev_value) < epsilon:
                return current_value, 4 * (2 ** i)

            prev_value = current_value

        return prev_value, 4 * (2 ** 19)

    def run(self):
        print("Добро пожаловать в программу вычисления интегралов!")

        while True:
            print("\nМеню:")
            print("1. Вычислить определенный интеграл")
            print("2. Вычислить несобственный интеграл II рода")
            print("3. Выход")

            choice = input("Выберите действие: ")

            if choice == '1':
                self.calculate_proper_integral()
            elif choice == '2':
                self.calculate_improper_integral()
            elif choice == '3':
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def calculate_proper_integral(self):
        print("\nДоступные функции:")
        for idx, (name, _) in self.functions.items():
            print(f"{idx}. {name}")

        func_idx = int(input("Выберите функцию (1-5): "))
        if func_idx not in self.functions:
            print("Неверный выбор функции.")
            return

        a = float(input("Введите нижний предел интегрирования: "))
        b = float(input("Введите верхний предел интегрирования: "))
        epsilon = float(input("Введите точность вычисления (например, 0.001): "))

        print("\nДоступные методы:")
        for idx, (name, _) in self.methods.items():
            print(f"{idx}. {name}")

        method_idx = int(input("Выберите метод (1-5): "))
        if method_idx not in self.methods:
            print("Неверный выбор метода.")
            return

        method_name, method_func = self.methods[method_idx]
        func = self.functions[func_idx][1]

        try:
            result, n = self.calculate_integral(func, a, b, method_func, epsilon)
            print(f"\nРезультат вычисления интеграла функции {self.functions[func_idx][0]} на интервале [{a}, {b}]:")
            print(f"Метод: {method_name}")
            print(f"Значение интеграла: {result}")
            print(f"Число разбиений интервала: {n}")
            print(f"Достигнутая точность: {epsilon}")
        except Exception as e:
            print(f"Ошибка при вычислении интеграла: {str(e)}")

    def calculate_improper_integral(self):
        print("\nДоступные функции с особенностями:")
        for idx, (name, _, _) in self.improper_functions.items():
            print(f"{idx}. {name}")

        func_idx = int(input("Выберите функцию (1-3): "))
        if func_idx not in self.improper_functions:
            print("Неверный выбор функции.")
            return

        a = float(input("Введите нижний предел интегрирования: "))
        b = float(input("Введите верхний предел интегрирования: "))
        epsilon = float(input("Введите точность вычисления (например, 0.001): "))

        print("\nДоступные методы:")
        for idx, (name, _) in self.methods.items():
            print(f"{idx}. {name}")

        method_idx = int(input("Выберите метод (1-5): "))
        if method_idx not in self.methods:
            print("Неверный выбор метода.")
            return

        method_name, method_func = self.methods[method_idx]
        func = self.improper_functions[func_idx][1]

        if not self.check_improper_convergence(func_idx, a, b):
            print("Интеграл не существует (расходится).")
            return

        try:
            result, n = self.calculate_improper(func, a, b, epsilon, method_func)
            print(
                f"\nРезультат вычисления несобственного интеграла функции {self.improper_functions[func_idx][0]} на интервале [{a}, {b}]:")
            print(f"Метод: {method_name}")
            print(f"Значение интеграла: {result}")
            print(f"Число разбиений интервала: {n}")
            print(f"Достигнутая точность: {epsilon}")
        except Exception as e:
            print(f"Ошибка при вычислении интеграла: {str(e)}")


if __name__ == "__main__":
    calculator = IntegralCalculator()
    calculator.run()