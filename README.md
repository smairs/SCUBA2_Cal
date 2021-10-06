# SCUBA2_Cal

Using Archimedes CSV files to summarise the state of SCUBA-2 Calibration.

This program produces plots that summarise the current condition of the SCUBA-2 calibration for
JCMT operations meetings. The input is an archimedes-downloaded CSV file over any time range, including any
number of sources.

Steve Mairs, September 2021

**param CSVFILE:** The CSV file downloaded from archimedes. Can include mmultiple sources and a mixture of 450 and 850 micron data

**param nominal_450_FCFpeak:** The expected 450 micron FCF peak value (default = 472)

**param nominal_850_FCFpeak:** The expected 850 micron FCF peak value (default = 495)

**param nominal_450_FCFpeak:** The expected 450 micron FCF arcsec value (default = 3.87)

**param nominal_850_FCFpeak:** The expected 850 micron FCF arcsec value (default = 2.07)

**returns:**  Scatterplots of the FCF_arcsec and FCF_peak as a function of UT and Transmission, histograms of the FCFs, and aspect ratios of the sources. Coloured by source with shapes indicating main hardware changes throughout history. Organised in a directory called "ops_meeting_plots_HH:MM:SS" where HH:MM:SS is the time the program is run.


Necessary Packages: 

pandas

numpy

seaborn

matplotlib

astropy

collections

datetime

pytz

os


Example: 

\>\>\>from SCUBA2_cal_ops_meeting import SCUBA2cal
\>\>\>SCUBA2cal('archimedes-results-2019_to_2021_example.csv')
