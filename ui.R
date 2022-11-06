#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
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
library(shinythemes)

#Define UI for application that draws a histogram
ui <- fluidPage( theme =shinytheme("united"),
            
    # Navigation bar
    
    navbarPage( "NBA",
                
          navbarMenu( "Top 10 players of the game & field goals",
  
####################################################################################################

                  tabPanel("field goals statistics",
                  
    # Application title


    titlePanel("NBA's best players and field goals in 2017-18 season"),

    # Sidebar to select the type of shoot
    
    sidebarLayout(
        sidebarPanel(
            selectInput(inputId = "shoot",
                        label = "Shot type:",
                        choices = list("3 Points" = "3 Points","2 Points" = "2 Points","Free Throws" = "Free Throws") )
            ), # sidbarlayoutPanel
    
        # Show a plot of the generated distribution
        
        mainPanel(
            plotOutput("distPlot"), width = 10)  # mainpanel
        
    ) #sidebarPanel
        
       ), #navigation bar/panel1
##########################################################################################################

    tabPanel("field goals statistics insight",
             
             # Title
             
             titlePanel("NBA's best players and total field goals in 2017-18 season"),
            
             sidebarLayout(
               sidebarPanel = (
                 checkboxGroupInput( inputId = "shoot_type",
                                     label = "shot type",
                                     choices = list("3 Points" = "3 Points","2 Points" = "2 Points","Free Throws" = "Free Throws"),
                                     selected = "3 Points" )
               ),
               
               mainPanel( 
                      plotOutput("plot"), width = 10)
             )
             
             
    ) # tabpanel 
    

    ),#Menu 1
##################################################################################################################

  tabPanel("Player's positions and field goals",  
           
           titlePanel("NBA's players points based on position"),
           
           sidebarLayout(
             sidebarPanel = (
               checkboxGroupInput( inputId = "shoot_t",
                                   label = "shot type",
                                   choices = list("3 Points" = "3 Points","2 Points" = "2 Points","Free Throws" = "Free Throws"),
                                   selected = "3 Points" )
             ),
             
             mainPanel( 
               plotOutput("plot1"), width = 10)
           )
          
), # tabpanel 
###############################################################################################################
          
          navbarMenu( "Lebron James statistics ",
                      
                      tabPanel("Type of shoots",
                               
                               titlePanel("Lebron James Field Goals over the years"),
                               sidebarLayout( 
                               sidebarPanel = (
                                 checkboxGroupInput( inputId = "shoot_leb",
                                                     label = "Shot type",
                                                     choices = list("3 Points" = "3PT Field Goal","2 Points" = "2PT Field Goal"),
                                                     selected = "3PT Field Goal" )
                               ),
                               
                               mainPanel( 
                                 plotOutput("plot2"), width = 10)
                               
                              ) # sidebarL
                      ),#tab panel
                      
################################################################################################################                      
                      
                      tabPanel("Geolocalisation of shots", 
                               
                               
                               titlePanel("Lebron James geolocalised Field Goals over the years"),
                               
                               
                               sidebarLayout( 
                                 sidebarPanel = (
                                   sliderInput( inputId = "shoot_year",
                                                       label = "Year",
                                                        min = 2003,
                                                        max = 2017,
                                                        value = c("2003","2004","2005","2006","2007","2008","2009","2O10","2014","2015","2016","2017"),
                                                        step = 1,
                                    
                                                )
                                 ),
                                 
                                 mainPanel( 
                                   plotOutput("plot3"), width = 10)
                                 
                               )
                               
                                      
                               
                               
                               )
                
                               ) # Navbar 1
                      
              
)) # fluid page
    
    
    
    
  