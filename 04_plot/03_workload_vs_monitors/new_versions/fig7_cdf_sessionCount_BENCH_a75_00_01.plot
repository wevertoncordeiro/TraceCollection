unset grid
unset key
set encoding utf8
#set xlabel "Number of users' sessions"
set xlabel "Number of sessions"
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

 
#

my_lw = 3

set style line 3 lt 1  					dashtype 1 pointtype 6 pointsize 2  linewidth my_lw
set style line 4 lt 1 lc rgb '#7e2f8e' 	dashtype 3 pointtype 7 pointsize 1  linewidth my_lw 

set style line 5 lt 2 lc rgb '#87bf77'	dashtype 1 pointtype 8 pointsize 1  linewidth my_lw
set style line 6 lt 2  					dashtype 3 pointtype 9 pointsize 1  linewidth my_lw

set style line 1 lt 3  					dashtype 1 pointtype 4 pointsize 1  linewidth my_lw
set style line 2 lt 3  lc rgb '#352a87' dashtype 3 pointtype 5 pointsize 1  linewidth my_lw +1

set style line 7 lt 3  lc rgb '#d95319' dashtype 1 pointtype 12 pointsize 1 linewidth my_lw 
set style line 8 lt 8  lc rgb '#a2142f' dashtype 3  pointtype 13 pointsize 1 linewidth my_lw


#set pointintervalbox 3

set yrange [.5:] #janela de 50
set xrange [0:500] #janela de 300

 
#set key on outside top horizontal maxrows 5  invert
#set key on inside bottom right horizontal maxrows 4  invert
#set key on inside bottom right 
#set key samplen 1
#set key reverse

set key at 1,1 horizontal maxrows 3 

set term postscript eps enhanced color "Helvetica" 24 lw 2 size 8, 3.5 #inches (default values are 5, 3.5)
#set term png "Helvetica" 24 lw 2 size 8, 3.5 #inches (default values are 5, 3.5)
set output "fig7_cdf_sessionCount_BENCH_a75_00_01.eps"  


set style arrow 1 head filled #ls 3 #size screen 0.03,15,5 ls 3
set multiplot# layout 1,2
  

### First plot


set arrow from 130,.78 to 130,.96 as 1
set label "gain" at 135,.86

set lmargin at screen 0.100
set rmargin at screen 0.500

set tmargin at screen 0.80
set bmargin at screen 0.20

set label at screen 0.300,0.04 center  "(a) S1" #font "Times"
set label at screen 0.750,0.04 center  "(b) S2" #font "Times"



unset key

 
plot \
'04_plot/01_evaluation/00_data/session_countcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-025.txt' using 2:1 title 'In p_{if}=.25' with l ls 7 ,\
'04_plot/01_evaluation/00_data/session_countcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-020.txt' using 2:1 title 'In p_{if}=.20' with l ls 5 ,\
'04_plot/01_evaluation/00_data/session_countcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-015.txt' using 2:1 title 'In p_{if}=.15' with l ls 3 ,\
'04_plot/01_evaluation/00_data/session_countcdf_00_Collection_SNAP_ORIGINAL_RES-100_FAIL-000.txt' using 2:1 title 'In Original' with l ls 1 ,\
'04_plot/01_evaluation/00_data/session_countcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-025_ALP-075.txt' using 2:1 title 'Out p_{if}=.25 {/Symbol a}=.75' with l ls 8 ,\
'04_plot/01_evaluation/00_data/session_countcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-020_ALP-075.txt' using 2:1 title 'Out p_{if}=.20 {/Symbol a}=.75' with l ls 6 ,\
'04_plot/01_evaluation/00_data/session_countcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-015_ALP-075.txt' using 2:1 title 'Out p_{if}=.15 {/Symbol a}=.75' with l ls 4 ,\
'04_plot/01_evaluation/00_data/session_countcdf_00_Collection_SNAP_CORRECTED_RES-100_FAIL-000_ALP-075.txt' using 2:1 title 'Out Original {/Symbol a}=.75' with l ls 2,  

unset arrow
unset label

 
### Second plot
set lmargin at screen 0.550
set rmargin at screen 0.950


unset ylabel
unset ytics

set arrow from 90,.8 to 90,.93 as 1
set label "gain" at 95,.88 

plot  \
'04_plot/01_evaluation/00_data/session_countcdf_01_Aerofly_SNAP_ORIGINAL_RES-100_FAIL-025.txt' using 2:1 title 'In p_{if}=.25' with l ls 7 , \
'04_plot/01_evaluation/00_data/session_countcdf_01_Aerofly_SNAP_ORIGINAL_RES-100_FAIL-020.txt' using 2:1 title 'In p_{if}=.20' with l ls 5 , \
'04_plot/01_evaluation/00_data/session_countcdf_01_Aerofly_SNAP_ORIGINAL_RES-100_FAIL-015.txt' using 2:1 title 'In p_{if}=.15' with l ls 3 , \
'04_plot/01_evaluation/00_data/session_countcdf_01_Aerofly_SNAP_ORIGINAL_RES-100_FAIL-000.txt' using 2:1 title 'In Original' with l ls 1 ,   \
'04_plot/01_evaluation/00_data/session_countcdf_01_Aerofly_SNAP_CORRECTED_RES-100_FAIL-025_ALP-075.txt' using 2:1 title 'Out p_{if}=.25 {/Symbol a}=.75' with l ls 8 , \
'04_plot/01_evaluation/00_data/session_countcdf_01_Aerofly_SNAP_CORRECTED_RES-100_FAIL-020_ALP-075.txt' using 2:1 title 'Out p_{if}=.20 {/Symbol a}=.75' with l ls 6 , \
'04_plot/01_evaluation/00_data/session_countcdf_01_Aerofly_SNAP_CORRECTED_RES-100_FAIL-015_ALP-075.txt' using 2:1 title 'Out p_{if}=.15 {/Symbol a}=.75' with l ls 4 , \
'04_plot/01_evaluation/00_data/session_countcdf_01_Aerofly_SNAP_CORRECTED_RES-100_FAIL-000_ALP-075.txt' using 2:1 title 'Out Original {/Symbol a}=.75' with l ls 2,  

unset arrow
unset label

### Last (key) plot
#set tmargin at screen bot(n,n,h,t,b)
#set bmargin at screen 0
#set key center center
set border 0
unset tics
unset xlabel
unset ylabel
set yrange [0:1]

#set key Left width .01

set key at screen 0.31,.95 maxcolumns 1

plot \
2 t 'Input trace: Original' with l ls 1, \
2 t 'Corrected trace {/Symbol a}=.75: Original' with l ls 2

set key at screen 0.58,.95 maxcolumns 1
plot \
2 t 'p_{if}=.15' with l ls 3, \
2 t 'p_{if}=.15' with l ls 4

set key at screen 0.79,.95 maxcolumns 1
plot \
2 t 'p_{if}=.20' with l ls 5, \
2 t 'p_{if}=.20' with l ls 6


set key at screen .99,.95 maxcolumns 1
plot \
2 t 'p_{if}=.25' with l ls 7, \
2 t 'p_{if}=.25' with l ls 8


