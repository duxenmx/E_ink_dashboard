# e_paper_dashboard
E-ink display using Raspberry Pi to display realtime weather, transit information, calendar and soon more

![E_paper_1](https://github.com/duxenmx/e_paper_dashboard/blob/main/pic/e_paper_1.png?raw=true)
![E_paper_2](https://github.com/duxenmx/e_paper_dashboard/blob/main/pic/e_paper_2.png?raw=true)


**SETUP**

1.Get your weather API Key from here https://home.openweathermap.org/users/sign_up.

2.Get your Transit API key from your local transit system, in my case I live in Vancouver, BC so my url would be https://developer.translink.ca/ServicesRtti, you will need to adjust significantly the dashboard_transit.py module to your local transit API, please be aware of that

3.Get your stop numbers, the program can do up to 4 stops showing 2 estimates per stop in the current space I provide it, for me I got the 5 digit codes from the transit app

4.Get your **longitude** and **lattitude** using I used https://www.latlong.net

5.**OPTIONAL STEP** I created a PM2 process so it can start on reboot and I wouldnt have to be meddling with it to start, if you want to do it as well take a look on the PM2 documentation

-run dashboard.py to start it

**Note**

-This code is made for 7.5 inch Version 2 display, if you are using another type of display please consult the documentation and adjust accordingly

-go to this website for e-ink display documentation of how to set it up and get it to work on your raspberry pi  https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT

-I used a raspberry pi zero w for this project however it should wourk fine on any other Pi as long as it has GPIO headers

-This is my first project in github, I'm still learning all its intricasies, if something is missing please let me know

-Still learning Python and squashing bugs as I progress, there is probably redundancies in the code so be gentle with it, =)

-Have fun with it and do something awesome!


**Parts**

-https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT

-Raspberry Pi zero W

-SD card for the Pi at least 8 GB.

-Power supply for the Pi.

-5x7 in frame

**Credit**

-Inspiration and using some of his code by [Abnormal Distributions] (https://github.com/AbnormalDistributions/e_paper_weather_display). go check out his cool project

-Icon designs are originally by [Erik Flowers] (https://erikflowers.github.io/weather-icons/). Some icons have been modified.

**Licensing**

Weather Icons licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL)

Code licensed under [MIT License](http://opensource.org/licenses/mit-license.html)

Documentation licensed under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0)
