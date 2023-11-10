from typing import TypeVar, Type, Any

T = TypeVar('T')

class _Wrapper:
	__wrapper_base_type__: Type[T]
	__wrapper_base__: T
	def __new__(cls, *args, **kwds) -> T:
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
	def __setattr__(self: T, __name: str, __value: Any) -> None:
		try:
			return super().__setattr__(__name, __value)
		except AttributeError:
			pass
		return self.__wrapper_base__.__setattr__(__name, __value)
	def __class_getattribute__(cls: Type[T], __name: str) -> Any:
		try:
			return super().__class_getattribute__(__name)
		except AttributeError:
			pass
		return cls.__wrapper_base_type__.__class_getattribute__(__name)
	def __class_setattr__(cls: Type[T], __name: str, __value: Any) -> None:
		try:
			return super().__class_setattr__(__name, __value)
		except AttributeError:
			pass
		return cls.__wrapper_base_type__.__class_setattr__(__name, __value)

def ClassWrapper(_type: Type[T]) -> Type[T]:
	class Wrapper(_Wrapper):
		__wrapper_base_type__ = _type
		__bases__ = _type, 
		__name__ = _type.__name__
		__qualname__ = f"{_Wrapper.__name__}[{_type.__qualname__}]"
	return Wrapper

def weak_instance(instance: T) -> T:
	wrapper = ClassWrapper(instance.__class__)
	return wrapper.from_instance(instance)

__all__ = [ClassWrapper, weak_instance]
