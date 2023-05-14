data <- read.csv("hackupc_provincies.csv")

data2 <- data[,!names(data) %in% c("summary", "images", "region", "summary", "X", "property_id", "beach_view", "price", "property_type")]
data2$property_type <- as.factor(data2$property_type)
data2$id_prov <- as.factor(data2$id_prov)

library(mltools)
library(data.table)
library(caret)


dummy <- dummyVars(" ~ .", data=df)
newdata <- data.frame(predict(dummy, newdata=data))

newdata <- one_hot(as.data.table(data2))
newdata <- newdata[, !names(newdata) %in% c("property_type_condo_apartment")]

newdata.T
correlations <- cor(newdata$logprice, newdata[-1])

cor(newdata$logprice, newdata$property_type_single_family)
ordered_correlations <- sort(correlations, decreasing = TRUE, index.return=TRUE)

