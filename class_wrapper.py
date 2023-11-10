from typing import TypeVar, Type, Any
from copy import deepcopy

T = TypeVar('T')

class _TypeWrapper(type):
	__wrapper_base_type__: Type[T]
	def __getattribute__(cls: Type[T], __name: str) -> Any:
		try:
			return super().__getattribute__(__name)
		except AttributeError:
			pass
		return getattr(cls.__wrapper_base_type__, __name)

class _Wrapper:
	__wrapper_base_type__: Type[T]
	__wrapper_base__: T
	def __new__(cls: Type[T], *args, **kwds) -> T:
		self = super().__new__(cls)
		self.__wrapper_base__ = self.__wrapper_base_type__(*args, **kwds)
		return self
	@classmethod
	def from_instance(cls: Type[T], instance: T) -> T:
		self = super().__new__(cls)
		self.__wrapper_base__ = instance
		return self
	def __getattribute__(self: T, __name: str) -> Any:
		try:
			return super().__getattribute__(__name)
		except AttributeError:
			pass
		return self.__wrapper_base__.__getattribute__(__name)

def ClassWrapper(_type: Type[T]) -> Type[T]:
	type_wrapper = deepcopy(_TypeWrapper)
	type_wrapper.__wrapper_base_type__ = _type
	class Wrapper(_Wrapper, metaclass=type_wrapper):
		__wrapper_base_type__ = _type
		__bases__ = _type, 
		__qualname__ = f"{_Wrapper.__name__}[{_type.__qualname__}]"
	Wrapper.__name__ = _type.__name__
	return Wrapper

def weak_instance(instance: T) -> T:
	wrapper = ClassWrapper(instance.__class__)
	return wrapper.from_instance(instance)

__all__ = [ClassWrapper, weak_instance]
