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
library(rsconnect)
library(plotly)
library(grid)
library(jpeg)
library(RCurl)

courtImg.URL <- "https://thedatagame.files.wordpress.com/2016/03/nba_court.jpg"
court <- rasterGrob(readJPEG(getURLContent(courtImg.URL)),
                    width=unit(1,"npc"), height=unit(1,"npc"))

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
    
    Lebronjames_shots_m <- select(Lebronjames, SHOT_TYPE, GAME_DATE, SHOT_ZONE_BASIC, SHOT_ZONE_RANGE)
    Lebronjames_shots_m$GAME_DATE <- year(ymd(Lebronjames_shots_m$GAME_DATE))
    
        # data frame (2 points in Mid-Range)
        Lebronjames_shots_md <- filter(Lebronjames_shots_m,SHOT_TYPE=="2PT Field Goal", SHOT_ZONE_BASIC=="Mid-Range")
        Lebronjames_shots_md$Points <- rep(1,1869)              # On a 1869 lignes 
        Lebronjames_shots_md = select(Lebronjames_shots_md,GAME_DATE,SHOT_TYPE,Points )
        Lebronjames_shots_md_tot = aggregate(Lebronjames_shots_md$Points, list(Lebronjames_shots_md$SHOT_TYPE,Lebronjames_shots_md$GAME_DATE), FUN = sum)
        # data frame (3 points in 24+ ft)
        Lebronjames_shots_ab <- filter(Lebronjames_shots_m,SHOT_TYPE=="3PT Field Goal", SHOT_ZONE_RANGE=="24+ ft.")
        Lebronjames_shots_ab$Points <- rep(1,1249)              # On a 1249 lignes
        Lebronjames_shots_ab = select(Lebronjames_shots_ab,GAME_DATE,SHOT_TYPE,Points )
        Lebronjames_shots_ab_tot = aggregate(Lebronjames_shots_ab$Points, list(Lebronjames_shots_ab$SHOT_TYPE,Lebronjames_shots_ab$GAME_DATE), FUN = sum)
      
        # New dataframe with usefull data (2 points in Mid-Range,3 points in 24+ ft)
        colnames(Lebronjames_shots_ab_tot ) <- c("Type_of_shot","Year","Points")
        colnames(Lebronjames_shots_md_tot ) <- c("Type_of_shot","Year","Points")
        year <- unique(Lebronjames_shots_ab_tot[,c("Year")])
        bl <- 1:13
        Lebron <- data.frame(year,PT_Field_Goal3,PT_Field_Goal2,bl)
        colnames(Lebron) <- c("Year","3PT Field Goal(Above 24 ft)","2PT Field Goal(in Mid-Range )","NA")  # Nouvelle data frame

    
    # Lebron James geo shot over the years
    Lebron_geo_shots = select(Lebronjames, LOC_X, LOC_Y, GAME_DATE, SHOT_TYPE, SHOT_ZONE_AREA)
    Lebron_geo_shots$GAME_DATE <- format(ymd(Lebron_geo_shots$GAME_DATE),'%Y-%m')
    
####################################################################################      
    # Plot of 
    output$distPlot <- renderPlot({
      
        ggplot(best_players, aes(x = Player, y = best_players[, input$shoot])) + 
        geom_bar(stat = "identity", fill = "steelblue") + 
        xlab("Players") + 
        ylab( "Points") +
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
     
      ggplot(Lebronjames_shots_tot_fin , aes(x = Year , y  = Points, color= `Type_of_shot`, linetype=`Type_of_shot`)) + 
        geom_line() +
        geom_point()+
        xlab("Year")+
        ylab("Points")+
        theme(text = element_text(size = 20))
      
    })
################################################################################################################
    
    output$plottt <- renderPlot({
      
  
      ggplot(nba18, aes(x=Age, fill=Pos)) + geom_histogram(bins = 23) + theme(text = element_text(size = 20)) + 
        xlab("Age") + 
        ylab("Number of player") +
        theme(text = element_text(size = 20))
    })
    

#################################################################################################################    
    
    output$plot3 <- renderPlot({ 
      
      season_shots = Lebron_geo_shots[Lebron_geo_shots$GAME_DATE >= paste0(input$shoot_year,-10) & Lebron_geo_shots$GAME_DATE <=paste0(input$shoot_year+1,-4) , ]
      
      if(input$shot_zones== "5"){
      
      
      ggplot(season_shots, aes(x=LOC_X, y=LOC_Y)) + 
        annotation_custom(court, -250, 250, -50, 420) +
        geom_point(aes(color = SHOT_ZONE_AREA )) +
        xlim(-250, 250) +
        ylim(-50, 420)+
        theme(text = element_text(size = 20))+
          xlab("X axis position")+
          ylab("Y axis position")}
      
      else{
        
          ggplot(season_shots, aes(x=LOC_X, y=LOC_Y)) + 
          annotation_custom(court, -250, 250, -50, 420) +
          geom_point(aes(color = SHOT_TYPE)) +
          xlim(-250, 250) +
          ylim(-50, 420)+
          theme(text = element_text(size = 20))+
          xlab("X axis position")+
          ylab("Y axis position")}
      
    })
    
}



