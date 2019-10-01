            for x in range(11):
                if self.joystick.get_button_state(x) == 1:
                    self.ids.jbuttons.text = str(x)
                    break