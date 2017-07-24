
## Headphone ##
require(foreign)
require(ggplot2)
require(MASS)
require(Hmisc)
require(reshape2)
library(caret)
library(readxl)
headphone <- read_excel("C:/Users/chen/PycharmProjects/web_scripting/headphone.xlsx")
View(headphone)
data1 = headphone[,4:7]
s = scale(data1[,c(2,3,4)])
data2 = data.frame(s,rating=data1$Rating)

## lm ##
model1 <- lm(rating~.,data=data2)
summary(model1)
plot(model1)

# google only #

model2 <- lm(rating ~ SentimentScoreGoogle, data = data2)
summary(model2)

# google + vader #
model3 <- lm(rating ~ SentimentScoreGoogle + SentimentScoreVader, data = data2)
summary(model3)

# compare

compare1 <- anova(model2,model1)
compare1

compare2 <- anova(model3,model1)
compare2


## olr ##
model4 <- polr(as.factor(rating )~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob, data=data2, Hess=TRUE)
summary(model4)
ctable <- coef(summary(model4))
p <- pnorm(abs(ctable[, "t value"]), lower.tail = FALSE) * 2
ctable <- cbind(ctable, "p value" = p)
ctable
ci <- confint(model4)
exp(coef(model4))
exp(cbind(OR = coef(model4), ci))
newdat <- data.frame(
  SentimentScoreGoogle = seq(from = -2.71, to = 1.6537, length.out = 100),
  SentimentScoreVader = 0.3355,
  SentimentScoreTextBlob = -0.03134,
  price = 5)

newdat <- cbind(newdat, predict(model4, newdat, type = "probs"))
lnewdat <- melt(newdat, id.vars = c("SentimentScoreVader", "SentimentScoreTextBlob", "SentimentScoreGoogle","price"),
                variable.name = "Level", value.name="Probability")

lnewdat$google_transformed = lnewdat$SentimentScoreGoogle * attr(s, 'scaled:scale')['SentimentScoreGoogle'] + attr(s, 'scaled:center')['SentimentScoreGoogle']
ggplot(lnewdat, aes(x = google_transformed, y = Probability, colour = Level)) +
  geom_line() 

## Prediction ##
set.seed(1234)
ind<-sample(2,nrow(data2),replace=TRUE,prob = c(0.70,0.30))
train<-data2[ind==1,]
test<-data2[ind==2,]
l1<-ifelse(train$rating == 1,"1",ifelse(train$rating == 2,"2",ifelse(train$rating == 3,"3","4+")))
new1<- data.frame(train[,c(1,2,3)],l1)
l2<-ifelse(test$rating == 1,"1",ifelse(test$rating == 2,"2",ifelse(test$rating == 3,"3","4+")))
new2 <- data.frame(test[,c(1,2,3)],l2)

# orl #
model5 <- polr(as.factor(rating)~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob, data=train, Hess=TRUE)
result1 <- predict(model5,test)  
table(result1, test$rating)

# randm forest#
model6<-randomForest(as.factor(rating)~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob,data = train, classwt = c(0.026,0.029,0.043,0.191,0.711),importance=TRUE,proximity=TRUE,ntree = 100)
result2 <- predict(model6,test)  
table(result2, test$rating)

# Improvement #
# orl #
model7 <- polr(as.factor(l1)~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob, data=new1, Hess=TRUE)
result3 <- predict(model7,new2)  
table(result3, new2$l2)


# randm forest#
model8<-randomForest(as.factor(l1)~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob,data = new1,classwt = c(0.026,0.029,0.043,0.902),importance=TRUE,proximity=TRUE,mrty=9,ntree = 100)
result4 <- predict(model8,new2)  
table(result4, new2$l2)






## movie ##
require(foreign)
require(ggplot2)
require(MASS)
require(Hmisc)
require(reshape2)
library(caret)
library(readxl)
movie <- read_excel("C:/Users/chen/PycharmProjects/web_scripting/movie.xlsx")
View(movie)
data1 = movie[,4:7]
s = scale(data1[,c(2,3,4)])
data2 = data.frame(s,rating=data1$Rating)

## lm ##
model1 <- lm(rating~.,data=data2)
summary(model1)
plot(model1)

# google only #

model2 <- lm(rating ~ SentimentScoreGoogle, data = data2)
summary(model2)

# google + vader #
model3 <- lm(rating ~ SentimentScoreGoogle + SentimentScoreVader, data = data2)
summary(model3)

# compare

compare1 <- anova(model2,model1)
compare1

compare2 <- anova(model3,model1)
compare2


## olr ##
model4 <- polr(as.factor(rating )~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob, data=data2, Hess=TRUE)
summary(model4)
ctable <- coef(summary(model4))
p <- pnorm(abs(ctable[, "t value"]), lower.tail = FALSE) * 2
ctable <- cbind(ctable, "p value" = p)
ctable
ci <- confint(model4)
exp(coef(model4))
exp(cbind(OR = coef(model4), ci))
newdat <- data.frame(
  SentimentScoreGoogle = seq(from = -2.71, to = 1.6537, length.out = 100),
  SentimentScoreVader = 0.3355,
  SentimentScoreTextBlob = -0.03134,
  price = 5)

newdat <- cbind(newdat, predict(model4, newdat, type = "probs"))
lnewdat <- melt(newdat, id.vars = c("SentimentScoreVader", "SentimentScoreTextBlob", "SentimentScoreGoogle","price"),
                variable.name = "Level", value.name="Probability")

lnewdat$google_transformed = lnewdat$SentimentScoreGoogle * attr(s, 'scaled:scale')['SentimentScoreGoogle'] + attr(s, 'scaled:center')['SentimentScoreGoogle']
ggplot(lnewdat, aes(x = google_transformed, y = Probability, colour = Level)) +
  geom_line() 

## Prediction ##
set.seed(1234)
ind<-sample(2,nrow(data2),replace=TRUE,prob = c(0.70,0.30))
train<-data2[ind==1,]
test<-data2[ind==2,]
l1<-ifelse(train$rating == 1,"1",ifelse(train$rating == 2,"2",ifelse(train$rating == 3,"3","4+")))
new3<- data.frame(train[,c(1,2,3)],l1)
l2<-ifelse(test$rating == 1,"1",ifelse(test$rating == 2,"2",ifelse(test$rating == 3,"3","4+")))
new4 <- data.frame(test[,c(1,2,3)],l2)



# orl #
model5 <- polr(as.factor(rating)~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob, data=train, Hess=TRUE)
result1 <- predict(model5,test)  
table(result1, test$rating)

##
result1   1   2   3   4   5
1  24  10   5   3   2
2   0   0   0   0   0
3   2   3   3   1   2
4   3  13  10  16   9
5   3   2  15  65 184  ##

# randm forest#
model6<-randomForest(as.factor(rating)~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob,data = train,importance=TRUE,proximity=TRUE,mrty=9,ntree = 100)
result2 <- predict(model6,test)  
table(result2, test$rating)

##
result2   1   2   3   4   5
1  22   9   4   4   1
2   1   3   0   3   1
3   5   6   7   6   1
4   1   1   6   8   9
5   3   9  16  64 185 ##

# Improvement #
# orl #
model7 <- polr(as.factor(l1)~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob, data=new3, Hess=TRUE)
result3 <- predict(model7,new4)  
table(result3, new4$l2)


# randm forest#
model8<-randomForest(as.factor(l1)~ SentimentScoreGoogle + SentimentScoreVader + SentimentScoreTextBlob,data = new3,classwt = c(0.11,0.06,0.09,0.74),importance=TRUE,proximity=TRUE,ntree = 100)
result4 <- predict(model8,new4)  
table(result4, new4$l2)





