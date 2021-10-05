import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from astropy.time import Time
from collections import OrderedDict
import datetime
import pytz
import os

##################################################
# Set up plot style for consistency for paper!
from matplotlib.pyplot import rc
rc('text', usetex=True)
rc('font',family = 'serif')
rc('xtick', labelsize=14)
rc('xtick', top=True)
rc('xtick', direction='in')
rc('ytick', labelsize=14)
rc('ytick', right=True)
rc('ytick', direction='in')
rc('legend', markerscale=1)
rc('legend', fontsize='small')
rc('legend', framealpha=1)
rc('axes',labelsize=16)
##################################################

def SCUBA2cal(CSVFILE='archimedes-results-2019_to_2021_example.csv',nominal_450_FCFpeak = 472,nominal_450_FCFasec=3.87,
              nominal_850_FCFpeak=495,nominal_850_FCFasec=2.07):
    '''
    This program produces plots that summarise the current condition of the SCUBA-2 calibration for
    JCMT operations meetings. The input is an archimedes-downloaded CSV file over any time range, including any
    number of sources.

    Steve Mairs, September 2021

    :param CSVFILE: The CSV file downloaded from archimedes. Can include mmultiple sources and a mixture of
    450 and 850 micron data
    :param nominal_450_FCFpeak: The expected 450 micron FCF peak value (default = 472)
    :param nominal_850_FCFpeak: The expected 850 micron FCF peak value (default = 495)
    :param nominal_450_FCFpeak: The expected 450 micron FCF arcsec value (default = 3.87)
    :param nominal_850_FCFpeak: The expected 850 micron FCF arcsec value (default = 2.07)
    :return:  Scatterplots of the FCF_arcsec and FCF_peak as a function of UT and Transmission, histograms of the FCFs,
    and aspect ratios of the sources. Coloured by source with shapes indicating main hardware changes throughout history
    '''


    # Read in the CSV file
    cat_df = pd.read_csv(CSVFILE)

    # Create a directory to store plots, labelled with date and time
    current_time   = str(datetime.datetime.now()).replace(' ','_').split('.')[0]
    output_dirname = 'ops_meeting_plots_{}'.format(current_time)
    os.system('mkdir {}'.format(output_dirname))

    # Define dictionaries of notable dates. The first is a comprehensive list of all known hardware changes
    # That have taken place since 2011 and may affect data. All dates inclusive:

    # Key:
    # Dempsey            = Data published by Dempsey et al 2012.
    # SIL                = Silver WVM in use
    # WVM_out_of_service = Data unreliable due to unreliable extinction correction
    # BLA                = Black WVM in use
    # NEWF               = New Thermal Filter Stacks Installed (MAJOR FCF CHANGE)
    # MEMOFF             = Membrane removed from telescope for POL-2 commissioning. The instability of the dish,
    #                      i.e. beam-smearing counteracted the improved transmission resulting in no significant change
    # MEMON              = Membrane replaced after POL-2 commissioning.
    # SMUT               = Secondary Mirror Unit Trouble -- the SMU was malfunctioning, creating large aspect ratios
    # SMUG               = Secondary Mirror Unit Gain fix -- The gain was adjusted as a temporary fix to SMU trouble
    #                      (MAJOR FCF CHANGE)
    # SMUHW              = Secondary Mirror Unit Hardware fix -- The SMU hardware was adjusted for a more permanent fix

    hardware_changes = OrderedDict()
    hardware_changes['Dempsey_start']        = Time("2011-05-01T00:00:00.00",format='isot',scale='utc')
    hardware_changes['Dempsey_end']          = Time("2012-05-31T00:00:00.00",format='isot',scale='utc')
    hardware_changes['SIL_start']            = Time("2012-06-01T00:00:00.00",format='isot',scale='utc')
    hardware_changes['WVM_out_of_service']   = Time("2013-03-15T00:00:00.00",format='isot',scale='utc')
    hardware_changes['WVM_back_in_service']  = Time("2013-04-09T00:00:00.00",format='isot',scale='utc')
    hardware_changes['SIL_end']              = Time("2015-01-27T00:00:00.00",format='isot',scale='utc')
    hardware_changes['WVM_out_of_service2']  = Time("2015-01-28T00:00:00.00", format='isot', scale='utc')
    hardware_changes['WVM_back_in_service2'] = Time("2015-04-09T00:00:00.00", format='isot', scale='utc')
    hardware_changes['BLA_start']            = Time("2015-04-10T00:00:00.00",format='isot',scale='utc')
    hardware_changes['BLA_end']              = Time("2016-10-05T00:00:00.00",format='isot',scale='utc')
    hardware_changes['NEWF_start']           = Time("2016-10-06T00:00:00.00",format='isot',scale='utc')
    hardware_changes['NEWF_end']             = Time("2017-12-05T00:00:00.00",format='isot',scale='utc')
    hardware_changes['MEMOFF_start']         = Time("2017-12-06T00:00:00.00",format='isot',scale='utc')
    hardware_changes['MEMOFF_end']           = Time("2018-01-10T00:00:00.00",format='isot',scale='utc')
    hardware_changes['MEMON_start']          = Time("2018-01-11T00:00:00.00",format='isot',scale='utc')
    hardware_changes['MEMON_end']            = Time("2018-05-01T00:00:00.00",format='isot',scale='utc')
    hardware_changes['SMUT_start']           = Time("2018-05-02T00:00:00.00",format='isot',scale='utc')
    hardware_changes['SMUT_end']             = Time("2018-06-30T08:10:00.00",format='isot',scale='utc')
    hardware_changes['SMUG_start']           = Time("2018-06-30T08:11:00.00",format='isot',scale='utc')
    hardware_changes['SMUG_end']             = Time("2018-07-25T00:00:00.00",format='isot',scale='utc')
    hardware_changes['SMUHW_start']          = Time("2018-07-28T00:00:00.00",format='isot',scale='utc')
    hardware_changes['SMUHW_end']            = Time("2500-12-30T00:00:00.00",format='isot',scale='utc')

    # This next list was derived during work for the 10-year SCUBA-2 calibration paper (Mairs et al 2021) and represents
    # Major and obvious changes to the FCFs over time. i.e. These dates define "step functions" in the FCFs over time.

    most_important_dates = OrderedDict()
    most_important_dates['filter_change']  = Time("2016-10-06T00:00:00.00", format='isot', scale='utc')
    most_important_dates['smu_adjustment'] = Time("2018-06-30T08:11:00.00", format='isot', scale='utc')

    # Historical RxA Warmups and Cooldowns - which can affect SCUBA-2 Performance!

    RxA_warmups = [Time("2015-11-21T05:00:00.00", format='isot', scale='utc'),
                   Time("2016-08-08T00:00:00.00", format='isot', scale='utc'),
                   Time("2016-10-21T03:00:00.00", format='isot', scale='utc'),
                   Time("2016-11-02T02:00:00.00", format='isot', scale='utc'),
                   Time("2016-11-09T06:00:00.00", format='isot', scale='utc'),
                   Time("2017-01-19T10:00:00.00", format='isot', scale='utc'),
                   Time("2017-03-16T21:00:00.00", format='isot', scale='utc'),
                   Time("2017-05-23T16:00:00.00", format='isot', scale='utc'),
                   Time("2017-07-03T10:00:00.00", format='isot', scale='utc'),
                   Time("2018-02-21T22:00:00.00", format='isot', scale='utc'),
                   Time("2018-02-28T10:00:00.00", format='isot', scale='utc'),
                   Time("2018-06-26T10:00:00.00", format='isot', scale='utc')]

    RxA_cooldowns = [Time("2016-01-06T02:00:00.00", format='isot', scale='utc'),
                     Time("2016-08-12T02:00:00.00", format='isot', scale='utc'),
                     Time("2016-10-28T05:00:00.00", format='isot', scale='utc'),
                     Time("2016-11-03T02:00:00.00", format='isot', scale='utc'),
                     Time("2016-11-10T06:00:00.00", format='isot', scale='utc'),
                     Time("2017-01-30T10:00:00.00", format='isot', scale='utc'),
                     Time("2017-03-24T00:00:00.00", format='isot', scale='utc'),
                     Time("2017-06-07T10:00:00.00", format='isot', scale='utc'),
                     Time("2017-07-10T10:00:00.00", format='isot', scale='utc'),
                     Time("2018-02-22T22:00:00.00", format='isot', scale='utc'),
                     Time("2018-03-06T10:00:00.00", format='isot', scale='utc')]

    # Add columns to the CSV file indicating within which epochs, defined above, the data point resides.

    obs_epoch = []
    obs_detailed_epoch = []
    for each_obs_time in cat_df['ut']:
        each_obs_time = Time(each_obs_time.replace(' ','T'),format='isot',scale='utc')
        if each_obs_time<hardware_changes['Dempsey_start']:
            obs_detailed_epoch.append('Pre-Dempsey')
            obs_epoch.append('Pre-Filter Change')
        elif each_obs_time>=hardware_changes['Dempsey_start'] and \
                each_obs_time<hardware_changes['SIL_start']:
            obs_detailed_epoch.append('Dempsey')
            obs_epoch.append('Pre-Filter Change')
        elif each_obs_time>=hardware_changes['SIL_start'] and \
                each_obs_time<hardware_changes['WVM_out_of_service']:
            obs_detailed_epoch.append('Silver WVM')
            obs_epoch.append('Pre-Filter Change')
        elif each_obs_time>=hardware_changes['WVM_out_of_service'] and \
                each_obs_time<hardware_changes['WVM_back_in_service']:
            obs_detailed_epoch.append('WVM Out Of Service')
            obs_epoch.append('Pre-Filter Change')
        elif each_obs_time>=hardware_changes['WVM_back_in_service'] and \
                each_obs_time<hardware_changes['WVM_out_of_service2']:
            obs_detailed_epoch.append('Silver WVM')
            obs_epoch.append('Pre-Filter Change')
        elif each_obs_time>=hardware_changes['WVM_out_of_service2'] and \
                each_obs_time<hardware_changes['BLA_start']:
            obs_detailed_epoch.append('WVM Out Of Service 2')
            obs_epoch.append('Pre-Filter Change')
        elif each_obs_time>=hardware_changes['BLA_start'] and \
                each_obs_time<hardware_changes['NEWF_start']:
            obs_detailed_epoch.append('Black WVM')
            obs_epoch.append('Pre-Filter Change')
        elif each_obs_time>=hardware_changes['NEWF_start'] and \
                each_obs_time<hardware_changes['MEMOFF_start']:
            obs_detailed_epoch.append('New Filters')
            obs_epoch.append('Post-Filter Change')
        elif each_obs_time>=hardware_changes['MEMOFF_start'] and \
                each_obs_time<hardware_changes['MEMON_start']:
            obs_detailed_epoch.append('Membrane Off')
            obs_epoch.append('Post-Filter Change')
        elif each_obs_time>=hardware_changes['MEMON_start'] and \
                each_obs_time<hardware_changes['SMUT_start']:
            obs_detailed_epoch.append('Membrane Back On')
            obs_epoch.append('Post-Filter Change')
        elif each_obs_time>=hardware_changes['SMUT_start'] and \
                each_obs_time<hardware_changes['SMUG_start']:
            obs_detailed_epoch.append('SMU Malfunction')
            obs_epoch.append('Post-Filter Change')
        elif each_obs_time>=hardware_changes['SMUG_start'] and \
                each_obs_time<hardware_changes['SMUHW_start']:
            obs_detailed_epoch.append('SMU Gain Fix')
            obs_epoch.append('Post-SMU Fix')
        elif each_obs_time>=hardware_changes['SMUHW_start'] and \
                each_obs_time<hardware_changes['SMUHW_end']:
            obs_detailed_epoch.append('SMU HW Fix')
            obs_epoch.append('Post-SMU Fix')
        else:
            print(each_obs_time)

    cat_1   = cat_df.assign(epoch=obs_epoch)
    cat_2   = cat_1.assign(detailed_epoch=obs_detailed_epoch)

    # Create a date axis that we can plot with seaborn (just need a change of format)

    ut_modified = []
    mjds        = []
    for each_obs_time in cat_df['ut']:
        ut_modified.append(each_obs_time.split()[0])
        mjds.append(Time(each_obs_time.replace(' ','T'),format='isot',scale='utc').mjd)

    time_range = (max(mjds)-min(mjds))/365.35 # In Years
    time_range_months = time_range*12

    cat     = cat_2.assign(date=ut_modified)
    pd.to_datetime(cat['date']).dt.strftime('%y-%m-%d')
    cat_450 = cat[cat['filter'] == 450]
    cat_850 = cat[cat['filter'] == 850]

    # Plot FCFArcsec versus UT date for 450 and 850

    print('\nPlotting FCF as a function of date...\n')

    if len(cat_450['filter'].to_list())>0:
        ax_FCFA_UT_450 = sns.scatterplot(x='date',y='fcfasec',
                                         hue=cat_450.targetname.tolist(),style=cat_450.epoch.tolist(),data=cat_450)
        ax_FCFA_UT_450.xaxis.set_major_locator(mdates.MonthLocator(interval=int(round(time_range_months/5))))
        plt.axhline(nominal_450_FCFasec,linestyle='dashed',linewidth='2',color='k')
        plt.legend(loc='upper left')
        plt.suptitle('450 Microns, FCF Arcsec')
        plt.ylim(ymax=12)
        plt.savefig('{}/FCFasec_vs_date_450.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()


    if len(cat_850['filter'].to_list()) > 0:
        ax_FCFA_UT_850 = sns.scatterplot(x='date',y='fcfasec',
                                         hue=cat_850.targetname.tolist(),style=cat_850.epoch.tolist(),data=cat_850)
        ax_FCFA_UT_850.xaxis.set_major_locator(mdates.MonthLocator(interval=int(round(time_range_months/5))))
        plt.axhline(nominal_850_FCFasec,linestyle='dashed',linewidth='2',color='k')
        plt.legend(loc='upper left')
        plt.ylim(ymax=4)
        plt.suptitle('850 Microns, FCF Arcsec')
        plt.savefig('{}/FCFasec_vs_date_850.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    # Plot FCFPeak versus UT date for 450 and 850

    if len(cat_450['filter'].to_list())>0:
        ax_FCFP_UT_450 = sns.scatterplot(x='date',y='fcfbeam',
                                         hue=cat_450.targetname.tolist(),style=cat_450.epoch.tolist(),data=cat_450)
        ax_FCFP_UT_450.xaxis.set_major_locator(mdates.MonthLocator(interval=int(round(time_range_months/5))))
        plt.axhline(nominal_450_FCFpeak,linestyle='dashed',linewidth='2',color='k')
        plt.legend(loc='upper left')
        plt.suptitle('450 Microns, FCF Peak')
        plt.ylim(ymax=1400)
        plt.savefig('{}/FCFpeak_vs_date_450.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()


    if len(cat_850['filter'].to_list()) > 0:
        ax_FCFP_UT_850 = sns.scatterplot(x='date',y='fcfbeam',
                                         hue=cat_850.targetname.tolist(),style=cat_850.epoch.tolist(),data=cat_850)
        ax_FCFP_UT_850.xaxis.set_major_locator(mdates.MonthLocator(interval=int(round(time_range_months/5))))
        plt.axhline(nominal_850_FCFpeak,linestyle='dashed',linewidth='2',color='k')
        plt.legend(loc='upper left')
        plt.suptitle('850 Microns, FCF Peak')
        plt.savefig('{}/FCFpeak_vs_date_850.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    # Plot FCFArcsec versus UT time for 450 and 850

    print('\nPlotting FCF as a function of time...\n')

    if len(cat_450['filter'].to_list())>0:
        times_450 = [] # Since Midnight
        for i in cat_450['ut']:
            thisdate = i.split()[0]
            thistime = i.split()[-1]
            t = datetime.datetime(year=int(thisdate.split('-')[0]),month=int(thisdate.split('-')[1]),
                                  day=int(thisdate.split('-')[2]),hour=int(thistime.split(':')[0]),
                                  minute=int(thistime.split(':')[1]),
                                  second=int(thistime.split(':')[2])).replace(tzinfo=pytz.utc)
            hst_time = t.astimezone(pytz.timezone('US/Hawaii'))
            secs_since_midnight  = datetime.timedelta(hours=hst_time.hour,
                                                      minutes=hst_time.minute,seconds=hst_time.second).total_seconds()
            hours_since_midnight = secs_since_midnight/3600
            if hours_since_midnight >= 12 and hours_since_midnight <24:
                hours_centered_on_midnight = hours_since_midnight-24
            else:
                hours_centered_on_midnight = hours_since_midnight
            times_450.append(hours_centered_on_midnight)
        cat_450_times = cat_450.assign(uttime=times_450)
        sns.scatterplot(x='uttime',y='fcfasec',hue=cat_450_times.targetname.tolist(),style=cat_450_times.epoch.tolist(),
                        data=cat_450_times)
        plt.axvline(x=-3,color='k',linestyle='dashed')
        plt.axvline(x=7, color='k', linestyle='dashed')
        plt.axhline(nominal_450_FCFasec,linestyle='dashed',linewidth='2',color='k')
        plt.xlim(xmin=-7,xmax=11)
        plt.ylim(ymin=0,ymax=8)
        plt.legend(loc='upper center')
        plt.suptitle('450 Microns, FCF Arcsec, 0.0 = Midnight HST')
        plt.text(2.2,0.5,'Stable: 21:00--07:00 HST',size=12,ha="center", va="center",
                 bbox=dict(boxstyle="round",ec='oldlace',fc='oldlace',))
        plt.savefig('{}/FCFasec_vs_time_450.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    if len(cat_850['filter'].to_list())>0:
        times_850 = [] # Since Midnight
        for i in cat_850['ut']:
            thisdate = i.split()[0]
            thistime = i.split()[-1]
            t = datetime.datetime(year=int(thisdate.split('-')[0]),month=int(thisdate.split('-')[1]),
                                  day=int(thisdate.split('-')[2]),hour=int(thistime.split(':')[0]),
                                  minute=int(thistime.split(':')[1]),
                                  second=int(thistime.split(':')[2])).replace(tzinfo=pytz.utc)
            hst_time = t.astimezone(pytz.timezone('US/Hawaii'))
            secs_since_midnight  = datetime.timedelta(hours=hst_time.hour,
                                                      minutes=hst_time.minute,seconds=hst_time.second).total_seconds()
            hours_since_midnight = secs_since_midnight/3600
            if hours_since_midnight >= 12 and hours_since_midnight <24:
                hours_centered_on_midnight = hours_since_midnight-24
            else:
                hours_centered_on_midnight = hours_since_midnight
            times_850.append(hours_centered_on_midnight)
        cat_850_times = cat_850.assign(uttime=times_850)
        sns.scatterplot(x='uttime',y='fcfasec',hue=cat_850_times.targetname.tolist(),style=cat_850_times.epoch.tolist(),
                        data=cat_850_times)
        plt.axvline(x=-3,color='k',linestyle='dashed')
        plt.axvline(x=7, color='k', linestyle='dashed')
        plt.axhline(nominal_850_FCFasec,linestyle='dashed',linewidth='2',color='k')
        plt.xlim(xmin=-7,xmax=11)
        plt.ylim(ymin=1.5,ymax=3)
        plt.legend(loc='upper center')
        plt.suptitle('850 Microns, FCF Arcsec, 0.0 = Midnight HST')
        plt.text(2.2,1.7,'Stable: 21:00--07:00 HST',size=12,ha="center", va="center",
                 bbox=dict(boxstyle="round",ec='oldlace',fc='oldlace',))
        plt.savefig('{}/FCFasec_vs_time_850.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    if len(cat_450['filter'].to_list())>0:
        sns.scatterplot(x='uttime',y='fcfbeam',hue=cat_450_times.targetname.tolist(),style=cat_450_times.epoch.tolist(),
                        data=cat_450_times)
        plt.axvline(x=-3,color='k',linestyle='dashed')
        plt.axvline(x=7, color='k', linestyle='dashed')
        plt.axhline(nominal_450_FCFpeak,linestyle='dashed',linewidth='2',color='k')
        plt.xlim(xmin=-7,xmax=11)
        plt.ylim(ymin=0,ymax=1400)
        plt.legend(loc='upper center')
        plt.suptitle('450 Microns, FCF Peak, 0.0 = Midnight HST')
        plt.text(2.2,100,'Stable: 21:00--07:00 HST',size=12,ha="center", va="center",
                 bbox=dict(boxstyle="round",ec='oldlace',fc='oldlace',))
        plt.savefig('{}/FCFpeak_vs_time_450.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    if len(cat_850['filter'].to_list())>0:
        sns.scatterplot(x='uttime',y='fcfbeam',hue=cat_850_times.targetname.tolist(),style=cat_850_times.epoch.tolist(),
                        data=cat_850_times)
        plt.axvline(x=-3,color='k',linestyle='dashed')
        plt.axvline(x=7, color='k', linestyle='dashed')
        plt.axhline(nominal_850_FCFpeak,linestyle='dashed',linewidth='2',color='k')
        plt.xlim(xmin=-7,xmax=11)
        plt.ylim(ymin=400,ymax=800)
        plt.legend(loc='upper center')
        plt.suptitle('850 Microns, FCF Peak, 0.0 = Midnight HST')
        plt.text(2.2,425,'Stable: 21:00--07:00 HST',size=12,ha="center", va="center",
                 bbox=dict(boxstyle="round",ec='oldlace',fc='oldlace',))
        plt.savefig('{}/FCFpeak_vs_time_850.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    # Make FCFArcsec Histogram, label Peak, fit and measure SD

    print('\nPlotting FCF histograms...\n')

    if len(cat_450['filter'].to_list()) > 0:
        sns.distplot(cat_450['fcfasec'],kde=True)
        plt.axvline(nominal_450_FCFasec,linestyle='dashed',linewidth='2',color='k',
                    label='Post 2018-06\nRecommended Value')
        plt.ylabel('Normalised Density')
        plt.legend(loc='upper right')
        plt.suptitle('450 Microns, FCF Arcsec')
        plt.xlim(xmax=10)
        plt.savefig('{}/FCFasec_hist_450.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    if len(cat_850['filter'].to_list()) > 0:
        sns.distplot(cat_850['fcfasec'],kde=True)
        plt.axvline(nominal_850_FCFasec,linestyle='dashed',linewidth='2',color='k',
                    label='Post 2018-06\nRecommended Value')
        plt.ylabel('Normalised Density')
        plt.legend(loc='upper right')
        plt.xlim(xmax=4)
        plt.suptitle('850 Microns, FCF Arcsec')
        plt.savefig('{}/FCFasec_hist_850.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    # Make FCFPeak Histogram, label Peak, fit and measure SD

    if len(cat_450['filter'].to_list()) > 0:
        sns.distplot(cat_450['fcfbeam'],kde=True)
        plt.axvline(nominal_450_FCFpeak,linestyle='dashed',linewidth='2',color='k',
                    label='Post 2018-06\nRecommended Value')
        plt.ylabel('Normalised Density')
        plt.legend(loc='upper right')
        plt.suptitle('450 Microns, FCF Peak')
        plt.xlim(xmax=1400)
        plt.savefig('{}/FCFpeak_hist_450.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    if len(cat_850['filter'].to_list()) > 0:
        sns.distplot(cat_850['fcfbeam'],kde=True)
        plt.axvline(nominal_850_FCFpeak,linestyle='dashed',linewidth='2',color='k',
                    label='Post 2018-06\nRecommended Value')
        plt.ylabel('Normalised Density')
        plt.legend(loc='upper right')
        plt.suptitle('850 Microns, FCF Peak')
        plt.savefig('{}/FCFpeak_hist_850.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    # Plot FCFArcsec as function of Transmission

    print('\nPlotting FCFs as a function of transmission...\n')

    if len(cat_450['filter'].to_list()) > 0:
        sns.scatterplot(x='trans',y='fcfasec',hue=cat_450.targetname.tolist(),style=cat_450.epoch.tolist(),data=cat_450)
        plt.axhline(nominal_450_FCFasec,linestyle='dashed',linewidth='2',color='k')
        plt.legend(loc='upper left')
        plt.ylim(ymax=11)
        plt.suptitle('450 Microns, FCF Arcsec versus Transmission')
        plt.savefig('{}/FCFasec_vs_trans_450.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    if len(cat_850['filter'].to_list()) > 0:
        sns.scatterplot(x='trans',y='fcfasec',hue=cat_850.targetname.tolist(),style=cat_850.epoch.tolist(),data=cat_850)
        plt.axhline(nominal_850_FCFasec,linestyle='dashed',linewidth='2',color='k')
        plt.legend(loc='upper left')
        plt.ylim(ymax=4)
        plt.suptitle('850 Microns, FCF Arcsec versus Transmission')
        plt.savefig('{}/FCFasec_vs_trans_850.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    # Plot FCFPeak as function of Transmission

    if len(cat_450['filter'].to_list()) > 0:
        sns.scatterplot(x='trans',y='fcfbeam',hue=cat_450.targetname.tolist(),style=cat_450.epoch.tolist(),data=cat_450)
        plt.axhline(nominal_450_FCFpeak,linestyle='dashed',linewidth='2',color='k')
        plt.legend(loc='upper left')
        plt.suptitle('450 Microns, FCF Peak versus Transmission')
        plt.ylim(ymax=1400)
        plt.savefig('{}/FCFpeak_vs_trans_450.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    if len(cat_850['filter'].to_list()) > 0:
        sns.scatterplot(x='trans',y='fcfbeam',hue=cat_850.targetname.tolist(),style=cat_850.epoch.tolist(),data=cat_850)
        plt.axhline(nominal_850_FCFpeak,linestyle='dashed',linewidth='2',color='k')
        plt.legend(loc='upper left')
        plt.suptitle('850 Microns, FCF Peak versus Transmission')
        plt.savefig('{}/FCFpeak_vs_trans_850.png'.format(output_dirname),dpi=300)
        #plt.show()
        plt.clf()

    # Plot empirical beam area using Uranus data points observed between 21:00 - 07:00 HST

    print('\nPlotting Empirical Beam Area based on Uranus...\n')

    if len(cat_450['filter'].to_list()) > 0:
        if 'URANUS' in list(cat_450['targetname']):
            cat_uranus2       = cat_450[cat_450['targetname']=='URANUS']
            stable_index      = []
            for i in cat_uranus2['ut']:
                hour = float(i.split()[-1].split(':')[0])
                if hour >= 7 and hour <17:
                    stable_index.append(1)
                else:
                    stable_index.append(0)
            if len(np.array(stable_index)[np.where(np.array(stable_index)==1)])>2:
                cat_uranus = cat_uranus2.assign(stable_index=stable_index)
                cat_uranus_stable = cat_uranus[cat_uranus['stable_index']==1]
                sns.scatterplot(x='fcfasec',y='fcfbeam',hue=cat_uranus_stable.targetname.tolist(),
                                style=cat_uranus_stable.epoch.tolist(),data=cat_uranus_stable)
                z         = np.polyfit(cat_uranus_stable['fcfasec'],cat_uranus_stable['fcfbeam'],1)
                slope     = z[0]
                intercept = z[1]
                x_for_fit = np.linspace(min(cat_uranus_stable['fcfasec']),max(cat_uranus_stable['fcfasec']),1000)
                plt.plot(x_for_fit,slope*x_for_fit+intercept,color='k',linestyle='dashed',linewidth=2)
                plt.suptitle('450 microns Uranus Empirical Beamwidth = {}", Expected = {} $\pm$ {}"'.format(
                    round(np.sqrt(slope/(np.pi/(4*np.log(2)))),1),10.0,0.6))
                plt.legend(loc='upper left')
                plt.savefig('{}/Empirical_Beam_Uranus_450.png'.format(output_dirname), dpi=300)
                #plt.show()
                plt.clf()
            else:
                print('\n\tSkipping 450 micron Empirical URANUS Beam Info because there are less than 3 Uranus ' +
                      'observations in the stable part of the night (21:00 -- 07:00 HST)\n')
        else:
            print('\n\tSkipping 450 micron Empirical URANUS Beam Info because Uranus is not found in Archimedes File\n')

    if len(cat_850['filter'].to_list()) > 0:
        if 'URANUS' in list(cat_850['targetname']):
            cat_uranus2       = cat_850[cat_850['targetname']=='URANUS']
            stable_index      = []
            for i in cat_uranus2['ut']:
                hour = float(i.split()[-1].split(':')[0])
                if hour >= 7 and hour <17:
                    stable_index.append(1)
                else:
                    stable_index.append(0)
            if len(np.array(stable_index)[np.where(np.array(stable_index)==1)])>2:
                cat_uranus = cat_uranus2.assign(stable_index=stable_index)
                cat_uranus_stable = cat_uranus[cat_uranus['stable_index']==1]
                sns.scatterplot(x='fcfasec',y='fcfbeam',hue=cat_uranus_stable.targetname.tolist(),
                                style=cat_uranus_stable.epoch.tolist(),data=cat_uranus_stable)
                z         = np.polyfit(cat_uranus_stable['fcfasec'],cat_uranus_stable['fcfbeam'],1)
                slope     = z[0]
                intercept = z[1]
                x_for_fit = np.linspace(min(cat_uranus_stable['fcfasec']),max(cat_uranus_stable['fcfasec']),1000)
                plt.plot(x_for_fit,slope*x_for_fit+intercept,color='k',linestyle='dashed',linewidth=2)
                plt.suptitle('850 microns Uranus Empirical Beamwidth = {}", Expected = {} $\pm$ {}"'.format(
                    round(np.sqrt(slope/(np.pi/(4*np.log(2)))),1),14.4,0.3))
                plt.legend(loc='upper left')
                plt.savefig('{}/Empirical_Beam_Uranus_850.png'.format(output_dirname), dpi=300)
                #plt.show()
                plt.clf()
            else:
                print('\n\tSkipping 850 micron Empirical URANUS Beam Info because there are less than 3 Uranus ' +
                      'observations in the stable part of the night (21:00 -- 07:00 HST)\n')
        else:
            print('\n\tSkipping 850 micron Empirical URANUS Beam Info because Uranus is not found in Archimedes File\n')

    # Plot Source Aspect Ratios

    print('\nPlotting FWHM main beam as a function of time (Aspect Ratio Proxy)...\n')

    if len(cat_450['filter'].to_list()) > 0:
        ax_FWHMMAIN_450 = sns.scatterplot(x='date', y='fwhmmain', hue=cat_450.targetname.tolist(),
                                          style=cat_450.epoch.tolist(), data=cat_450)
        ax_FWHMMAIN_450.xaxis.set_major_locator(mdates.MonthLocator(interval=int(round(time_range_months / 10))))
        plt.suptitle('450 $\mu$m - Beam Issues (Aspect Ratio Proxy)')
        plt.ylim(ymax=12)
        plt.xticks(rotation=20)
        plt.savefig('{}/FWHMMAIN_vs_date_450.png'.format(output_dirname), dpi=300)
        #plt.show()
        plt.clf()

    if len(cat_850['filter'].to_list()) > 0:
        ax_FWHMMAIN_850 = sns.scatterplot(x='date', y='fwhmmain', hue=cat_850.targetname.tolist(),
                                          style=cat_850.epoch.tolist(), data=cat_850)
        ax_FWHMMAIN_850.xaxis.set_major_locator(mdates.MonthLocator(interval=int(round(time_range_months / 10))))
        plt.suptitle('850 $\mu$m - Beam Issues (Aspect Ratio Proxy)')
        plt.xticks(rotation=20)
        plt.savefig('{}/FWHMMAIN_vs_date_850.png'.format(output_dirname), dpi=300)
        #plt.show()
        plt.clf()

    # Compare FCF beam and FCF matched filter -- we generally find an ~2% difference between these values

    print('\nPlotting FCF matched filter vs FCF peak...\n')

    if len(cat_450['filter'].to_list()) > 0:
        sns.scatterplot(x='fcfbeam',y='fcfmatch',hue=cat_450.targetname.tolist(),
                        style=cat_450.epoch.tolist(),data=cat_450)
        plt.plot(cat_450['fcfbeam'],cat_450['fcfbeam'],linestyle='dashed',color='k',label='1:1')
        plt.ylabel('FCF Match')
        plt.xlabel('FCF Peak')
        plt.xlim(xmin=0,xmax=1500)
        plt.ylim(ymin=0,ymax=1500)
        plt.suptitle('450 $\mu$m - Matched Filter Versus Peak FCF')
        #plt.show()
        plt.savefig('{}/FCFmatch_vs_FCFPeak_450.png'.format(output_dirname),dpi=300)
        plt.clf()

    if len(cat_850['filter'].to_list()) > 0:
        sns.scatterplot(x='fcfbeam',y='fcfmatch',hue=cat_850.targetname.tolist(),
                        style=cat_850.epoch.tolist(),data=cat_850)
        plt.plot(cat_850['fcfbeam'],cat_850['fcfbeam'],linestyle='dashed',color='k',label='1:1')
        plt.ylabel('FCF Match')
        plt.xlabel('FCF Peak')
        plt.xlim(xmin=300,xmax=900)
        plt.ylim(ymin=300,ymax=900)
        plt.suptitle('850 $\mu$m - Matched Filter Versus Peak FCF')
        #plt.show()
        plt.savefig('{}/FCFmatch_vs_FCFPeak_850.png'.format(output_dirname),dpi=300)
        plt.clf()

    print('\n######################')
    print('              ___            ___')
    print('             /   \          /   \\')
    print('             \_   \        /  __/')
    print('              _\   \      /  /__')
    print('              \___  \____/   __/')
    print('                  \_       _/')
    print('                    | @ @  \_')
    print('                    |        ')
    print('                  _/     /\  ')
    print('                 /o)  (o/\ \_')
    print('Done!            \_____/ /   ')
    print('Thanks, eh?!       \____/    ')
    print('')
    print('Results stored in: {}'.format(output_dirname))
    print('######################\n')


SCUBA2cal('archimedes-results-2019_to_2021_example.csv')
