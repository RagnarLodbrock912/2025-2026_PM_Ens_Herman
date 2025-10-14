from math import pi, isclose
from typing import Self

class Angle:
    def __init__(self, angle: float) -> None:
        self.angle = angle

    @classmethod
    def from_degree(cls, degrees: float) -> Self:
        radians = degrees * (pi / 180)
        return cls(radians)
    
    def __eq__(self, other: Self) -> bool:
        return isclose(self.angle % (2*pi), other.angle % (2*pi), abs_tol=1e-9)

    def __repr__(self) -> str:
        return f"Angle({self.angle})"

    def __str__(self) -> str:
        return str(self.angle)

    def __int__(self) -> int:
        return int(self.angle)

    def __float__(self) -> float:
        return float(self.angle)
    
    @property
    def degree(self) -> float:
        return self.angle * (180 / pi)
    
    @degree.setter
    def degree(self, angle: float) -> None:
        self.angle = angle * (pi / 180)

    @property
    def radian(self) -> float:
        return self.angle
    
    @radian.setter
    def radian(self, angle: float) -> None:
        self.angle = angle

    def __add__(self, other: Self | int | float) -> Self:
        if isinstance(other, Angle):
            return Angle(self.angle + other.angle)
        elif isinstance(other, (int, float)):
            return Angle(self.angle + other)
        else:
            return NotImplemented
        
    def __radd__(self, other: int | float) -> Self:
        return self.__add__(other)
        
    def __sub__(self, other: Self | int | float) -> Self:
        if isinstance(other, Angle):
            return Angle(self.angle - other.angle)
        elif isinstance(other, (int, float)):
            return Angle(self.angle - other)
        else:
            return NotImplemented

    def __rsub__(self, other: int | float) -> Self:
        if isinstance(other, (int, float)):
            return Angle(other - self.angle)
        return NotImplemented
    
    def __mul__(self, other: int | float) -> Self:
        return Angle(self.angle * other)
    
    def __rmul__(self, other: int | float) -> Self:
        return self.__mul__(other)
    
    def __truediv__(self, other: int | float) -> Self:
        return Angle(self.angle / other)
    
    def __rtruediv__(self, other: int | float) -> Self:
        return self.__truediv__(other)
    
    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Self) -> bool:
        return self.angle % (2*pi) < other.angle % (2*pi)
    
    def __le__(self, other: Self) -> bool:
        return self.__eq__(other) or self.__lt__(other)
    
    def __gt__(self, other: Self) -> bool:
        return self.angle % (2*pi) > other.angle % (2*pi)
    
    def __ge__(self, other: Self) -> bool:
        return self.__eq__(other) or self.__gt__(other)


class AngleRange:
    def __init__(self, start: float, end: float, include_start: bool = True, include_end: bool = True) -> None:
        self.start = start
        self.end = end
        self.include_start = include_start
        self.include_end = include_end

    @classmethod
    def from_angle(cls, angle: Angle) -> Self:
        return cls(0, angle.radian)
    
    def __abs__(self):
        if self.start <= self.end:
            return self.end - self.start
        else:
            return (2*pi - self.start) + self.end
    
    def __eq__(self, other: Self) -> bool:
        return self.__abs__() == other.__abs__() and \
                Angle(self.end) == Angle(other.end) and \
                Angle(self.start) == Angle(other.start)
    
    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Self) -> bool:
        return self.__abs__() < other.__abs__()
    
    def __le__(self, other: Self) -> bool:
        return self.__abs__() <= other.__abs__()
    
    def __gt__(self, other: Self) -> bool:
        return self.__abs__() > other.__abs__()
    
    def __ge__(self, other: Self) -> bool:
        return self.__abs__() >= other.__abs__()
    
    def __repr__(self):
        start_bracket = "[" if self.include_start else "("
        end_bracket = "]" if self.include_end else ")"
        return f"AngleRange({start_bracket}{self.start}, {self.end}{end_bracket})"
    
    def __contains__(self, other: Self | Angle) -> bool:
        if isinstance(other, AngleRange):
            return self.__contains__(Angle(other.start)) and self.__contains__(Angle(other.end))
        elif isinstance(other, Angle):
            start = self.start % (2*pi)
            end = self.end % (2*pi)
            a = other.radian % (2*pi)
            if start < end:
                start_check = a > start if not self.include_start else a >= start
                end_check = a < end if not self.include_end else a <= end
                return start_check and end_check
            else:
                start_check = a > start if not self.include_start else a >= start
                end_check = a < end if not self.include_end else a <= end
                return start_check or end_check
        else:
            raise NotImplemented
        
    def __add__(self, other: Self) -> list[Self]:
        s1, e1 = self.start % (2*pi), self.end % (2*pi)
        s2, e2 = other.start % (2*pi), other.end % (2*pi)

        parts1 = [(s1, e1)] if s1 <= e1 else [(s1, 2*pi), (0, e1)]
        parts2 = [(s2, e2)] if s2 <= e2 else [(s2, 2*pi), (0, e2)]

        merged = parts1 + parts2
        merged.sort(key=lambda x: x[0])

        result = []
        cur_start, cur_end = merged[0]

        for s, e in merged[1:]:
            if s <= cur_end:
                cur_end = max(cur_end, e)
            else:
                result.append(AngleRange(cur_start, cur_end))
                cur_start, cur_end = s, e

        result.append(AngleRange(cur_start, cur_end))

        return result
    
    def __sub__(self, other: Self) -> list[Self]:
        s1, e1 = self.start % (2*pi), self.end % (2*pi)
        s2, e2 = other.start % (2*pi), other.end % (2*pi)

        parts1 = [(s1, e1)] if s1 <= e1 else [(s1, 2*pi), (0, e1)]
        parts2 = [(s2, e2)] if s2 <= e2 else [(s2, 2*pi), (0, e2)]

        result = []

        for s1, e1 in parts1:
            temp = [(s1, e1)]
            for s2, e2 in parts2:
                new_temp = []
                for ts, te in temp:

                    if te <= s2 or ts >= e2:
                        new_temp.append((ts, te))
                    else:
                        if ts < s2:
                            new_temp.append((ts, s2))
                        if te > e2:
                            new_temp.append((e2, te))
                temp = new_temp
            result.extend([AngleRange(ts, te) for ts, te in temp])

        return result
        
print("---- Создание углов ----")
a1 = Angle(pi/2)
a2 = Angle.from_degree(90)
print(a1, a2, "→ оба должны быть π/2")  

print("\n---- Получение и присваивание ----")
print(a1.radian, "→ π/2")
print(a1.degree, "→ 90")
a1.radian = pi
print(a1.radian, a1.degree, "→ π, 180")
a1.degree = 45
print(a1.radian, a1.degree, "→ π/4, 45")

print("\n---- Преобразования ----")
a = Angle(pi/2)
print(float(a), int(a), str(a), repr(a), "→ float, int, str, repr")

print("\n---- Сравнение углов ----")
a = Angle(0)
b = Angle(2*pi)
c = Angle(pi)
print(a == b, "→ True")
print(a != c, "→ True")
print(a < c, "→ True")
print(c > b, "→ True")
print(a <= b, "→ True")
print(c >= b, "→ True")

print("\n---- Арифметика ----")
a = Angle(pi/2)
b = Angle(pi/4)
print(a + b, "→ 3π/4")
print(a - b, "→ π/4")
print(a + pi/4, "→ 3π/4")
print(pi/4 + a, "→ 3π/4")
print(a - pi/4, "→ π/4")
print(pi/2 - a, "→ 0")
print(a * 2, "→ π")
print(2 * a, "→ π")
print(a / 2, "→ π/4")


print("\n---- Создание диапазонов ----")
r1 = AngleRange(0, pi/2)             # [0, π/2]
r2 = AngleRange(pi/4, 3*pi/4)        # [π/4, 3π/4]
r3 = AngleRange(3*pi/2, pi/2)        # [3π/2, π/2] — через 0
r4 = AngleRange(0, 2*pi)             # полный круг

print("\n---- Длина диапазонов ----")
print(abs(r1), "→ π/2")
print(abs(r3), "→ π")

print("\n---- Проверка включения углов ----")
a1 = Angle(0)
a2 = Angle(pi/4)
a3 = Angle(pi)
a4 = Angle(2*pi)
a5 = Angle(7*pi/4)
print(a1 in r1, "→ True")
print(a2 in r1, "→ True")
print(a3 in r1, "→ False")
print(a4 in r1, "→ True")
print(a5 in r3, "→ True")
print(Angle(-pi/4) in r3, "→ True")
print(Angle(3*pi/2) in r1, "→ False")

print("\n---- Проверка вложенности диапазонов ----")
print(r2 in r1, "→ False")
print(r1 in r4, "→ True")
print(r3 in r4, "→ True")
print(r3 in r1, "→ False")

print("\n---- Сравнение диапазонов ----")
print(r1 < r2, "→ False")    # π/2 < π/2? (по длине) False
print(r1 <= r2, "→ True")   # равно по длине?
print(r3 > r1, "→ True")    # π > π/2
print(r4 >= r3, "→ True")   # 2π >= π

print("\n---- Пограничные случаи ----")
r5 = AngleRange(0, 0)           # нулевой промежуток
print(Angle(0) in r5, "→ True")  # угол на границе
r6 = AngleRange(pi, pi, include_start=False, include_end=False)
print(Angle(pi) in r6, "→ False") # исключаемые границы
