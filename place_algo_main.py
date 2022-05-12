from place_algo_methods import *

class PlacerAlgoMain(PlacerAlgoMethod):

    def __init__(self, ledare, days):
        super().__init__(ledare, days)
        self.last_off_day = 0

        """ Method exe"""
        self.det_off_days()
        self.run_week()
        self.excelin.calc_total_hours()



        """ Terminal outputs """

        self.output_counter()
        self.output_under_houred()
        # self.output_hours()
        # self.output_aval()
        self.output()


    def run_week(self):
        for i in range(self.last_off_day, -1, -1):
            self.run_day(i, '+')

        for i in range(self.last_off_day +1, len(self.led[0].total)):
            # input(f"\nDay {i}")

            self.run_day(i)

    def run_day(self, it, op='-'):
        self.run_setter(it, op)  # Place shift
        if op == '-':
            self.day.under_houred_calc(it)  # Calc under houred
        elif op == '+':
            self.rev_underh_calc(it, self.last_off_day)
        #print(input(f"Dag {it} körd"))

    def run_setter(self, it, op):
        """ Controls the order to place the shift types"""
        self.setters(it, 'D', self.D_count, self.check_d, dmax, False, op)
        self.setters(it, 'D', self.hlD_count, self.check_d, hldmax, True, op)
        self.setters(it, 'A', self.A_count, self.check_a, amax, False, op)
        self.setters(it, 'A', self.hlA_count, self.check_a, hlamax, True, op)

        self.setters(it, 'B', self.B_count, self.check_b, self.bmax, False, op)
        self.setters(it, 'B', self.hlB_count, self.check_b, self.hlbmax, True, op)
        self.setters(it, 'C', self.C_count, self.check_c, self.cmax, False, op)
        self.setters(it, 'C', self.hlC_count, self.check_c, self.hlcmax, True, op)

    def det_off_days(self):
        off_days = []
        for it, L in enumerate(self.L_count):
            if L >= self.ihigh//3:
                off_days.append(it)
        if off_days:
            self.last_off_day = off_days[-1]

    def rev_underh_calc(self, it, off_day):
        """ Calc if leds are under houred  - reversed"""
        hour_list_ul = []
        hour_list_hl = []

        # Append all hours to list
        for led in self.led:
            if led.isHl is False:
                hour_list_ul.append(sum(led.hours[it:off_day+1]))

            elif led.isHl is True:
                hour_list_hl.append(sum(led.hours[it:off_day+1]))
        hour_list_ul.sort()
        hour_list_hl.sort()
        #print('it', it, ' offday', off_day)
        #print(hour_list_hl)

        # Determine if led is under houred
        for i in self.led:

            """(sum(i.hours[it:off_day + 1]), '<', (sum(hour_list_ul)) / (len(hour_list_ul)),
                  sum(i.hours[it:off_day+1]) < (sum(hour_list_ul) / (len(hour_list_ul))))"""
            if i.isHl:
                continue
            if sum(i.hours[it:off_day+1]) < (sum(hour_list_ul) / (len(hour_list_ul))):
                i.isUnderh[it] = True

        for i in self.led:
            if i.isHl is False:
                continue
            if sum(i.hours[it:off_day+1]) < (sum(hour_list_hl) / (len(hour_list_hl))):
                i.isUnderh[it] = True

        """
        for i in self.led:
            print(f"\n led: {i.name} in range {it}:{off_day+1}")
            print(hour_list_ul, sum(hour_list_ul), len(hour_list_ul))
            print((sum(i.hours[it:off_day + 1]), '<', (sum(hour_list_ul)) / (len(hour_list_ul)),
                  sum(i.hours[it:off_day+1]) < (sum(hour_list_ul) / (len(hour_list_ul)))))"""
