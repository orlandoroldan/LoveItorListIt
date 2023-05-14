% Analysis of correlations between variables
% We use the dataframe that includes the information about the location of the properties


library(mltools)
library(data.table)
library(caret)

data <- read.csv("hackupc_provincies.csv")

data2 <- data[,!names(data) %in% c("summary", "images", "region", "summary", "X", "property_id", "beach_view", "price", "property_type")]

data2$property_type <- as.factor(data2$property_type)
data2$id_prov <- as.factor(data2$id_prov)

newdata <- as.data.frame(one_hot(as.data.table(data2)))
newdata <- newdata[, !names(newdata) %in% c("property_type_condo_apartment")]

newdata.T
correlations <- cor(newdata$logprice, newdata[-1])
ordered_correlations <- sort(correlations, decreasing = TRUE, index.return=TRUE)

