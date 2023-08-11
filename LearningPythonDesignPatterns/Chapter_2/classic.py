# Singleton pattern



class Singleton:
    ''' classic singleton class '''

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

class ChildSingleton(Singleton):
    pass

def main():

    # check original instance with new one
    original_instance = Singleton()
    original_instance.msg = 'some message'
    new_instance = Singleton()
    
    print(new_instance.msg)
    assert original_instance is new_instance

    # check class inheridation
    child_instance = ChildSingleton()

    assert child_instance is original_instance
    print(child_instance.msg)

if __name__ == '__main__':
    main()
