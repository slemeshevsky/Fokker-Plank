set terminal postscript eps enhanced
set output "result.ps"
plot 'rangedata.txt' title 'SRIM' with linespoints lt rgb 'black', \
	 '1Ddata.txt' title '1D' with lines lt rgb 'green', \
	 '2Ddata.txt' title '2D' with lines lt rgb 'blue'