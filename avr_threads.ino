#include <LiquidCrystal.h>
#include <Thread.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

Thread taskOne = Thread();
Thread taskTwo = Thread();

typedef struct {
  char symbol;
  bool dir;
  int x_begin;
  int x_end;
  int x_old;
  int x_coord; 
} Arrow;

Arrow animatedArrow[6] = {' ', false, 9, 15, 12, 12};

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
  //char symbol;
  if(self->dir)
    self->symbol = '>';
  else
    self->symbol = '<';
  
  lcd.setCursor(self->x_old, 0);
  lcd.write(" ");
  lcd.setCursor(self->x_coord, 0);
  lcd.write(self->symbol);

  if (self->x_coord == self->x_end || self->x_coord == self->x_begin)
    self->dir = !self->dir;
  self->x_old = self->x_coord;
  if (self->dir)
    self->x_coord++;
   else
    self->x_coord--;

  // debug info on the second row: current coordinate and moving direction
  lcd.setCursor(5, 1);
  lcd.print(self->x_coord);
  lcd.print('=');
  lcd.print(self->dir);
}

void setup(){
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.write("Sec: ");
  //Arrow animatedArrow = {" ", true, 12, 15, 12, 12};
  taskOne.onRun(taskOneFunc);
  taskTwo.onRun(taskTwoFunc);
  //taskTwo.onRun(arrowStep(animatedArrow));
  taskOne.setInterval(1000);
  taskTwo.setInterval(100);  
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
