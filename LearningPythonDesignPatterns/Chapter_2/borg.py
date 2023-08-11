
class Borg:
    __shared_state = {}

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance.__dict__ = cls.__shared_state
        return instance

def main():
    original_instance = Borg()
    original_instance.msg = 666

    new_one = Borg()

    print(new_one.msg)
    assert original_instance is not new_one

if __name__ == '__main__':
    main()