library(ggplot2)

data <- read.csv("/home/user/Documents/St.Olaf/Csci379/Project01_non_git/num_steps.csv")
data <- cbind(data, Group = apply(data, 1, function(x){return(1)}))

data$init_goal <- factor(data$init_goal, levels = unique(data$init_goal))

ggplot(data=data, aes(x=init_goal, y=num_steps, group = Group))+
  geom_point()+
  theme(axis.text.x = element_text(angle = 45),plot.margin = margin(0.5, 0.5, 0.5, 0, "cm"))+
  scale_x_discrete(breaks = data$init_goal[seq(1,90,by=10)])

summary(data$num_steps)
avg <- mean(data$num_steps)

ggplot(data=data, aes(x=Initial, y= num_steps, group=Initial))+
  geom_boxplot()+
  scale_x_continuous(breaks = 1:10)+
  scale_y_continuous(labels = seq(0,14,by=2), breaks =  seq(0,14,by=2))+
  geom_hline(yintercept=avg, color = "red")

ggplot(data=data, aes(x=Goal, y= num_steps, group=Goal))+
  geom_boxplot()+
  scale_x_continuous(breaks = 1:10)+
  scale_y_continuous(labels = seq(0,14,by=2), breaks =  seq(0,14,by=2))+
  geom_hline(yintercept=avg, color = "red")
