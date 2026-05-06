from typing import ClassVar, Self, TypeAlias, Iterator, overload

Scalar: TypeAlias = int | float
Index: TypeAlias = int | str

class Vec4:

    x: Scalar
    y: Scalar
    z: Scalar
    w: Scalar

    def __init__(self, x: Scalar, y: Scalar, z: Scalar, w: Scalar) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def zero() -> Self:
        return Vec4(0, 0, 0, 0)

    def copy(self) -> Self:
        return Vec4(self.x, self.y, self.z, self.w)
    
    def __add__(self, other: Self | Scalar) -> Self:
        if isinstance(other, Vec4):
            return Vec4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
        if isinstance(other, int | float):
            return Vec4(self.x + other, self.y + other, self.z + other, self.w + other)
        return NotImplemented
    
    def __radd__(self, other: Scalar) -> Self:
        return self.__add__(other)
    
    def __sub__(self, other: Self | Scalar) -> Self:
        if isinstance(other, Vec4):
            return Vec4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)
        if isinstance(other, int | float):
            return Vec4(self.x - other, self.y - other, self.z - other, self.w - other)
        return NotImplemented
    
    def __rsub__(self, other: Scalar) -> Self:
        if isinstance(other, int | float):
            return Vec4(other - self.x, other - self.y, other - self.z, other - self.w)
        return NotImplemented

    @overload
    def __mul__(self, other: Self) -> float: ...
    @overload
    def __mul__(self, other: Scalar) -> Self: ...
    def __mul__(self, other):
        if isinstance(other, Vec4):
            return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w
        if isinstance(other, int | float):
            return Vec4(self.x * other, self.y * other, self.z * other, self.w * other)
        return NotImplemented
    
    def __rmul__(self, other: Scalar) -> Self:
        return self.__mul__(other)
    
    def __truediv__(self, other: Scalar) -> Self:
        if isinstance(other, int | float):
            return Vec4(self.x / other, self.y / other, self.z / other, self.w / other)
        return NotImplemented
    
    def __pos__(self) -> Self:
        return Vec4(self.x, self.y, self.z, self.w)
    
    def __neg__(self) -> Self:
        return Vec4(-self.x, -self.y, -self.z, -self.w)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2) ** 0.5
    
    def __len__(self) -> int:
        return 4
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Vec4) and (self.x, self.y, self.z, self.w) == (other.x, other.y, other.z, other.w)
    
    def __gt__(self, other) -> bool:
        if isinstance(other, Vec4):
            return abs(self) > abs(other)
        if isinstance(other, int | float):
            return abs(self) > other
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        if isinstance(other, Vec4):
            return abs(self) >= abs(other)
        if isinstance(other, int | float):
            return abs(self) >= other
        return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, Vec4):
            return abs(self) < abs(other)
        if isinstance(other, int | float):
            return abs(self) < other
        return NotImplemented
    
    def __le__(self, other) -> bool:
        if isinstance(other, Vec4):
            return abs(self) <= abs(other)
        if isinstance(other, int | float):
            return abs(self) <= other
        return NotImplemented

    def __bool__(self) -> bool:
        return any((self.x, self.y, self.z, self.w))
    
    def __copy__(self) -> Self:
        return Vec4(self.x, self.y, self.z, self.w)

    def __getitem__(self, index: Index) -> Scalar:
        if isinstance(index, int) and 0 <= index < 4:
            return (self.x, self.y, self.z, self.w)[index]
        if isinstance(index, str) and index in ('x', 'y', 'z', 'w'):
            return getattr(self, index)
        raise IndexError('Index out of range')

    def __setitem__(self, index: Index, value: Scalar) -> None:
        if isinstance(index, int) and 0 <= index < 4:
            setattr(self, ('x', 'y', 'z', 'w')[index], value)
            return
        if isinstance(index, str) and index in ('x', 'y', 'z', 'w'):
            setattr(self, index, value)
            return
        raise IndexError('Index out of range')

    def __iter__(self) -> Iterator[Scalar]:
        yield self.x
        yield self.y
        yield self.z
        yield self.w

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z, self.w))

    def __repr__(self) -> str:
        return f'Vec4({self.x}, {self.y}, {self.z}, {self.w})'