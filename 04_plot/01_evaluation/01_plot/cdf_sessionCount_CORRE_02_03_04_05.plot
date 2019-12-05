unset grid
unset key
set encoding utf8
set xlabel "Number of users' sessions"
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




set style line 1 lt 1 lc rgb '#7e2f8e'  pointtype 6 pointsize 2  ##
set style line 2 lt 2 lc rgb '#87bf77'	pointtype 3 pointsize 1  
set style line 3 lt 3 lc rgb '#4dbeee'  pointtype 2 pointsize 1  
set style line 4 lt 4 lc rgb '#d95319' 	pointtype 1 pointsize 1   
set style line 5 lt 5 lc rgb '#d9ba56' 	pointtype 7 pointsize 1   

set style line 6 lt 6 lc rgb '#a2142f' 	pointtype 4 pointsize 1   
set style line 7 lt 7 lc rgb '#0072bd' 	pointtype 9 pointsize 1   








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
set xrange [0:500] #janela de 300

 
#set key on outside top horizontal maxrows 5  invert
#set key on inside bottom right horizontal maxrows 4  invert
#set key on inside bottom right 
#set key samplen 1
#set key reverse

set key at 1,1 horizontal maxrows 3 

set term postscript eps enhanced color "Helvetica" 24 lw 2 size 16, 3.5 #inches (default values are 5, 3.5)
set output "04_plot/01_evaluation/cdf_sessionCount_CORRE_02_03_04_05.eps"  

set multiplot
 
### First plot
set lmargin at screen 0.060
set rmargin at screen 0.275 

set tmargin at screen 0.90
set bmargin at screen 0.20

set label at screen 0.167,0.03 center  "(a) S3" #font "Times"
set label at screen 0.402,0.03 center  "(b) S4" #font "Times"
set label at screen 0.637,0.03 center  "(c) S5" #font "Times"
set label at screen 0.872,0.03 center  "(d) S6" #font "Times"

unset key

#S3
plot \
'04_plot/01_evaluation/00_data/session_countcdf_03_Happytime_SNAP_ORIGINAL_RES-100_FAIL-000.txt'          using 2:1 title 'In Original' with lp ls 1 ,\
'04_plot/01_evaluation/00_data/session_countcdf_03_Happytime_SNAP_CORRECTED_RES-100_FAIL-000_ALP-060.txt' using 2:1 title 'Out {/Symbol a}=.60' with lp ls 2,\
'04_plot/01_evaluation/00_data/session_countcdf_03_Happytime_SNAP_CORRECTED_RES-100_FAIL-000_ALP-075.txt' using 2:1 title 'Out {/Symbol a}=.75' with lp ls 3,\
'04_plot/01_evaluation/00_data/session_countcdf_03_Happytime_SNAP_CORRECTED_RES-100_FAIL-000_ALP-085.txt' using 2:1 title 'Out {/Symbol a}=.85' with lp ls 4,\
'04_plot/01_evaluation/00_data/session_countcdf_03_Happytime_SNAP_CORRECTED_RES-100_FAIL-000_ALP-095.txt' using 2:1 title 'Out {/Symbol a}=.95' with lp ls 5



### Second plot
set lmargin at screen 0.295
set rmargin at screen 0.510

unset ylabel
unset ytics

#S4
plot \
'04_plot/01_evaluation/00_data/session_countcdf_02_Increibles_SNAP_ORIGINAL_RES-100_FAIL-000.txt' using 2:1 title 'In Original' with lp ls 1 ,\
'04_plot/01_evaluation/00_data/session_countcdf_02_Increibles_SNAP_CORRECTED_RES-100_FAIL-000_ALP-060.txt' using 2:1 title 'Out {/Symbol a}=.60' with lp ls 2,\
'04_plot/01_evaluation/00_data/session_countcdf_02_Increibles_SNAP_CORRECTED_RES-100_FAIL-000_ALP-075.txt' using 2:1 title 'Out {/Symbol a}=.75' with lp ls 3,\
'04_plot/01_evaluation/00_data/session_countcdf_02_Increibles_SNAP_CORRECTED_RES-100_FAIL-000_ALP-085.txt' using 2:1 title 'Out {/Symbol a}=.85' with lp ls 4,\
'04_plot/01_evaluation/00_data/session_countcdf_02_Increibles_SNAP_CORRECTED_RES-100_FAIL-000_ALP-095.txt' using 2:1 title 'Out {/Symbol a}=.95' with lp ls 5



### Third plot
set lmargin at screen 0.530
set rmargin at screen 0.745

#S5
plot \
'04_plot/01_evaluation/00_data/session_countcdf_05_Mission_SNAP_ORIGINAL_RES-100_FAIL-000.txt' using 2:1 title 'In Original' with lp ls 1 ,\
'04_plot/01_evaluation/00_data/session_countcdf_05_Mission_SNAP_CORRECTED_RES-100_FAIL-000_ALP-060.txt' using 2:1 title 'Out {/Symbol a}=.60' with lp ls 2,\
'04_plot/01_evaluation/00_data/session_countcdf_05_Mission_SNAP_CORRECTED_RES-100_FAIL-000_ALP-075.txt' using 2:1 title 'Out {/Symbol a}=.75' with lp ls 3,\
'04_plot/01_evaluation/00_data/session_countcdf_05_Mission_SNAP_CORRECTED_RES-100_FAIL-000_ALP-085.txt' using 2:1 title 'Out {/Symbol a}=.85' with lp ls 4,\
'04_plot/01_evaluation/00_data/session_countcdf_05_Mission_SNAP_CORRECTED_RES-100_FAIL-000_ALP-095.txt' using 2:1 title 'Out {/Symbol a}=.95' with lp ls 5


### Fourth plot
set lmargin at screen 0.765
set rmargin at screen 0.980

#S6
plot \
'04_plot/01_evaluation/00_data/session_countcdf_04_Star_SNAP_ORIGINAL_RES-100_FAIL-000.txt' using 2:1 title 'In Original' with lp ls 1 ,\
'04_plot/01_evaluation/00_data/session_countcdf_04_Star_SNAP_CORRECTED_RES-100_FAIL-000_ALP-060.txt' using 2:1 title 'Out {/Symbol a}=.60' with lp ls 2,\
'04_plot/01_evaluation/00_data/session_countcdf_04_Star_SNAP_CORRECTED_RES-100_FAIL-000_ALP-075.txt' using 2:1 title 'Out {/Symbol a}=.75' with lp ls 3,\
'04_plot/01_evaluation/00_data/session_countcdf_04_Star_SNAP_CORRECTED_RES-100_FAIL-000_ALP-085.txt' using 2:1 title 'Out {/Symbol a}=.85' with lp ls 4,\
'04_plot/01_evaluation/00_data/session_countcdf_04_Star_SNAP_CORRECTED_RES-100_FAIL-000_ALP-095.txt' using 2:1 title 'Out {/Symbol a}=.95' with lp ls 5



### Last (key) plot
#set tmargin at screen bot(n,n,h,t,b)
#set bmargin at screen 0
#set key center center
set border 0
unset tics
unset xlabel
unset ylabel
set yrange [0:1]

set key at screen 0.20,0.975 maxrow 1

plot \
2 t 'In Original' with lp ls 1

set key at screen 0.35,0.975 maxrow 1
plot \
2 t 'Out {/Symbol a}=.60' with lp ls 2

set key at screen 0.50,0.975 maxrow 1
plot \
2 t 'Out {/Symbol a}=.75' with lp ls 3

set key at screen 0.65,0.975 maxrow 1
plot \
2 t 'Out {/Symbol a}=.85' with lp ls 4

set key at screen 0.80,0.975 maxrow 1
plot \
2 t 'Out {/Symbol a}=.95' with lp ls 5

 



