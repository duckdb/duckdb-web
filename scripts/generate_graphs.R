# generate_graphs.R
# This script creates the performance over time graphs for each of the different benchmarks, and places them in the images/graphs folder

library(RSQLite)
library(ggplot2)
library(ggthemes)
library(grid)

theme <- theme_economist(base_size=16) +
        theme(legend.position = "bottom", legend.direction = "horizontal",
              legend.box = "horizontal",
              legend.key.size = unit(1, "cm"),
              plot.title = element_text(family="Tahoma"),
              text = element_text(family = "Tahoma"),
              axis.title = element_text(size = 20),
			  axis.text = element_text(size=16),
              legend.text = element_text(size = 16),
              legend.title=element_text(face = "bold", size = 16))

con <- dbConnect(SQLite(), "benchmarks.db");
benchmarks <- dbGetQuery(con, "SELECT name, id FROM benchmarks");

for(idx in 1:nrow(benchmarks)) {
	benchmark_name <- benchmarks[[1]][idx];
	benchmark_id <- benchmarks[[2]][idx];
	result <- dbGetQuery(con, paste0("SELECT commits.hash, date, median, timings FROM timings JOIN commits ON commits.hash=timings.hash WHERE benchmark_id=", benchmark_id, " ORDER BY date;"))
	# obtain standard deviation
	# result['sd'] <- as.numeric(lapply(lapply(strsplit(result[[4]], ','), as.numeric), sd))
	# convert to date
	result <- na.omit(result)
	if (nrow(result) == 0) {
		next;
	}
	result[[2]] <- as.Date(result[[2]])

	store_path <- paste0("images/graphs/", benchmark_name, ".png")
	print(store_path)
	png(store_path, width=1024, height=640)
	fill <- "#4271AE"
	line <- "#1F3552"
	print(ggplot(result, aes(x=date, y=median)) + ggtitle(paste0("Benchmark ", benchmark_name)) + xlab('Date') + scale_y_continuous('Median Time (s)', limits=c(0, max(result['median'] * 1.3))) + geom_line(aes(x=date,y=median), size=.5, colour=line) + theme + geom_ribbon(ymin=0, aes(x=date, ymax=median), fill=fill))
	dev.off()
};
