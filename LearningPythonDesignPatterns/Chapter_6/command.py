import os
from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def execute(self):
        """ method for execute command """
        pass

    @abstractmethod
    def undo(self):
        """ method for undo command """
        pass


class LsReceiver:
    @staticmethod
    def show_current_dir():
        cur_dir = '/'
        filenames = []
        for filename in os.listdir(cur_dir):
            if os.path.isfile(filename):
                filenames.append(filename)

        # return filenames
        print('Content of dir: ', os.path.join(*filenames))


class LsCommand(Command):

    def __init__(self, receiver: LsReceiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.show_current_dir()

    def undo(self):
        pass


class TouchReceiver:

    def __init__(self, filename):
        self.filename = filename

    def create_file(self):
        """ python implementation touch Linux """
        with open(self.filename, 'a'):
            os.utime(self.filename, None)

    def delete_file(self):
        os.remove(self.filename)


class TouchCommand(Command):

    def __init__(self, receiver: TouchReceiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.create_file()

    def undo(self):
        self.receiver.delete_file()


class RmReceiver:

    def __init__(self, filename):
        self.filename = filename
        self.backup_name = None

    def delete_file(self):
        self.backup_name = '.' + self.filename

        os.rename(self.filename, self.backup_name)

    def undo(self):
        original_name = self.backup_name[1:]
        os.rename(self.backup_name, original_name)
        self.backup_name = None


class RmCommand(Command):

    def __init__(self, receiver: RmReceiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.delete_file()

    def undo(self):
        self.receiver.undo()


class Invoker:

    def __init__(self, create_file_commands, delete_file_commands):
        self.create_file_commands = create_file_commands
        self.delete_file_commands = delete_file_commands
        self.history = []

    def create_file(self):
        print('create file ...')
        for command in self.create_file_commands:
            command.execute()
            self.history.append(command)

        print('file created \n')

    def delete_file(self):
        print('deleting file')
        for command in self.delete_file_commands:
            command.execute()
            self.history.append(command)
        print('file deleted \n')

    def undo_all(self):
        print('undo all..')
        for command in reversed(self.history):
            command.undo()
        print('undo all finished')


if __name__ == '__main__':
    ls_receiver = LsReceiver()
    ls_command = LsCommand(ls_receiver)

    touch_receiver = TouchReceiver('test_file')
    touch_command = TouchCommand(touch_receiver)

    rm_receiver = RmReceiver('test_file')
    rm_command = RmCommand(rm_receiver)

    create_file_commands = [ls_command, touch_command, ls_command]
    delete_file_commands = [ls_command, rm_command, ls_command]

    invoker = Invoker(create_file_commands, delete_file_commands)

    invoker.create_file()
    invoker.delete_file()
    invoker.undo_all()
