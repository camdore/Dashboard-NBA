#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(dplyr)
library(ggplot2)
library(tidyr)
library(lubridate)

# 1-Define server logic required to draw a histogram
server <- function(input, output) {
    
    # Read NBA csv file and select the 10 best scorer
  
    nba18 = read.csv("csv_data_2018_clean.csv", header = TRUE, sep = ",")
    best_players = select(head( nba18[order(nba18$FG, decreasing = TRUE),], 10), Player, FG, X3P, X2P, FT)
    colnames(best_players) <- c("Player","FG","3 Points","2 Points","Free Throws")
    
    # 
    Position_points = select(nba18, Pos, X3P, X2P, FT)
    colnames(Position_points) <- c("Position","3 Points","2 Points","Free Throws")
    Position_points = aggregate(.~Position, data = Position_points, FUN = sum)
    
    # Read Lebron Geoloc data
    Lebronjames = read.csv("lebron_geoloc_clean.csv", header = TRUE, sep = ",")
    Lebronjames_shots <- select(Lebronjames, SHOT_TYPE, GAME_DATE)
    Lebronjames_shots$GAME_DATE <- year(ymd(Lebronjames_shots$GAME_DATE))
    Lebronjames_shots$Points <- rep(1,8369)                                     # dim(Lebronjames_shots) = [1] 8369    2
    Lebronjames_shots_tot = aggregate(Lebronjames_shots$Points, list(Lebronjames_shots$SHOT_TYPE,Lebronjames_shots$GAME_DATE), FUN = sum)
    colnames(Lebronjames_shots_tot ) <- c("Type_of_shot","Year","Points")
    
    PT_Field_Goal3 = filter(Lebronjames_shots_tot, Type_of_shot=="3PT Field Goal")$Points
    PT_Field_Goal2 = filter(Lebronjames_shots_tot, Type_of_shot=="2PT Field Goal")$Points
    year <- unique(Lebronjames_shots_tot[,c("Year")])
    bl <- 1:13
    Lebron <- data.frame(year,PT_Field_Goal3,PT_Field_Goal2,bl)
    colnames(Lebron) <- c("Year","3PT Field Goal","2PT Field Goal","NA")
####################################################################################      
    # Plot of 
    output$distPlot <- renderPlot({
      
        ggplot(best_players, aes(x = Player, y = best_players[, input$shoot])) + 
        geom_bar(stat = "identity", fill = "steelblue") + 
        xlab("Players") + 
        ylab( "shoots") +
        theme(text = element_text(size = 20))

         
    })
#########################################################################################
    output$plot <- renderPlot({ 
      
        best_players_longer = pivot_longer(select(best_players, Player, input$shoot_type ), !c(Player), names_to = "Type_of_point", values_to = "Points")
        best_players_longer$Type_of_point <- as.factor(best_players_longer$Type_of_point)
        best_players_longer$Type_of_point <- as.factor(best_players_longer$Type_of_point)
      
      ggplot(best_players_longer, aes(x = Player, y  = Points, fill= Type_of_point  )) + 
        geom_bar(stat = "identity" )+
        theme(text = element_text(size = 20))
      
    })
##########################################################################################
    output$plot1 <- renderPlot({ 
      
      Position_points_longer = pivot_longer(select(Position_points, Position, input$shoot_t ), !c(Position), names_to = "Type_of_point",values_to = "Points") 
      
      ggplot(Position_points_longer, aes(x = Position , y  = Points, fill= Type_of_point  )) + 
        geom_bar(stat = "identity" )+
        theme(text = element_text(size = 20))
      
    })

#####################################################################################################
    
    output$plot2 <- renderPlot({ 
      
    
      
      Lebronjames_shots_tot_fin = pivot_longer(select(Lebron, Year, input$shoot_leb ), !c(Year), names_to = "Type_of_shot",values_to = "Points") 
     
      ggplot(Lebronjames_shots_tot_fin , aes(x = Year , y  = Points, color= `Type_of_shot`)) + 
        geom_line() +
        geom_point()+
        xlab("Year")+
        ylab("Points")+
        theme(text = element_text(size = 20))
      
    })
    
#################################################################################################################    
    
    output$plot3 <- renderPlot({ 
      
      season_shots = Lebron_geo_shots[Lebron_geo_shots$GAME_DATE >= paste0(input$shoot_year,-10) & Lebron_geo_shots$GAME_DATE <=paste0(input$shoot_year+1,-4) , ]
      
      
      gg_court + geom_point(data = season_shots, aes(LOC_X, LOC_Y)) 
      
      
    })
      
}



