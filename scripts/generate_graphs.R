library(RSQLite)
library(ggplot2)
library(ggthemes)

theme <- theme_few(base_size = 24) +
theme(axis.title.y=element_text(vjust=0.9),
  axis.title.x=element_text(vjust=-0.1),
  axis.ticks.x=element_blank(),
  text=element_text(family="serif"))

con <- dbConnect(SQLite(), "benchmarks.db");
benchmarks <- dbGetQuery(con, "SELECT name, id FROM benchmarks");

for(idx in 1:nrow(benchmarks)) {
	benchmark_name <- benchmarks[[1]][idx];
	benchmark_id <- benchmarks[[2]][idx];
	result <- dbGetQuery(con, paste0("SELECT commits.hash, date, median FROM timings JOIN commits ON commits.hash=timings.hash WHERE benchmark_id=", benchmark_id, " ORDER BY date;"))
	result[[2]] <- as.Date(result[[2]])

	store_path <- paste0("images/graphs/", benchmark_name, ".png")
	print(store_path)
	png(store_path, width=1024, height=640)
	print(qplot(x=date, y=median, data=result, na.rm=TRUE, main=paste0("Benchmark ", benchmark_name), xlab="Date", ylab="Median Time (s)") + geom_line() + ylim(0,max(result['median'])) + theme)
	dev.off()
};
