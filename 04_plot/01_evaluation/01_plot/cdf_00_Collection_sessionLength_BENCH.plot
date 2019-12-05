# File generated by analyze4_evaluate_trace.py on 2019-10-06 00:42:50.824693
unset grid
unset key
set xlabel "Duration of users' sessions"
set ylabel "CDF"

# line styles
set style line  1 lt 1 lc rgb '#352a87' # blue
set style line  2 lt 1 lc rgb '#0f5cdd' # blue
set style line  3 lt 1 lc rgb '#1481d6' # blue
set style line  4 lt 1 lc rgb '#06a4ca' # cyan
set style line  5 lt 1 lc rgb '#2eb7a4' # green
set style line  6 lt 1 lc rgb '#87bf77' # green
set style line  7 lt 1 lc rgb '#d1bb59' # orange
set style line  8 lt 1 lc rgb '#fec832' # orange
set style line  9 lt 1 lc rgb '#f9fb0e' # yellow

# New default Matlab line colors, introduced together with parula (2014b)
set style line 11 lt 1 lc rgb '#0072bd' # blue
set style line 12 lt 1 lc rgb '#d95319' # orange
set style line 13 lt 1 lc rgb '#edb120' # yellow
set style line 14 lt 1 lc rgb '#7e2f8e' # purple
set style line 15 lt 1 lc rgb '#77ac30' # green
set style line 16 lt 1 lc rgb '#4dbeee' # light-blue
set style line 17 lt 1 lc rgb '#a2142f' # red



set style line 1 lt 1  					pointtype 6 pointsize 2  
set style line 2 lt 1 lc rgb '#7e2f8e' 	pointtype 7 pointsize 1   

set style line 3 lt 2 lc rgb '#87bf77'	pointtype 8 pointsize 1  
set style line 4 lt 2  					pointtype 9 pointsize 1  

set style line 5 lt 3  					pointtype 4 pointsize 1  
set style line 6 lt 3  lc rgb '#352a87' pointtype 5 pointsize 1 

set style line 7 lt 3  lc rgb '#d95319' pointtype 12 pointsize 1   
set style line 8 lt 3  lc rgb '#a2142f' pointtype 13 pointsize 1  

 

# palette
set palette defined (\
0 '#352a87',\
1 '#0363e1',\
2 '#1485d4',\
3 '#06a7c6',\
4 '#38b99e',\
5 '#92bf73',\
6 '#d9ba56',\
7 '#fcce2e',\
8 '#f9fb0e')

 
#set pointintervalbox 3

set yrange [.5:] #janela de 50
set xrange [0:100] #janela de 300

set term postscript eps enhanced color "Helvetica" 24 lw 2


set termoption enhanced

#set key on outside top horizontal maxrows 4  invert
set key on inside bottom right horizontal maxrows 4 invert
#set key on outside top right horizontal maxrows 4  invert
set key samplen 1
#set key reverse



#set output "04_plot/01_evaluation/cdf_00_Collection_sessionLength_BENCH_alpha-090.eps"

#plot                                                                                                       '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-075.txt' using 2:1 title 'In p_{if}=.75' with lp ls 5 , '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-050.txt' using 2:1 title 'In p_{if}=.50' with lp ls 7 ,   '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-025.txt' using 2:1 title 'In p_{if}=.25' with lp ls 3 ,                          '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-000.txt' using 2:1 title 'In Original' with lp ls 1 ,  '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-075_ALP-090.txt' using 2:1 title 'Out p_{if}=.75 {/Symbol a}=.90' with lp ls 6, '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-050_ALP-090.txt' using 2:1 title 'Out p_{if}=.50 {/Symbol a}=.90' with lp ls 8,   '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-025_ALP-090.txt' using 2:1 title 'Out p_{if}=.25 {/Symbol a}=.90' with lp ls 4,   '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-000_ALP-090.txt' using 2:1 title 'Out Original {/Symbol a}=.90' with lp ls 2,  

#set output "04_plot/01_evaluation/03_png/cdf_00_Collection_sessionLength_BENCH_alpha-090.png"
#set term png
#replot




#set output "04_plot/01_evaluation/cdf_00_Collection_sessionLength_BENCH_alpha-070.eps"

#plot                                                                                                       '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-010.txt' using 2:1 title 'In p_{if}=.10' with lp ls 5 , '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-050.txt' using 2:1 title 'In p_{if}=.50' with lp ls 7 ,   '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-025.txt' using 2:1 title 'In p_{if}=.25' with lp ls 3 ,                          '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-000.txt' using 2:1 title 'In Original' with lp ls 1 ,  '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-010_ALP-070.txt' using 2:1 title 'Out p_{if}=.10 {/Symbol a}=.70' with lp ls 6, '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-050_ALP-070.txt' using 2:1 title 'Out p_{if}=.50 {/Symbol a}=.70' with lp ls 8,   '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-025_ALP-070.txt' using 2:1 title 'Out p_{if}=.25 {/Symbol a}=.70' with lp ls 4,   '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-000_ALP-070.txt' using 2:1 title 'Out Original {/Symbol a}=.70' with lp ls 2,  

#set output "04_plot/01_evaluation/03_png/cdf_00_Collection_sessionLength_BENCH_alpha-070.png"
#set term png
#replot


set output "04_plot/01_evaluation/cdf_00_Collection_sessionLength_BENCH_alpha-075.eps"

plot                                                                                                       '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-025.txt' using 2:1 title "In p_{if}=.25" with lp ls 7 , '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-020.txt' using 2:1 title "In p_{if}=.20" with lp ls 5 ,   '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-015.txt' using 2:1 title "In p_{if}=.15" with lp ls 3 ,                          '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-000.txt' using 2:1 title "In Original" with lp ls 1 ,  '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-025_ALP-075.txt' using 2:1 title "Out p_{if}=.25 {/Symbol a}=.75" with lp ls 8, '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-020_ALP-075.txt' using 2:1 title "Out p_{if}=.20 {/Symbol a}=.75" with lp ls 6,   '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-015_ALP-075.txt' using 2:1 title "Out p_{if}=.15 {/Symbol a}=.75" with lp ls 4,   '04_plot/01_evaluation/00_data/session_lengthcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-000_ALP-075.txt' using 2:1 title "Out Original {/Symbol a}=.75" with lp ls 2,  

set output "04_plot/01_evaluation/03_png/cdf_00_Collection_sessionLength_BENCH_alpha-075.png"
set term png
replot





