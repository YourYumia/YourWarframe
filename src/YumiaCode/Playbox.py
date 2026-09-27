def sumArr(array:list[int|float], o:int=0) -> int|float:
    if not array:
        return o
    if len(array) == 1:
        return o + array[0]
    return sumArr(array[2:], o+array[0]+array[1])

def indexOfLargest(array:list[int|float], prev:int|float=0, i:int=0) -> int:
    if i < len(array) and i+1 < len(array):
        tailLarge = indexOfLargest(array, array[i] if array[i] >= prev else prev, i+1)
        return i if array[i] >= array[tailLarge] else tailLarge
    if i+1 == len(array):
        return i if array[i] >= prev else i-1
    return i



def returnGreater(a:int|float|list[int|float], b:int|float|list[int|float]) -> int|float|list[int|float]|None:
    if a == b: return None
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if a == b: return None
        return a if a > b else b
    if isinstance(a, (int, float)):
        if sumArr(a) == b: return None
        return a if sumArr(a) > b else b
    if isinstance(b, (int, float)):
        if a == sumArr(b): return None
        return a if a > sumArr(b) else b
    return a if sumArr(a) > sumArr(b) else b



def checkIndex(array:list[any], target:int, index:int) -> bool:
    if index < len(array):
        if index+1 < len(array):
            return index+1 if index+1 == target else checkIndex(array, target, index+1)
        return True if index == target else False



def filter(array:list[any], predicate:function, index:int=0) -> list[any]:
    if index < len(array):
        filtered = filter(array, predicate, index+1) # filter later results immediately

        ele = array[index]
        if predicate(ele):
            return [ele]+filtered # return all filtered elements in new array

        return filtered # if current element does not match filter
    return [] # when no elements matched filter



def map(array:list[any], transform:function, index:int=0) -> list[any]:
    if index < len(array):
        elements = map(array, transform, index+1) # map later elements immediately

        ele = array[index]
        transformed = transform(ele)

        return [transformed]+elements # return transformed array
    return [] # out of bounds index or empty array given ???



def take(array:list[any], count:int, index:int=0) -> list[any]:
    if (index < len(array) and index < count):
        elements = take(array, count, index+1)# take later elements first

        ele = array[index]
        return [ele]+elements # return taken elements
    return [] # out of bounds index or empty array given ???