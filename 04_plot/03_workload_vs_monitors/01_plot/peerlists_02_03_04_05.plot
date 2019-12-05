unset grid
unset key
set encoding utf8
 
set ylabel "Number of Peer Lists"


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


set style line 1 lt 1  					pointtype 6 pointsize 2  ##
set style line 2 lt 1 lc rgb '#7e2f8e' 	pointtype 1 pointsize 1   

set style line 3 lt 3  lc rgb '#d95319' pointtype 12 pointsize 1   
set style line 4 lt 3  lc rgb '#4dbeee' pointtype 2 pointsize 1  

set style line 5 lt 2 lc rgb '#87bf77'	pointtype 8 pointsize 1  
set style line 6 lt 2  					pointtype 3 pointsize 1  

set style line 7 lt 3  lc rgb '#d95319' pointtype 12 pointsize 2   
set style line 8 lt 3  lc rgb '#a2142f' pointtype 13 pointsize 1  



set key samplen 1
set style line 1 lt 2 lc rgb '#7e2f8e' pointtype 2 pointsize 1  
set style line 2 lt 3 lc rgb '#87bf77' pointtype 3 pointsize 1 
set style line 3 lt 1 lc rgb '#4dbeee' pointtype 1 pointsize 1 

##1-Window 2-avg_peers 3-std_peers 4-replied_queries 5-required_queries_avg_LNUMWANT 6-monitors 7-obtained_peers 8-min_peers 9-max_peers 10-sum_peer 11-required_queries_max_LNUMWANT 12-required_queries_sum_LNUMWANT 13-peers_uniques 14-required_queries_sum_avg_peers 15-obtained_monitors 16-obtained_sentinels 17-required_queries_max_avg_peers 18-required_queries_unique_peers_avg_peers 19-required_queries_avg_L200 20-required_queries_max_L200 21-required_queries_sum_L200  22-obtained_peers_avg 23-obtained_peers_std

set term postscript eps enhanced color "Helvetica" 24 lw 2


set xlabel "Sampling No."
set format x "%.sK"
#set format y "%.sK"

#set xrange [0:7200] # 2.5 months (ground truth)
#set xrange [0:75] # 2.5 months in days (ground truth)

set xrange [0:17280] # 6.0 months in samplings (case study)
#set xrange [0:180] # 6.0 months in days (case study)
#set xrange [0:6] # 6.0 months (case study)

set yrange [0:1000]

 

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

#set xrange[0:100]

set key at 1,1 horizontal maxrows 3 

set term postscript eps enhanced color "Helvetica" 24 lw 2 size 16, 3.5 #inches (default values are 5, 3.5)
set output "04_plot/03_workload_vs_monitors/peerlists_02_03_04_05.eps"

set multiplot 
 
 
### First plot
set lmargin at screen 0.060
set rmargin at screen 0.260 

set tmargin at screen 0.90
set bmargin at screen 0.20

set label at screen 0.160,0.03 center "(a) S3" #font "Times"
set label at screen 0.380,0.03 center "(b) S4" #font "Times"
set label at screen 0.670,0.03 center "(c) S5" #font "Times"
set label at screen 0.890,0.03 center "(d) S6" #font "Times"

unset key

#S3
plot \
'04_plot/03_workload_vs_monitors/00_data/03_Happytime_RES-100.txt' using ($1):4  title 'Collected Peer Lists' with p ls 1, \
'04_plot/03_workload_vs_monitors/00_data/03_Happytime_RES-100.txt' using ($1):21 title 'Est. Req., N=(Sum), L=200' with p ls 2, \
'04_plot/03_workload_vs_monitors/00_data/03_Happytime_RES-100.txt' using ($1):20 title 'Est. Req., N=(Max), L=200' with p ls 3
 


### Second plot
set lmargin at screen 0.280
set rmargin at screen 0.480

unset ylabel
unset ytics

#S4
plot \
'04_plot/03_workload_vs_monitors/00_data/02_Increibles_RES-100.txt' using ($1):4  title 'Collected Peer Lists' with p ls 1, \
'04_plot/03_workload_vs_monitors/00_data/02_Increibles_RES-100.txt' using ($1):21 title 'Est. Req., N=(Sum), L=200' with p ls 2, \
'04_plot/03_workload_vs_monitors/00_data/02_Increibles_RES-100.txt' using ($1):20 title 'Est. Req., N=(Max), L=200' with p ls 3
 

### Third plot
set yrange [0:3000]
set lmargin at screen 0.570
set rmargin at screen 0.770

set ylabel "Number of Peer Lists"
set ytics

#S5
plot \
'04_plot/03_workload_vs_monitors/00_data/05_Mission_RES-100.txt' using ($1):4  title 'Collected Peer Lists' with p ls 1, \
'04_plot/03_workload_vs_monitors/00_data/05_Mission_RES-100.txt' using ($1):21 title 'Est. Req., N=(Sum), L=200' with p ls 2, \
'04_plot/03_workload_vs_monitors/00_data/05_Mission_RES-100.txt' using ($1):20 title 'Est. Req., N=(Max), L=200' with p ls 3
 




### Fourth plot
set lmargin at screen 0.790
set rmargin at screen 0.990

unset ylabel
unset ytics

#S6
plot \
'04_plot/03_workload_vs_monitors/00_data/04_Star_RES-100.txt' using ($1):4  title 'Collected Peer Lists' with p ls 1, \
'04_plot/03_workload_vs_monitors/00_data/04_Star_RES-100.txt' using ($1):21 title 'Est. Req., N=(Sum), L=200' with p ls 2, \
'04_plot/03_workload_vs_monitors/00_data/04_Star_RES-100.txt' using ($1):20 title 'Est. Req., N=(Max), L=200' with p ls 3
 


### Last (key) plots

set border 0
unset tics
unset xlabel
unset ylabel
set yrange [0:1]
 
set key at screen 0.20,.975 maxrows 1
plot \
2 title 'Collected Peer Lists' with p ls 1


set key at screen 0.40,.975  maxrows 1
plot \
2 title 'Est. Req., N=(Sum), L=200' with p ls 2


set key at screen 0.60,.975  maxrows 1
plot \
2 title 'Est. Req., N=(Max), L=200' with p ls 3

