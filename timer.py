"""Routine for studying

This should generally run as a standalone routine
and would probably need to be modified a good bit
to be of much use for anything but the usecase for which
it was designed.

class Timer: The main routine, runs a set of four timers
             in a tkinter app.  Subclasses a ttk.Frame.

def main: Just a dispach function that sets the tkinter
          app in Timer running.

License: You're free to use this program.  This was
basically a one day hack, because I really wanted it. So
the best use case would be someone wanting to play with
a bit of TK code.

The following are possible todos:

TODO:
    - The timer is a deeply recursive function, which is
      going to create a deep stack in memory, I presume.
      Make it work on repeated calls would be better.
    - Each line of the timer gui is a bunch of  repeated
      code, which can be built in a more DRY way.
"""

import tkinter as tk
import tkinter.ttk as ttk

import tkSnack


class Timer(ttk.Frame):
    """Timer routine

    This sets for timers for my study routine which
    follows the following:
        - Clear my mind, think about when I expect to learn
          in the next section
        - Study
        - Review what I've just covered
        - Relax - take a break.

    Each timer ends with a gong sound, followed
    by the next timer automatically being called.

    This set of timers are very specific to how
    I like to study when I've got big blocks of time.
    The idea is to make sure that big blocks of time
    are used well.

    Designed during the Covid-19 pandemic when
    I wanted to make sure my studying was effective.
    """

    def __init__(self, master):
        """
        Run a set of timers concurrently
        - clear_mind (default 5 minutes)
        - study (default 30 minutes)
        - review (default 5 minutes)
        - break (15 minutes)
        """
        super().__init__(master)
        self.master = master

        # tkSnack used to play sound
        tkSnack.initializeSnack(self.master)
        self.snd = tkSnack.Sound()
        self.snd.read("media/gong.wav")

        self.minutes = self.seconds = 0
        self.minute_vals = [5, 30, 5, 15]

        self.clear_mind_label_text = tk.StringVar()
        self.study_label_text = tk.StringVar()
        self.review_label_text = tk.StringVar()
        self.relax_label_text = tk.StringVar()
        self.clear_mind_input_value = tk.StringVar()
        self.study_input_value = tk.StringVar()
        self.review_input_value = tk.StringVar()
        self.relax_input_value = tk.StringVar()
        self.error_message = tk.StringVar()
        self.item = [
            self.clear_mind_label_text,
            self.study_label_text,
            self.review_label_text,
            self.relax_label_text,
        ]

        self.current_row = 0
        self.line_label = 0
        self.entry_colomn = 1
        self.set_entry_column = 2
        self.time_column = 3

        self.initUI()

    def dispatch(self, input, output):
        """Sets the clock values when user updates them"""
        try:
            val = int(input.get())
            self.minute_vals[self.item.index(output)] = val
            self.minutes = val
            clock = f"{self.minutes:02}:00"
            output.set(clock)
            self.error_message.set("")
        except ValueError:
            self.error_message.set("The value you gave isn't valid")

    def set_user_input(self, context):
        exec(f"self.dispatch(self.{context}_input_value, self.{context}_label_text)")

    def update_clock(self, label_text):
        """Sets the values for each timer

        The timer takes the form MM:SS
        The user can only set minutes, but minutes
        are included here for the timer routine.
        """
        clock = f"{self.minutes:02}:{self.seconds:02}"
        label_text.set(clock)

    def initUI(self):
        """Build the gui"""
        self.master.geometry("+100+100")
        self.master.title("Timer")

        # --------- Top intro line -------
        intro_text = "Timer, clear your mind, study, review, relax"
        intro = ttk.Label(self, text=intro_text)
        intro.grid(row=self.current_row, column=0, columnspan=4, pady=20)
        self.current_row += 1
        divide = ttk.Separator(self, orient=tk.HORIZONTAL)
        divide.grid(row=self.current_row, sticky="ew", columnspan=4)

        # --------- Clear mind line line -------
        self.current_row += 1
        clear_mind_instruction = ttk.Label(self,
                                           text="Clear your mind timer")
        clear_mind_instruction.grid(row=self.current_row,
                                    column=self.line_label,
                                    padx=5, pady=5)
        clear_mind_amount = ttk.Entry(self, justify=tk.RIGHT, width=9,
                                      textvariable=self.clear_mind_input_value)
        clear_mind_amount.grid(row=self.current_row,
                               column=self.entry_colomn,
                               padx=5, pady=9)
        set_clear_mind_amount = ttk.Button(self, text="SET")
        set_clear_mind_amount.configure(command=lambda: self.set_user_input("clear_mind"))
        set_clear_mind_amount.grid(row=self.current_row,
                                   column=self.set_entry_column,
                                   padx=5, pady=5)
        clear_mind_clock = ttk.Label(self,
                                     textvariable=self.clear_mind_label_text)
        clear_mind_clock.grid(row=self.current_row,
                              column=self.time_column,
                              padx=5, pady=5)
        self.current_row += 1
        divide = ttk.Separator(self, orient=tk.HORIZONTAL)
        divide.grid(row=self.current_row, sticky="ew", columnspan=4)

        # --------- Study line -------
        self.current_row += 1
        study_instruction = ttk.Label(self,
                                      text="Study mind timer")
        study_instruction.grid(row=self.current_row,
                               column=self.line_label,
                               padx=5, pady=5)
        study_amount = ttk.Entry(self, justify=tk.RIGHT, width=9,
                                 textvariable=self.study_input_value)
        study_amount.grid(row=self.current_row,
                          column=self.entry_colomn,
                          padx=5, pady=9)
        set_study_amount = ttk.Button(self, text="SET")
        set_study_amount.configure(command=lambda: self.set_user_input("study"))
        set_study_amount.grid(row=self.current_row,
                              column=self.set_entry_column,
                              padx=5, pady=5)
        study_clock = ttk.Label(self,
                                textvariable=self.study_label_text)
        study_clock.grid(row=self.current_row,
                         column=self.time_column,
                         padx=5, pady=5)
        self.current_row += 1
        divide = ttk.Separator(self, orient=tk.HORIZONTAL)
        divide.grid(row=self.current_row, sticky="ew", columnspan=4)

        # --------- Review line -------
        self.current_row += 1
        review_instruction = ttk.Label(self,
                                       text="Review mind timer")
        review_instruction.grid(row=self.current_row,
                                column=self.line_label,
                                padx=5, pady=5)
        review_amount = ttk.Entry(self, justify=tk.RIGHT, width=9,
                                  textvariable=self.review_input_value)
        review_amount.grid(row=self.current_row,
                           column=self.entry_colomn,
                           padx=5, pady=9)
        set_review_amount = ttk.Button(self, text="SET")
        set_review_amount.configure(command=lambda: self.set_user_input("review"))
        set_review_amount.grid(row=self.current_row,
                               column=self.set_entry_column,
                               padx=5, pady=5)
        review_clock = ttk.Label(self,
                                 textvariable=self.review_label_text)
        review_clock.grid(row=self.current_row,
                          column=self.time_column,
                          padx=5, pady=5)
        self.current_row += 1
        divide = ttk.Separator(self, orient=tk.HORIZONTAL)
        divide.grid(row=self.current_row, sticky="ew", columnspan=4)

        # --------- Relax line -------
        self.current_row += 1
        relax_instruction = ttk.Label(self,
                                      text="Relax mind timer")
        relax_instruction.grid(row=self.current_row,
                               column=self.line_label,
                               padx=5, pady=5)
        relax_amount = ttk.Entry(self, justify=tk.RIGHT, width=9,
                                 textvariable=self.relax_input_value)
        relax_amount.grid(row=self.current_row,
                          column=self.entry_colomn,
                          padx=5, pady=9)
        set_relax_amount = ttk.Button(self,
                                      text="SET",
                                      command=self.set_user_input)
        set_relax_amount.configure(command=lambda: self.set_user_input("relax"))
        set_relax_amount.grid(row=self.current_row,
                              column=self.set_entry_column,
                              padx=5, pady=5)
        relax_clock = ttk.Label(self,
                                textvariable=self.relax_label_text)
        relax_clock.grid(row=self.current_row,
                         column=self.time_column,
                         padx=5, pady=5)
        self.current_row += 1
        divide = ttk.Separator(self, orient=tk.HORIZONTAL)
        divide.grid(row=self.current_row, sticky="ew", columnspan=4)

        # --------- control column line -------
        self.current_row += 1

        self.error_message = tk.StringVar()
        error_message_label = ttk.Label(self, textvariable=self.error_message)
        error_message_label.grid(row=self.current_row, column=0, columnspan=2)
        start_button = ttk.Button(self, text="Start", command=self.start_timer)
        start_button.grid(row=self.current_row, column=2, padx=5, pady=30, ipady=5, sticky=tk.S)
        quit = ttk.Button(self, text="Quit", command=self.quit)
        quit.grid(row=self.current_row, column=3, padx=5, pady=30, ipady=5, sticky=tk.S)
        self.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        self.set_vals()

    def set_vals(self):
        """Set the clock values"""
        self.seconds = 0
        # Reversed so self.minute ends at the starting val
        for key, item in enumerate(reversed(self.item)):
            self.minutes = self.minute_vals[key]
            self.update_clock(item)

    def start_timer(self, context=0):
        """The main timer routine

        This is what this whole program is about.
        It recursively calling itself.
        """
        self.seconds -= 1
        if self.seconds == -1:
            self.seconds = 59
            self.minutes -= 1
        self.update_clock(self.item[context])
        if self.minutes > 0 or self.seconds > 0:
            self.master.after(1000, lambda: self.start_timer(context))
        else:
            self.item[context].set("DONE!")
            self.snd.play(blocking=1)
            context += 1
            if context < len(self.item):
                self.seconds = 0
                val = self.item[context].get().split(':')[0]
                self.minutes = int(val)
                self.start_timer(context)
            else:
                context = 0
                self.set_vals()
                val = self.item[context].get().split(':')[0]
                self.minutes = int(val)
                self.start_timer(context)


def main():
    """Run the tk timer"""
    root = tk.Tk()
    Timer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
