from input_excel import *
from day_info_algo import *
from place_algo_main import *
from output_excel import *
from output_excel_final import *
import timeit


def main():
    time_start = timeit.default_timer()  # Run-timer

    indata = ExcelIn()  # Load excel into programme and create leader-objects
    daydata = DayAlgo(indata)  # Calculate how many shifts per day and the total hours
    scheme = PlacerAlgoMain(indata, daydata)  # Place out new shifts
    """ Out """
    ExcelOutMain(scheme)  # Scheme sheet
    ExcelOutData(scheme, time_start)  # All data sheet



if __name__ == '__main__':
    main()
