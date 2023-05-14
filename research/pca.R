setwd("C:/Users/aairu/Desktop/HACKUPC")
library(FactoMineR)
library(corrplot)
library(mltools)
library(data.table)

hackupc <- read.csv("hackupc_provicies_.csv", header = TRUE)
hackupc <- hackupc[, -1]

hackupc$id_prov <- as.factor(hackupc$id_prov)
newdata <- one_hot(as.data.table(hackupc))

hackupc <- newdata
head(hackupc)
str(hackupc) 

pca <- PCA(hackupc, quanti.sup=which(names(hackupc)=="logprice"), scale.unit = TRUE)
pca$eig
pca$var$cor

prop_varex <- pca$svd$vs^2/sum(pca$svd$vs^2)
barplot(prop_varex, xlab = "Principal Component", ylab = "Proportion of Variance Explained")
lines(prop_varex, type="b", pch=20)
axis(1, at = 1:180)

corrplot((pca$var$cor), tl="null")

plot.PCA(pca, axes=c(1,2), choix='ind', cex = 0)

num <- hackupc_pca
num$region <- NULL
num$property_type <- NULL

# corrplot(cor(num), tl.col = "black")

var_coord <- pca$var$coord
coords <- rbind(var_coord, pca$quanti.sup$coord)
df_var_coord <- data.frame(coords)
write.csv(df_var_coord, file = "var_coord.csv", row.names = FALSE)

coords <- as.data.frame(coords)
response <- tail(coords, n = 1)
predictors <- coord$logprice <- NULL

# Create a linear regression model
lm_model <- lm(response ~ ., data = predictors)

# Print the summary of the linear regression model
summary(lm_model)