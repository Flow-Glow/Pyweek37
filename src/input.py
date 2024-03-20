import pyxel


class Input:
    """Input class."""

    LEFT = 1
    RIGHT = 2
    CONFIRM = 3
    CANCEL = 4
    UP = 5
    DOWN = 6

    def __init__(self) -> None:
        self.inputs: list[int] = []

    def update(self) -> list[int]:
        """
        Update the input class.

        :return: the inputs.
        """
        self.inputs.clear()
        if (
                pyxel.btn(pyxel.KEY_LEFT)
                or pyxel.btn(pyxel.KEY_A)
                or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
        ):
            self.inputs.append(self.LEFT)  # 2
        elif (
                pyxel.btn(pyxel.KEY_RIGHT)
                or pyxel.btn(pyxel.KEY_D)
                or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)  # 3
        ):
            self.inputs.append(self.RIGHT)

        if (
                pyxel.btn(pyxel.KEY_UP)
                or pyxel.btn(pyxel.KEY_W)
                or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)
        ):
            self.inputs.append(self.UP)
        elif (
                pyxel.btn(pyxel.KEY_DOWN)
                or pyxel.btn(pyxel.KEY_S)
                or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)
        ):
            self.inputs.append(self.DOWN)

        if (
                pyxel.btn(pyxel.KEY_Z)
                or pyxel.btn(pyxel.KEY_N)
                or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)
        ):
            self.inputs.append(self.CONFIRM)  # 4
        elif (
                pyxel.btn(pyxel.KEY_X)
                or pyxel.btn(pyxel.KEY_M)
                or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)
        ):
            self.inputs.append(self.CANCEL)  # 5

        return self.inputs
