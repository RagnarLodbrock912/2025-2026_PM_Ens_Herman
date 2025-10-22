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
    def __init__(self, start: float | int, end: float | int, include_start: bool = True, include_end: bool = True) -> None:
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
            if abs(other) > abs(self):
                return False

            s1, e1 = self.start, self.end
            s2, e2 = other.start, other.end

            def less_or_equal(a: float | int, b: float | int, include: bool) -> bool:
                return a < b or (include and a == b)

            def greater_or_equal(a: float | int, b: float | int, include: bool) -> bool:
                return a > b or (include and a == b)

            if s1 <= e1:
                if s2 <= e2:
                    start_ok = greater_or_equal(s2, s1, self.include_start and other.include_start)
                    end_ok = less_or_equal(e2, e1, self.include_end and other.include_end)
                    return start_ok and end_ok
                else:
                    a = e1 - s1
                    b = s2 + e2
                    if a == b and a % (2 * pi) == 0 and self.include_start and self.include_end and other.include_end and other.include_start:
                        return True
                    return False
            else:
                if s2 <= e2:
                    in_start = greater_or_equal(s2, s1, self.include_start and other.include_start)
                    in_end = less_or_equal(e2, e1, self.include_end and other.include_end)
                    return in_start or in_end
                else:
                    in_start = greater_or_equal(s2, s1, self.include_start and other.include_start)
                    in_end = less_or_equal(e2, e1, self.include_end and other.include_end)
                    return in_start and in_end

        elif isinstance(other, Angle):
            return self.__contains__(AngleRange.from_angle(other))

        else:
            raise NotImplementedError

        
    def __add__(self, other: Self) -> list[Self]:
        s1, e1 = self.start % (2*pi), self.end % (2*pi)
        s2, e2 = other.start % (2*pi), other.end % (2*pi)

        parts1 = [(s1, e1, self.include_start, self.include_end)] if s1 <= e1 else [
            (s1, 2*pi, self.include_start, True),
            (0, e1, True, self.include_end)
        ]
        parts2 = [(s2, e2, other.include_start, other.include_end)] if s2 <= e2 else [
            (s2, 2*pi, other.include_start, True),
            (0, e2, True, other.include_end)
        ]

        merged = parts1 + parts2
        merged.sort(key=lambda x: x[0])

        result = []
        cur_start, cur_end, cur_start_inc, cur_end_inc = merged[0]

        for s, e, s_inc, e_inc in merged[1:]:
            if s < cur_end or (s == cur_end and (cur_end_inc or s_inc)):
                if e > cur_end or (e == cur_end and e_inc):
                    cur_end = e
                    cur_end_inc = e_inc
            else:
                result.append(AngleRange(cur_start, cur_end, cur_start_inc, cur_end_inc))
                cur_start, cur_end, cur_start_inc, cur_end_inc = s, e, s_inc, e_inc

        result.append(AngleRange(cur_start, cur_end, cur_start_inc, cur_end_inc))
        return result
    
    def __sub__(self, other: Self) -> list[Self]:
        s1, e1 = self.start % (2*pi), self.end % (2*pi)
        s2, e2 = other.start % (2*pi), other.end % (2*pi)

        parts1 = [(s1, e1, self.include_start, self.include_end)] if s1 <= e1 else [
            (s1, 2*pi, self.include_start, True),
            (0, e1, True, self.include_end)
        ]
        parts2 = [(s2, e2, other.include_start, other.include_end)] if s2 <= e2 else [
            (s2, 2*pi, other.include_start, True),
            (0, e2, True, other.include_end)
        ]

        result = []

        for s1, e1, s1_inc, e1_inc in parts1:
            temp = [(s1, e1, s1_inc, e1_inc)]
            for s2, e2, s2_inc, e2_inc in parts2:
                new_temp = []
                for ts, te, ts_inc, te_inc in temp:
                    if te < s2 or (te == s2 and not (te_inc and s2_inc)) or ts > e2 or (ts == e2 and not (ts_inc and e2_inc)):
                        new_temp.append((ts, te, ts_inc, te_inc))
                    else:
                        if ts < s2 or (ts == s2 and ts_inc and not s2_inc):
                            new_temp.append((ts, s2, ts_inc, not s2_inc))
                        if te > e2 or (te == e2 and te_inc and not e2_inc):
                            new_temp.append((e2, te, not e2_inc, te_inc))
                temp = new_temp
            result.extend([AngleRange(ts, te, tsi, tei) for ts, te, tsi, tei in temp])

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
r1 = AngleRange(0, pi/2)
r2 = AngleRange(pi/2, pi)
r3 = AngleRange(3*pi/2, pi/2)
r4 = AngleRange(0, pi*2)
print(r1)
print(r2)
print(r3)

print("\n---- Получение длины диапазона ----")
print(abs(r1), "→ должно быть π/2")
print(abs(r3), "→ должно быть π (от 3π/2 до π/2 через 2π)")

print("\n---- Проверка вхождения углов ----")
a = Angle(pi/4)
b = Angle(3*pi/2)
print(a in r1, "→ True (π/4 ∈ [0, π/2])")
print(b in r4, "→ True (3π/2 ∈ [0, 2π])")
print(b in r3, "→ False (3π/2 ∉ [3π/2, π/2)")

print("\n---- Проверка вхождения диапазонов ----")
r4 = AngleRange(0, pi)
r5 = AngleRange(pi/4, pi/2)
r6 = AngleRange(pi/2, 3*pi/2)
print(r5 in r4, "→ True ([π/4, π/2] внутри [0, π])")
print(r6 in r4, "→ False ([π/2, 3π/2] частично выходит за границы)")
print(r3 in r4, "→ False (wrap-around не внутри обычного диапазона)")
print(r4 in r3, "→ False (обычный диапазон не входит в wrap-around, длина меньше)")

print("\n---- Проверка включающих и исключающих границ ----")
r7 = AngleRange(0, pi, include_start=False, include_end=False)
print(Angle(0) in r7, "→ False (начало исключено)")
print(Angle(pi) in r7, "→ False (конец исключён)")
print(AngleRange(pi/4, pi/2) in r7, "→ True (середина включена)")

print("\n---- Сравнение диапазонов ----")
r8 = AngleRange(0, pi)
r9 = AngleRange(pi, 2*pi)
r10 = AngleRange(0, 2*pi)
print(r8 < r9, "→ True (оба длиной π, но 0<π)")
print(r8 == r9, "→ False (разные границы)")
print(r10 > r8, "→ True (2π > π)")

print("\n---- Сумма диапазонов ----")
r11 = AngleRange(0, pi/2)
r12 = AngleRange(pi/4, pi)
sum_result = r11 + r12
print(sum_result)
print("→ должно получиться один объединённый диапазон [0, π]")

r13 = AngleRange(3*pi/2, 2*pi)
r14 = AngleRange(0, pi/4)
sum_wrap = r13 + r14
print(sum_wrap)

print("\n---- Разность диапазонов ----")
r15 = AngleRange(0, pi)
r16 = AngleRange(pi/4, 3*pi/4)
diff_result = r15 - r16
print(diff_result)
print("→ должно остаться два диапазона: [0, π/4] и [3π/4, π]")

r17 = AngleRange(3*pi/2, pi/2)
r18 = AngleRange(0, pi/4)
diff_wrap = r17 - r18
print(diff_wrap)
print("→ диапазон wrap-around минус маленький — должен остаться разорванный участок")
