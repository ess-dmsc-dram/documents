import math


import matplotlib.pyplot as plt


if "ws" not in mtd:
    ws = Load(Filename='/home/anton/builds/Mantid2_QtCreator/ExternalData/Testing/Data/SystemTest/TOPAZ_3132_event.nxs')
else:
    ws = mtd["ws"]

# ------------------------------------------
# Get a n-percent file
# -----------------------------------------
def create_n_percent_workspace(workspace, fraction):
    run = workspace.run()

    # Determine the absolute filter times
    start_time  = run.startTime()
    end_time = run.endTime()
    duration = end_time - start_time
    total_duration = duration.total_nanoseconds()
    reduced_duration = total_duration*fraction
    cut_off_time = start_time + int(reduced_duration)

    # Filter by time
    #filtered = FilterByTime(InputWorkspace=workspace,AbsoluteStartTime=str(start_time), AbsoluteStopTime=str(cut_off_time))

    total_duration = duration.total_seconds()
    reduced_duration = total_duration*fraction
    filtered = FilterByTime(InputWorkspace=workspace,StartTime=0.,  StopTime=reduced_duration)
    return filtered

# ---------------------------------
# Create 1% filtering
# ---------------------------------

def create_deviation_plots(ws, fractions):
    number_of_plots = len(fractions) if len(fractions)  > 0 else len(fractions) + 1

    plt.close("all")
    f, axarr = plt.subplots(number_of_plots, 2, sharex='col')
    for index, fraction in enumerate(fractions):
        ws_filter = create_n_percent_workspace(ws, fraction)
        # ------------------------------------------------------------
        # Convert the small data set to MD
        # ------------------------------------------------------------
        md_ws_filter = ConvertToMD(InputWorkspace=ws_filter, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', LorentzCorrection='1', MinValues='-25,-25,-25', MaxValues='25,25,25', SplitInto='2', SplitThreshold='50', MaxRecursionDepth='13')
        bc = md_ws_filter.getBoxController()

        # ------------------------------------------------------------
        # Convert the large data set to MD
        # ------------------------------------------------------------
        if not "md_ws" in mtd:
            md_ws = ConvertToMD(InputWorkspace=ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', LorentzCorrection='1',
                                                           MinValues='-25,-25,-25', MaxValues='25,25,25', SplitInto='2', SplitThreshold='50', MaxRecursionDepth='13')
        else:
            md_ws = mtd["md_ws"]

        # --------------------------
        # Bin Comparison
        # -------------------------
        # Assuming 10^3 ranks, ie we bin by 10 in each direction.
        dimensioning = 20
        binned_ws_filter = BinMD(InputWorkspace=md_ws_filter,
                                                            AlignedDim0='Q_sample_x,-25,25,{}'.format(dimensioning),
                                                            AlignedDim1='Q_sample_y,-25,25,{}'.format(dimensioning),
                                                            AlignedDim2='Q_sample_z,-25,25,{}'.format(dimensioning),
                                                            Parallel=True)
        binned_ws = BinMD(InputWorkspace=md_ws,
                                                AlignedDim0='Q_sample_x,-25,25,{}'.format(dimensioning),
                                                AlignedDim1='Q_sample_y,-25,25,{}'.format(dimensioning),
                                                AlignedDim2='Q_sample_z,-25,25,{}'.format(dimensioning),
                                                Parallel=True)

        arr_filter = binned_ws_filter.getNumEventsArray()
        arr =  binned_ws.getNumEventsArray()

        # Data to be filled
        relative_deviation = []
        relative_deviation_outlier = []
        absolute_deviation = []
        absolute_deviation_outlier  = []


        # Extract outliers for relative deviation
        compare_outlier = lambda x: x>100 or x < -100
        outlier_more_than_100_percent = []
        deviation_no_outlier = []


         # Extract outliers for absolute deviation
        average_count_in_bin = ws.getNumberEvents()/dimensioning**3
        number_of_events = ws.getNumberEvents()
        compare_outlier_absolute = lambda x: x>1


        for dim0 in range(dimensioning):
            for dim1 in range(dimensioning):
                for dim2 in range(dimensioning):
                    value = arr[dim0, dim1, dim2]
                    value_filter = arr_filter[dim0, dim1, dim2]
                    if value != 0. and value_filter != 0.:
                        # Get the realtive deviation
                        rel_dev = ((value-value_filter/fraction)/value)*100

                         #Get the absolute deviation
                        abs_dev = math.fabs(value-value_filter/fraction)
                        abs_dev = abs_dev/average_count_in_bin


                        # If the data points differ by more than 100%, and the

                        # and the deviation is larger than 100% of the value is larger than 10% of the average bin count
                        # then we are dealing with an outlier, else we have small-count effects
                        # We still need to look at the absolute deviation. If this is smaller than 1, then
                        # we don't have an outlier
                        if compare_outlier(rel_dev) and value >average_count_in_bin*0.1 and abs_dev > 1:
                            relative_deviation_outlier.append(rel_dev)
                            absolute_deviation_outlier.append(abs_dev)
                        else:
                            # Now we discard all those entries which are not outliers but appear as outliers
                            if not compare_outlier(rel_dev):
                                relative_deviation.append(rel_dev)
                            if abs_dev < 1:
                                absolute_deviation.append(abs_dev)


        axarr[index, 0].hist(relative_deviation, 100, normed=1, facecolor='green', alpha=0.75)
        axarr[index, 0].set_xlim([-110, 110])
        axarr[index, 0].set_ylim([0, 0.2])
        axarr[index, 0].set_xlabel('Rel. Dev. in %')
        axarr[index, 0].set_ylabel("Dist. for {} %".format(fraction*100))
        axarr[index, 0].grid(color='r')

        #axarr[index, 1].hist(relative_deviation_outlier, 100, normed=1, facecolor='green', alpha=0.75)
        #axarr[index, 1].set_xlabel('Rel. Dev.  outliers in %')
        #axarr[index, 1].set_ylabel("Dist. for {} %".format(fraction*100))
        #axarr[index, 1].grid(color='r')

        axarr[index, 1].hist(absolute_deviation, 100, normed=1, facecolor='green', alpha=0.75)
        axarr[index, 1].set_xlim([0, 1])
        axarr[index, 1].set_xlabel('Deviation counts / avg. counts in bin')
        axarr[index, 1].set_ylabel("Abs. Dev.  for {} %".format(fraction*100))
        axarr[index, 1].grid(color='r')

        #axarr[index, 3].hist(absolute_deviation_outlier, 100, normed=1, facecolor='green', alpha=0.75)
        ###axarr[index, 0].set_xlim([-110, 110])
        ###axarr[index, 0].set_ylim([0, 0.2])
        #axarr[index, 3].set_xlabel('Deviation counts / avg. counts in bin')
        #axarr[index, 3].set_ylabel("Abs. Dev.  for {} %".format(fraction*100))
        #axarr[index, 3].grid(color='r')
    plt.show()

#create_deviation_plots(ws, [0.01])
create_deviation_plots(ws, [0.01, 0.05, 0.1, 0.4, 0.7])
