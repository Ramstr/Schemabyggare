import random
import math
from CONFIG import *



class PlacerAlgoMethod:
    """ Places out all new shifts  """
    def __init__(self, ledare, days):
        self.excelin = ledare
        self.day = days
        self.led = self.excelin.led

        self.ilow, self.ihigh = self.excelin.led_index()  # Index for ul/hl
        self.fail_log = []
        self.algo_loop_counter = 0

        """ Counters for number of shifts per type """
        self.A_count = self.day.A_count
        self.B_count = self.day.B_count
        self.C_count = self.day.C_count
        self.D_count = self.day.D_count
        self.L_count = self.day.L_count

        self.hlA_count = self.day.hlA_count
        self.hlB_count = self.day.hlB_count
        self.hlC_count = self.day.hlC_count
        self.hlD_count = self.day.hlD_count
        self.hlL_count = self.day.hlL_count


        """ Max number of B and C shifts"""
        self.bmax = math.ceil((self.ihigh + 1 - self.ilow - amax - dmax) / 2)
        self.cmax = math.floor((self.ihigh + 1 - self.ilow - amax - dmax) / 2)
        self.hlbmax = math.ceil((self.ilow - hlamax - hldmax) / 2)
        self.hlcmax = math.floor((self.ilow - hlamax - hldmax) / 2)






    def setters(self, it, type, typecount, checkfunc, max, hl, op):
        """
        The setter method controls how shifts are placed, uses check-methods to determine how good a shift are.
        Uses responses (res) from check-methods. If no spot is good then let failed_loop-method try and place instead
        :param it: int, interation (which day)
        :param type: str, shift type to place
        :param typecount: list, type counter for given type
        :param checkfunc: callback method, which checker-method to use
        :param max: int, max number of leds per type per day
        :param hl: bool, is led an HL
        :return: places shift, else let failed_loop try
        """

        failed_loops = 0
        while typecount[it] < max and failed_loops < max_fail_count:

            index_list_ul = []
            index_list_hl = []

            # Get available leds
            for led in self.led:
                if led.available[it]:
                    if led.isHl:
                        index_list_hl.append(led.index)
                    else:
                        index_list_ul.append(led.index)

            # Debugg
            # print('hl', index_list_hl, 'ul:', index_list_ul, type, it)
            # print(typecount[it], max, failed_loops, max_fail_count, hl)
            # print(f"D: {self.D_count}, dhl: {self.hlD_count}, failed: {failed_loops < max_fail_count}")

            # pick a random leader (index)
            if hl:
                if index_list_hl == []:  # stop if none is available
                    break
                index = random.choice(index_list_hl)
            else:
                if index_list_ul == []:
                    break
                index = random.choice(index_list_ul)


            res = checkfunc(index, it, op)  # Check with check-method and get a respons
            # print(res)
            if res == 1:  # All good
                self.add(it, index, type)
            elif res == 2:  # Could work
                if failed_loops > max_fail_count / 2:
                    self.add(it, index, type)
                else:
                    failed_loops += 1
            elif res == 3:  # Doesn't work
                failed_loops += 1
            self.algo_loop_counter += 1

            # If no spot is good
            if failed_loops >= max_fail_count - 3:
                print(index_list_hl)
                print(index_list_ul)
                print(type, hl, it)
                self.failed_loop(type, hl, it)

    def failed_loop(self, type, hl, it):
        """ If no spot is good, force-place a shift in the best available spot"""
        for i, led in enumerate(self.led):

            if hl == led.isHl:
                if led.available[it]:
                    if type == "C":
                        self.add(it, i, "Fc")

                    elif type == "B":
                        self.add(it, i, "Fb")

                    elif type == "D":
                        self.add(it, i, "Fd")

                    elif type == "A":
                        self.add(it, i, "Fa")

                    msg = f" Kunde inte placera {type} på dag {it}. {led.name} tvingades därför på ett {type} pass." \
                          f" Kraven är för snäva, pröva igen eller ändra kraven "
                    self.fail_log.append([msg])
                    print(f" {hl}: {type} loop failed on day {it} for row {i} ({led.name})")
                    break

    def add(self, col, row, type):
        """ When shift is added: add to type counter, total hours, set unavailable"""
        self.led[row].total[col] = type
        self.led[row].available[col] = False
        """
        var listan
        om huvudledare -> hl listorna
        bokstav(X) 
        lista a,b,c,d
        
        """



        if type == "A" or type == "Fa":
            if self.led[row].isHl is False:
                self.A_count[col] += 1
                self.led[row].hours[col] = Ah
            elif self.led[row].isHl:
                self.hlA_count[col] += 1
                self.led[row].hours[col] = Ahhl
        elif type == "B" or type == "Fb":

            if self.led[row].isHl is False:
                self.B_count[col] += 1

                self.led[row].hours[col] = Bh

            elif self.led[row].isHl:
                self.hlB_count[col] += 1
                self.led[row].hours[col] = Bhhl
        elif type == "C" or type == "Fc":

            if self.led[row].isHl is False:
                self.C_count[col] += 1
                self.led[row].hours[col] = Ch
            elif self.led[row].isHl:
                self.hlC_count[col] += 1
                self.led[row].hours[col] = Chhl
        elif type == "D" or type == "Fd":

            if self.led[row].isHl is False:
                self.D_count[col] += 1
                self.led[row].hours[col] = Dh
            elif self.led[row].isHl:
                self.hlD_count[col] += 1
                self.led[row].hours[col] = Dhhl
        elif type == 'L':
            pass
        else:
            self.led[row].available[col] = True

    """ CHECKERS """

    def op(self, it, num, op='-'):

        if op == '+':
            return it + num
        elif op == '-':
            return it - num

    def range_op(self, it, num1, num2, first=True, op='-'):
        if first:
            if op == '+':
                return it + num1
            elif op == '-':
                return it - num2
        if first is False:
            if op == '+':
                return it + num2
            elif op == '-':
                return it - num1



    def check_d(self, index, it, op='-'):

        if self.led[index].available[it]:
            soft_req = self.led[index].total[self.range_op(it, 1, 3, True, op):self.range_op(it, 1, 3, False, op)]
            hard_req = self.led[index].total[self.op(it, 1, op)]
            try:
                if hard_req != "A" and hard_req != "D":  # No D/A in a row

                    if 'D' in soft_req:  # Maybe not D in the last 3 day
                        return 2
                    else:
                        return 1  # all god
                else:
                    return 3  # nope
            except IndexError:
                return 2  # could work
        else:
            return 3

    def check_a(self, index, it, op='-'):
        if self.led[index].available[it]:
            hard_req = self.led[index].total[self.op(it, 1, op)]
            soft_req = self.led[index].total[self.range_op(it, 1, 3, True, op):self.range_op(it, 1, 3, False, op)]
            try:
                if hard_req != "A" and hard_req != "D":
                    if 'A' in soft_req:
                        return 2
                    else:
                        return 1  # all god
                else:
                    return 3  # nope
            except IndexError:

                return 2  # could work
        else:
            return 3

    def check_b(self, index, it, op='-'):
        if self.led[index].available[it]:
            soft_req = self.led[index].isUnderh[self.op(it, 1, op)]
            try:
                if soft_req is True:
                    return 1
                else:
                    return 2

            except IndexError:
                return 2

        else:
            return 3

    def check_c(self, index, it, op='-'):
        if self.led[index].available[it]:
            soft_req = self.led[index].isUnderh[self.op(it, 1, op)]
            #print(f"it: {it}, num: 1, op: {op}, opreturn: {self.op(it, 1, op)} soft: {soft_req}")
            try:
                if soft_req is False:
                    return 1
                else:
                    return 2
            except IndexError:
                return 2

        else:
            return 3

    """ Terminal Outputs """

    def output(self):
        """ Prints to terminal """
        counter = 0
        print("\n")
        for i in self.led:
            # if i.isHl is False:
            print(
                f"{self.led[counter].name}:    {self.led[counter].total}      Total hours: {self.led[counter].hours_tot}")
            counter += 1

    def output_aval(self):
        """ Prints to terminal (availability) """
        counter = 0
        print("\n")
        for i in self.led:
            # if i.isHl is False:
            print(
                f"{self.led[counter].name}:    {self.led[counter].available}      Avaliable: {sum(self.led[counter].available)}")
            counter += 1

    def output_under_houred(self):
        """ Prints to terminal (under houred (bools)) """
        counter = 0
        print("\n")
        for i in self.led:
            # if i.isHl is False:
            print(
                f"{self.led[counter].name}:    {self.led[counter].isUnderh}      Avaliable: {self.led[counter].hours_tot}")
            counter += 1

    def output_hours(self):
        """ Prints to terminal (Hours) """
        counter = 0
        print("\n")
        for i in self.led:
            # print(self.led[counter].hours)
            print(
                f"{self.led[counter].name}:    {self.led[counter].hours}      Avaliable: {self.led[counter].hours_tot}")
            counter += 1

    def output_counter(self):
        """ Prints to terminal (shift type counter) """
        print("\n")

        # if i.isHl is False:
        print(f"  A :    {self.A_count}      Hl: {self.hlA_count}")
        print(f"  B :    {self.B_count}      Hl: {self.hlB_count}")
        print(f"  C :    {self.C_count}      Hl: {self.hlC_count}")
        print(f"  D :    {self.D_count}      Hl: {self.hlD_count}")
        print(f"  L :    {self.L_count}      Hl: {self.hlL_count}")
