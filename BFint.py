import sys

class Interpreter(object):
    def __init__(self, code="", commands="><+-.,[]"):
        self.initialize_internals()
        self.code = code
        self.command_mapping = {commands[0] : self.increment_pointer,
                                commands[1] : self.decrement_pointer,
                                commands[2] : self.increment_pointee,
                                commands[3] : self.decrement_pointee,
                                commands[4] : self.print_pointee,
                                commands[5] : self.read_to_pointee,
                                commands[6] : self.loop_start,
                                commands[7] : self.loop_end}
        self.command_chars = {v: k for k, v in self.command_mapping.items()}
        
    def initialize_internals(self):
        self.pointer = 0
        self.memory = {0:0}
        self.ip = 0

    def initialize_pointee(self, pointer):
        if not pointer in self.memory:
            self.memory[pointer] = 0
                    
    def increment_pointer(self):
        self.pointer += 1
        self.initialize_pointee(self.pointer)
        
    def decrement_pointer(self):
        self.pointer -= 1
        self.initialize_pointee(self.pointer)
        
    def increment_pointee(self):
        self.memory[self.pointer] += 1
        
    def decrement_pointee(self):
        self.memory[self.pointer] -= 1
        
    def print_pointee(self):
        sys.stdout.write((chr(self.memory[self.pointer])))
        
    def read_to_pointee(self):
        self.memory[self.pointer] = ord(sys.stdin.read(1))
        
    def loop_start(self):
        if self.memory[self.pointer] == 0:
            new_position = self.code.find(self.command_chars[self.loop_end],self.ip)
            if new_position < 0:
                raise Exception("LoopError: Loop terminator not found.")
            self.ip = new_position
    
    def loop_end(self):
        previous_code_backwards = self.code[self.ip::-1]
        backward_offset = previous_code_backwards.find(self.command_chars[self.loop_start])
        if backward_offset < 0:
                raise Exception("LoopError: Loop start not found.")
        self.ip -= (backward_offset + 1)
        
    def make_single_step(self):
        cmd = self.code[self.ip]
        if cmd in self.command_mapping:
            self.command_mapping[cmd]()
        self.ip += 1

    def runProgram(self):
        while self.ip < len(self.code):
            self.make_single_step()

if __name__ == '__main__':
    hello_world = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
    interpreter = Interpreter(hello_world)
    interpreter.runProgram()    