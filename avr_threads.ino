#include <LiquidCrystal.h>
#include <Thread.h>

#include <SPI.h>  // for sd card
#include <SD.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

Thread taskOne = Thread();  // thread for task one, print time in seconds since controller start
Thread taskTwo = Thread();  // thread for task two, animation for ">" moving in the first LCD row between
                            // positions 9 and 15



typedef struct {
  char symbol;// = ' ';
  bool dir;// = false;
  int x_begin;// = 9;
  int x_end;// = 15;
  int x_old;// = 12;
  int x_coord;// = 12; 
} Arrow;

//Arrow* animatedArrow = (Arrow*)malloc(sizeof(Arrow));
Arrow animatedArrow[] = {' ', false, 9, 15, 9, 9};

void taskOneFunc(){
  // Printing seconds since restart on the first row
  lcd.setCursor(5, 0);
  lcd.write("    ");
  lcd.setCursor(5, 0);
  lcd.print(millis() / 1000);
}

void taskTwoFunc(){
  // Running arrow ">" or "<"
  //Arrow animatedArrow;
  arrowStep(animatedArrow);
  delay(120);
//  lcd.setCursor(15, 1);
//  lcd.write(' ');
//  lcd.setCursor(14, 1);
//  lcd.write('@');
}

void arrowStep(Arrow *self){
  // function performs one single movement of the character ">" or "<"
  // depending on its current movement direction
  
  //char symbol;
  if(self->dir)
    self->symbol = '>';
  else
    self->symbol = '<';
  
  // update LCD 
  lcd.setCursor(self->x_old, 0);
  lcd.write(" ");
  lcd.setCursor(self->x_coord, 0);
  lcd.write(self->symbol);

  // update current coordinate and direction
  if (self->x_coord == self->x_end || self->x_coord == self->x_begin)
    self->dir = !self->dir;
  self->x_old = self->x_coord;
  if (self->dir)
    self->x_coord++;
   else
    self->x_coord--;

  // debug info on the second row: current coordinate and moving direction
  lcd.setCursor(5, 1);
  lcd.print("        ");
  int sc;
  sc = self->x_coord < 10 ? 6 : 5;
  lcd.setCursor(sc, 1);
  lcd.print(self->x_coord);
  lcd.print('|');
  lcd.print(self->dir ? "true" : "false");
}

void sdCardProgram() {
  // setup sd card variables
  Sd2Card card;
  SdVolume volume;
  SdFile root;
  
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.write("SD Card Init...");
  lcd.setCursor(0, 1);
  if (!card.init(SPI_HALF_SPEED, 4))
    lcd.write("Initialization failed");
  else
    lcd.write("Initialization OK");
  delay(1000);
  //char cardType[10];
  String cardType = "xxxx";
  lcd.setCursor(0, 1);
  switch (card.type()) {
    case SD_CARD_TYPE_SD1:
      cardType = "SD1";
      break;
    case SD_CARD_TYPE_SD2:
      cardType = "SD2";
      break;
    case SD_CARD_TYPE_SDHC:
      cardType = "SDHC";
      break;
    default:
      cardType = "Unknown";
  }
  lcd.print("Card Type: ");
  lcd.print(cardType);
  delay(2000);
}

void setup(){
  sdCardProgram();
  
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.write("Sec: ");
  lcd.setCursor(0, 1);
  lcd.write("Dbg:");
  //Arrow animatedArrow = {" ", true, 12, 15, 12, 12};
  taskOne.onRun(taskOneFunc);
  taskTwo.onRun(taskTwoFunc);
  //taskTwo.onRun(arrowStep(animatedArrow));
  taskOne.setInterval(100);  // call taskOne every 1000 ms
  taskTwo.setInterval(300);   // call taskTwo every 100 ms
}

void loop(){
  
  if (taskOne.shouldRun())
    taskOne.run();

  if (taskTwo.shouldRun())
    taskTwo.run();
 
//  lcd.setCursor(0, 1);
//  lcd.write("+");
//  delay(33);
//  lcd.setCursor(0, 1);
//  lcd.write(".");
//  delay(33);
}
