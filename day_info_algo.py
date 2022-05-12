class DayAlgo:
    """
    Get info for the day, i.e how many shifts per type (A,B,C,D,L) and determain who is under houred
    """
    def __init__(self, ledare):
        self.excelin = ledare
        self.led = self.excelin.led
        self.ilow, self.ihigh = self.excelin.led_index()

        """ Counter for number of shifts per type """
        self.A_count = []
        self.B_count = []
        self.C_count = []
        self.D_count = []
        self.L_count = []

        self.hlA_count = []
        self.hlB_count = []
        self.hlC_count = []
        self.hlD_count = []
        self.hlL_count = []

        """ Methods exe """
        self.type_count_filler()  # fill up all the lists
        self.iter_leds()
        #self.run_week()


        """ Terminal outputs """
        # self.output_counter()
        # self.output_under_houred()

    def type_count_filler(self):
        """ Fill up all the spots, shifts are mutated not appended for the rest of the programme"""
        for i in range(len(self.led[0].total)):
            self.A_count.append(0)
            self.B_count.append(0)
            self.C_count.append(0)
            self.D_count.append(0)
            self.L_count.append(0)
            self.hlA_count.append(0)
            self.hlB_count.append(0)
            self.hlC_count.append(0)
            self.hlD_count.append(0)
            self.hlL_count.append(0)

    def iter_leds(self):
        """ Loop trough all: add shift type count for each shift and tag everyone as not under-houred"""
        for i in range(len(self.led)):
            for y in range(len(self.led[0].total)):
                self.type_count(i, y, self.led[i].total[y])
                self.led[i].isUnderh.append(False)

    def type_count(self, i, y, type):
        """ Check for shift type and add to counter"""
        # print('in', i, y, type)
        if type == "A" or type == "Fa":

            if self.led[i].isHl is False:
                self.A_count[y] += 1

            elif self.led[i].isHl:
                self.hlA_count[y] += 1

        elif type == "B" or type == "Fb":

            if self.led[i].isHl is False:
                self.B_count[y] += 1

            elif self.led[i].isHl:
                self.hlB_count[y] += 1

        elif type == "C" or type == "Fc":

            if self.led[i].isHl is False:
                self.C_count[y] += 1

            elif self.led[i].isHl:
                self.hlC_count[y] += 1

        elif type == "D" or type == "Fd":

            if self.led[i].isHl is False:
                self.D_count[y] += 1

            elif self.led[i].isHl:
                self.hlD_count[y] += 1

        elif type == "L":

            if self.led[i].isHl is False:
                self.L_count[y] += 1

            elif self.led[i].isHl:
                self.hlL_count[y] += 1

        else:
            self.led[i].available[y] = True

    def run_week(self):
        """ loop trough all days"""
        for i in range(len(self.led[0].total)):
            # input(f"\nDay {i}")
            self.run_day(i)

            # self.output()

    def run_day(self, it):
        """ loop trough each day """
        #self.under_houred_calc(it)

    def under_houred_calc(self, it):
        """ Calc if leds are under houred """
        hour_list_ul = []
        hour_list_hl = []

        # Append all hours to list
        for led in self.led:
            if led.isHl is False:
                hour_list_ul.append(sum(led.hours[0:it+1]))

            elif led.isHl is True:
                hour_list_hl.append(sum(led.hours[0:it+1]))
        hour_list_ul.sort()
        hour_list_hl.sort()

        # Determine if led is under houred
        for i in self.led:
            if i.isHl:
                continue
            if sum(i.hours[0:it+1]) < (sum(hour_list_ul) / len(hour_list_ul)):
                #print(i.name, "got set to true")
                i.isUnderh[it] = True
                # print("is ul and is under")

        for i in self.led:
            if i.isHl is False:
                continue
            if sum(i.hours[0:it+1]) < (sum(hour_list_hl) / len(hour_list_hl)):

                i.isUnderh[it] = True

        """for i in self.led:
            print(f"\n led: {i.name} in range 0:{it+1}")
            print(hour_list_ul, sum(hour_list_ul), len(hour_list_ul))
            print((sum(i.hours[0:it + 1]), '<', (sum(hour_list_ul)) / (len(hour_list_ul)),
                  sum(i.hours[0:it+1]) < (sum(hour_list_ul) / (len(hour_list_ul)))), i.isUnderh[it])"""


    """ Terminal Outputs """

    def output_under_houred(self):
        """ Prints to terminal (under houred (bools)) """
        counter = 0
        print("\n")
        for i in self.led:
            # if i.isHl is False:
            print(
                f"{self.led[counter].name}:    {self.led[counter].isUnderh}      Avaliable: {self.led[counter].hours_tot}")
            counter += 1

    def output_counter(self):
        """ Prints to terminal (Type counters) """

        print("\n")

        # if i.isHl is False:
        print(f"  A :    {self.A_count}      Hl: {self.hlA_count}")
        print(f"  B :    {self.B_count}      Hl: {self.hlB_count}")
        print(f"  C :    {self.C_count}      Hl: {self.hlC_count}")
        print(f"  D :    {self.D_count}      Hl: {self.hlD_count}")
        print(f"  L :    {self.L_count}      Hl: {self.hlL_count}")
