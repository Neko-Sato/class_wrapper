from typing import *

T = TypeVar('T')

class _Wrapper:
	__wrapper_base__: T
	def __init__(self: T, base: T) -> None:
		self.__wrapper_base__ = base
	def __getattribute__(self: T, __name: str) -> Any:
		if __name != "__wrapper_base__":
			try:
				return self.__wrapper_base__.__getattribute__(__name)
			except AttributeError:
				pass
		return super().__getattribute__(__name)
	def __setattr__(self: T, __name: str, __value: Any) -> None:
		if __name != "__wrapper_base__":
			try:
				return self.__wrapper_base__.__setattr__(__name, __value)
			except AttributeError:
				pass
		return super().__setattr__(__name, __value)

def ClassWrapper(_type: Type[T]) -> Type[T]:
	##
	class Wrapper(_Wrapper):
		__bases__ = _type, 
		__name__ = _type.__name__
		__qualname__ = f"Wrapper({_type.__qualname__})"
		def __init__(self: T, *args, **kwds) -> None:
			super().__init__(_type(*args, **kwds))
	##
	return Wrapper

__all__ = [ClassWrapper]
