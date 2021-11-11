# https://stackoverflow.com/questions/510357/how-to-read-a-single-character-from-the-user/48136131#48136131

import sys

if sys.platform == 'win32':
    import msvcrt
    def __gen_ch_getter(echo):
        def __fun():
            ch = ''
            if echo:
                ch = msvcrt.getche()
            else:
                ch = msvcrt.getch()
            if ch == b'\x03':
                raise KeyboardInterrupt
            return ch.decode('ascii')
        return __fun
    getch = __gen_ch_getter(False)
    getche = __gen_ch_getter(True)

else:
    import termios
    def __gen_ch_getter(echo):
        def __fun():
            fd = sys.stdin.fileno()
            oldattr = termios.tcgetattr(fd)
            newattr = oldattr[:]
            try:
                if echo:
                    # disable ctrl character printing, otherwise, backspace will be printed as "^?"
                    lflag = ~(termios.ICANON | termios.ECHOCTL)
                else:
                    lflag = ~(termios.ICANON | termios.ECHO)
                newattr[3] &= lflag
                termios.tcsetattr(fd, termios.TCSADRAIN, newattr)
                ch = sys.stdin.read(1)
                if echo and ord(ch) == 127: # backspace
                    # emulate backspace erasing
                    # https://stackoverflow.com/a/47962872/404271
                    sys.stdout.write('\b \b')
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, oldattr)
            return ch
        return __fun
    getch = __gen_ch_getter(False)
    getche = __gen_ch_getter(True)
